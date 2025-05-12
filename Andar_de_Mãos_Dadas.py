# -*- codificação: UTF-8 -*- 


'''
http://doc.aldebaran.com/1-14/dev/python/examples/almath/index.html#using-almath-with-almotion 

Este exemplo mostra como guiar o robô NAO usando seu braço esquerdo.
Movimentos do braço são interpretados como comandos de movimento (andar ou girar).
Usa a biblioteca ALMath para calcular passos e transforma essas poses em movimentos reais.

Para usar o exemplo, execute o script fornecendo o IP do seu NAO como argumento. 
O NAO se levantará. Quando estiver pronto, segure o braço esquerdo do NAO e pressione o sensor tátil frontal. 
Agora você pode guiar o NAO inclinando o braço para frente e para trás e fazê-lo girar girando o pulso esquerdo. 
Os olhos do NAO ficarão verdes quando a posição do braço indicar um alvo e azuis quando a posição do braço for neutra. 
Para finalizar o exemplo, pressione o sensor tátil traseiro: o NAO se agachará e removerá sua rigidez.

'''

import sys
import time
import math

from naoqi import ALProxy           # Permite comunicação com módulos do NAO (movimento, memória, LEDs)
import almath                       # Biblioteca de álgebra linear da SoftBank Robotics
import almath_foot_clip            # Script externo para limitar o tamanho e direção dos passos

# Nome do braço que será usado para controle
armName = "LArm"

# Offset dos pés em relação ao centro do robô (usado para calcular passos)
lFootOffset = almath.Pose2D(0.0, 0.09, 0.0)
rFootOffset = almath.Pose2D(0.0, -0.09, 0.0)

# Parâmetros para velocidade e tamanho dos passos
stepSpeed = 1.0
stepLength = 0.05

# Função para inicializar a posição e configuração do NAO
def initRobotPosition(motionProxy):
    ''' Inicializa a posição e rigidez do NAO, desativando o controle do braço esquerdo. '''
    
    motionProxy.stiffnessInterpolation("Body", 1.0, 0.5)  # Ativa rigidez de todo o corpo
    motionProxy.moveInit()                                # Prepara o robô para movimento
    time.sleep(1.0)

    # Ajusta articulações para posição inicial
    motionProxy.setAngles("LWristYaw", 0.0, 1.0, True)
    motionProxy.setAngles("Head", [0.44, -0.44], 0.5)

    # Desativa a rigidez do braço esquerdo para que o usuário possa movê-lo manualmente
    motionProxy.setStiffnesses("LArm", 0.0)
    motionProxy.setStiffnesses("LWristYaw", 0.2)

    # Desativa movimento automático dos braços ao caminhar (somente o braço esquerdo é afetado)
    motionProxy.setWalkArmsEnabled(False, True)
    time.sleep(1.0)


# Função para interpretar a pose atual do braço e converter em movimento
def interpretJointsPose(motionProxy, memoryProxy):
    ''' Lê a pose do braço esquerdo e converte em uma posição de destino para os pés do robô. '''

    armPose = motionProxy.getAngles(armName, True)  # Lê ângulos das articulações do braço

    targetX = 0.0
    targetY = 0.0
    targetTheta = 0.0

    # Recupera configuração de caminhada padrão
    gaitConfig = motionProxy.getMoveConfig("Default")

    # Interpreta inclinação do ombro como movimento para frente ou para trás
    if (armPose[0] > -0.9 and armPose[0] < -0.20):
        targetX = stepLength  # Passo para frente
    elif (armPose[0] > -2.5 and armPose[0] < -1.5):
        targetX = -stepLength - 0.02  # Passo para trás

    # Interpreta rotação do punho como rotação do robô
    if (armPose[4] > 0.2):
        targetTheta = gaitConfig[2][1]  # Gira para um lado
    elif (armPose[4] < -0.2):
        targetTheta = -gaitConfig[2][1]  # Gira para o outro

    # Retorna a pose calculada (x, y, rotação)
    return almath.Pose2D(targetX, targetY, targetTheta)


# Função para executar o movimento baseado na pose alvo
def moveToTargetPose(targetPose, motionProxy, isLeftSupport):
    ''' Move o robô para a pose desejada, alternando entre os pés de apoio. '''

    # Converte a pose para uma matriz de transformação
    targetTf = almath.transformFromPose2D(targetPose)

    # Define o pé que irá se mover e aplica offset
    if isLeftSupport:
        footTargetTf = targetTf * almath.transformFromPose2D(rFootOffset)
        footTargetPose = almath.pose2DFromTransform(footTargetTf)
        name = ["RLeg"]  # Pé direito se move
    else:
        footTargetTf = targetTf * almath.transformFromPose2D(lFootOffset)
        footTargetPose = almath.pose2DFromTransform(footTargetTf)
        name = ["LLeg"]  # Pé esquerdo se move

    # Limita o passo para evitar ultrapassar limites físicos
    almath_foot_clip.clipFootStep(footTargetPose, isLeftSupport)

    step = [[footTargetPose.x, footTargetPose.y, footTargetPose.theta]]
    speed = [stepSpeed]

    # Executa o passo com a perna correspondente
    motionProxy.setFootStepsWithSpeed(name, step, speed, False)

    # Alterna o pé de apoio para o próximo passo
    isLeftSupport = not isLeftSupport


# Função principal
def main(robotIP):
    # Cria os proxies para acessar os módulos internos do NAO
    try:
        memoryProxy = ALProxy("ALMemory", robotIP, 9559)
    except Exception, e:
        print("Não foi possível criar proxy para ALMemory")
        print("O erro foi: ", e)

    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception, e:
        print("Não foi possível criar proxy para ALMotion")
        print("O erro foi: ", e)

    try:
        ledsProxy = ALProxy("ALLeds", robotIP, 9559)
    except Exception, e:
        print("Não foi possível criar proxy para ALLeds")
        print("O erro foi: ", e)

    # Inicializa posição do robô
    initRobotPosition(motionProxy)

    # Aguarda o usuário tocar o sensor tátil frontal (início)
    while not memoryProxy.getData("FrontTactilTouched"):
        pass

    # Inicializa variáveis de controle
    isLeftSupport = False
    isMoving = False

    # Define LEDs faciais como azuis (neutro)
    ledsProxy.fadeRGB("FaceLeds", 255, 0.1)

    # Loop principal: até que o sensor traseiro seja tocado (fim)
    while not memoryProxy.getData("RearTactilTouched"):
        targetPose = interpretJointsPose(motionProxy, memoryProxy)

        # Verifica se há movimento significativo a ser executado
        if (math.fabs(targetPose.x) > 0.01 or
            math.fabs(targetPose.y) > 0.01 or
            math.fabs(targetPose.theta) > 0.08):

            # Executa o movimento
            moveToTargetPose(targetPose, motionProxy, isLeftSupport)
            isLeftSupport = not isLeftSupport
            isMoving = True

            # Define LEDs para verde (movimento ativo)
            ledsProxy.fadeRGB("FaceLeds", 256 * 255, 0.1)

        elif isMoving:
            # Se não houver movimento, para o robô
            motionProxy.stopMove()
            isMoving = False

            # Define LEDs como azul (parado)
            ledsProxy.fadeRGB("FaceLeds", 255, 0.1)

    # Define LEDs como branco (fim do controle)
    ledsProxy.fadeRGB("FaceLeds", 256 * 256 * 255 + 256 * 255 + 255, 0.1)

    # Coloca o robô em repouso
    motionProxy.rest()


# Corrigido: nome correto para executar o script diretamente
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python almath_robot_guide.py <robotIP>")
        sys.exit(1)

    # Executa o programa principal com o IP do robô
    main(sys.argv[1])
