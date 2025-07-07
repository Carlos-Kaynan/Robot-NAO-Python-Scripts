# -*- encoding: UTF-8 -*- 

'''
use Python 2.7
Exemplo que mostra como usar o ALMath com Python e enviar os resultados
para o robô usando um proxy para o ALMotion.
'''

import sys
import time

from naoqi import ALProxy
import almath

def main(IP):
    PORT = 9559  # Porta padrão para se comunicar com o NAO

    # Cria um proxy para o módulo ALMotion (movimentação do robô)
    try:
        motionProxy = ALProxy("ALMotion", IP, PORT)
    except Exception as e:
        print("Não foi possível criar o proxy para ALMotion")
        print("O erro foi:", e)

    chainName = "RArm"     # Nome da cadeia de articulações a ser controlada (braço direito)
    space = 1              # Espaço de referência (1 = espaço do mundo, World)
    useSensors = True      # Utiliza os sensores para obter a posição real

    # Liga a rigidez do corpo inteiro, permitindo movimento
    motionProxy.stiffnessInterpolation("Body", 1.0, 0.5)

    # Coloca o robô em pé e prepara os motores
    motionProxy.moveInit()

    # ---------------------------------------------------------
    # Recupera a matriz de transformação usando o ALMotion
    # ---------------------------------------------------------

    # Recupera a transformação atual do braço direito no espaço do mundo
    # e converte para uma matriz de transformação do ALMath
    origTransform = almath.Transform(
        motionProxy.getTransform(chainName, space, useSensors))

    # Mostra a matriz original no terminal
    print("Transformação original")
    print(origTransform)

    # ---------------------------------------------------------
    # Usa o ALMath para fazer cálculos com a matriz de transformação
    # ---------------------------------------------------------

    # Cria uma nova transformação de movimento: 5cm para frente (eixo X) e 5cm para cima (eixo Z)
    moveTransform = almath.Transform.fromPosition(0.05, 0.0, 0.05)

    # Calcula a nova matriz de destino aplicando o movimento à transformação original
    targetTransform = moveTransform * origTransform

    # Mostra a matriz de destino no terminal
    print("Transformação alvo")
    print(targetTransform)

    # ---------------------------------------------------------
    # Envia a transformação de destino para o robô via ALMotion
    # ---------------------------------------------------------

    # Converte a matriz de transformação para uma lista (formato exigido pelo ALMotion)
    targetTransformList = list(targetTransform.toVector())

    # Envia a transformação desejada para o braço direito do NAO
    fractionOfMaxSpeed = 0.5  # Velocidade de movimento (50% da máxima)
    axisMask = almath.AXIS_MASK_VEL  # Máscara de eixos para permitir movimento linear (X, Y, Z)

    motionProxy.setTransform(
        chainName,          # Cadeia de articulações (braço direito)
        space,              # Espaço de referência (World)
        targetTransformList,# Nova transformação a ser aplicada
        fractionOfMaxSpeed, # Fração da velocidade máxima
        axisMask            # Máscara para definir os eixos ativos
    )

    # Espera 2 segundos para observar o movimento
    time.sleep(2.0)


# Verifica se o IP do robô foi fornecido como argumento ao script
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Uso: python almath_transform.py robotIP")
        sys.exit(1)

    # Executa a função principal com o IP fornecido
    main(sys.argv[1])

