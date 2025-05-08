# -*- codificação: UTF-8 -*- 

''' Este exemplo mostra como guiar NAO pela mão, enquanto calcula seus 
    movimentos apenas com passos, usando a biblioteca ALMath. O recorte de passos é 
    descrito em almath_foot_clip.py. 
    http://doc.aldebaran.com/1-14/dev/python/examples/almath/index.html#using-almath-with-almotion ''' 

'''
O exemplo a seguir permite que você guie o NAO pelo braço. 
Ele gera passos de acordo com a posição do braço esquerdo e, em seguida, os corta para garantir que sejam possíveis para o NAO.

Para usar o exemplo, execute o script fornecendo o IP do seu NAO como argumento. 
O NAO se levantará. Quando estiver pronto, segure o braço esquerdo do NAO e pressione o sensor tátil frontal. 
Agora você pode guiar o NAO inclinando o braço para frente e para trás e fazê-lo girar girando o pulso esquerdo. 
Os olhos do NAO ficarão verdes quando a posição do braço indicar um alvo e azuis quando a posição do braço for neutra. 
Para finalizar o exemplo, pressione o sensor tátil traseiro: o NAO se agachará e removerá sua rigidez.

'''

import  sys 
import  time 
import  math 

from  naoqi  import  ALProxy 
import  almath 

import  almath_foot_clip 

armName  =  "LArm" 
lFootOffset  =  almath . Pose2D ( 0.0 ,  0.09 ,  0.0 ) 
rFootOffset  =  almath . Pose2D ( 0.0 ,  - 0.09 ,  0.0 ) 
stepSpeed = 1.0 
stepLength  =  0.05 

def  initRobotPosition ( motionProxy ): 
  ''' Inicia a posição e a rigidez de NAO para tornar a orientação possível.''' 

  motionProxy . stiffnessInterpolation ( "Corpo" ,  1.0 ,  0.5 ) 
  motionProxy . moveInit () 
  time . sleep ( 1.0 ) 
  # Solte o braço esquerdo. 
  motionProxy . setAngles ( "LWristYaw" ,  0.0 ,  1.0 ,  True ) 
  motionProxy . setAngles ( "Cabeça" ,  [ 0.44 ,  -0.44 ], 0.5 ) 
  motionProxy . setStiffnesses ( "LArm" , 0.0 )
  motionProxy . setStiffnesses ( "LWristYaw" , 0.2 ) 
  # Desabilite os movimentos do braço ao caminhar sobre o braço esquerdo . 
  motionProxy . setWalkArmsEnabled ( False , True ) 
  time . sleep ( 1.0 ) 
  
  
def interpretJointsPose ( motionProxy , memoryProxy ): 
  ''' Traduz a postura atual do braço esquerdo em uma posição alvo para o       pé do NAO.''' 
  
  # Recupera a posição atual do braço. armPose 

  armPose =  motionProxy . getAngles ( armName ,  True ) 
  targetX  =  0.0 
  targetY  =  0.0 
  targetTheta  =  0.0 
  gaitConfig  =  motionProxy . getMoveConfig ( "Default" ) 

  # Filtrar inclinação do ombro. 
  if (armPose[0] > - 0.9 and armPose[0] < -0.20):
    targetX = stepLength
  elif (armPose[0] > -2.5 and armPose[0] < -1.5):
    targetX = - stepLength - 0.02


  # Filtrar guinada do pulso. 
  if  ( armPose [ 4 ]  >  0.2 ): 
    targetTheta  =  gaitConfig [ 2 ][ 1 ] 
  elif  ( armPose [ 4 ]  <  - 0.2 ): 
    targetTheta  =  -  gaitConfig [ 2 ][ 1 ] 

  # Retorna a pose correspondente. 
  return  almath . Pose2D ( targetX ,  targetY ,  targetTheta ) 


def  moveToTargetPose ( targetPose ,  motionProxy ,  isLeftSupport ): 
  ''' Mover para o alvo desejado com o pé atual. ''' 

  targetTf  =  almath . transformFromPose2D ( targetPose ) 

  # Calcula a posição do pé com o deslocamento em NAOSpace. 
  if  ( isLeftSupport ): 
    footTargetTf  =  targetTf  *  almath . transformFromPose2D ( rFootOffset ) 
    footTargetPose  =  almath . pose2DFromTransform ( footTargetTf ) 
    name  =  [ "RLeg" ]
  else : 
    footTargetTf  =  targetTf  *  almath . transformFromPose2D ( lFootOffset ) 
    footTargetPose  =  almath . pose2DFromTransform ( footTargetTf ) 
    name  =  [ "LLeg" ] 

  # Recorte o passo para evitar colisões e passos muito largos. 
  almath_foot_clip . clipFootStep ( footTargetPose ,  isLeftSupport ) 

  step  =  [[ footTargetPose . x ,  footTargetPose . y ,  footTargetPose . theta ]] 
  speed = [stepSpeed]

  # Envia o passo para NAO. 
  motionProxy . setFootStepsWithSpeed ​​( name ,  step ,  speed ,  False ) 

  # Altera o pé atual. 
  isLeftSupport  =  not  isLeftSupport 


def  main ( robotIP ): 

  # Inicializa proxies. 
  try : 
    memoryProxy  =  ALProxy ( "ALMemory" ,  robotIP ,  9559 ) 
  except  Exception ,  e : 
    print  ("Não foi possível criar proxy para ALMemory" )
    print  ("O erro foi: " ,  e )

  try : 
    motionProxy  =  ALProxy ( "ALMotion" ,  robotIP ,  9559 ) 
  except  Exception ,  e : 
    print  ("Não foi possível criar proxy para ALMotion" )
    print  ("O erro foi: " ,  e )

  try : 
    ledsProxy  =  ALProxy ( "ALLeds" ,  robotIP ,  9559 ) 
  except  Exception ,  e : 
    print  ("Não foi possível criar proxy para ALLeds" )
    print  ("O erro foi: " ,  e )

  # Inicializar posição do robô. 
  initRobotPosition ( motionProxy ) 

  # Aguarde até que o usuário pressione o sensor tátil frontal. 
  while ( not  memoryProxy . getData ( "FrontTactilTouched" )): 
    pass 

  # Comece movendo o pé esquerdo. 
  isLeftSupport  =  False 
  isMoving  =  False 
  ledsProxy . fadeRGB ( "FaceLeds" ,  255 ,  0.1 ) 

  while  ( not  memoryProxy . getData ( "RearTactilTouched" )): 
    targetPose  =  interpretJointsPose ( motionProxy ,  memoryProxy ) 

    # Filtre a pose para evitar passos muito pequenos. 
    if  ( math . fabs ( targetPose . x )  >  0.01  or \
         math . fabs ( targetPose . y )  >  0.01  or \
         math . fabs ( targetPose . theta )  >  0.08 ): 
      moveToTargetPose ( targetPose ,  motionProxy ,  isLeftSupport ) 
      isLeftSupport  =  not  isLeftSupport 
      isMoving  =  True 
      # Define os LEDs para verde. 
      ledsProxy . fadeRGB ( "FaceLeds" ,  256  *  255 ,  0.1 ) 

    elif  ( isMoving ): 
      # Para o robô. 
      motionProxy . stopMove () 
      isMoving  =  False 
      # Define os LEDs para azul. 
      ledsProxy . fadeRGB ( "FaceLeds" ,  255 ,  0.1 ) 

  # Define os LEDs para branco. 
  ledsProxy . fadeRGB ( "FaceLeds" ,  256  *  256  *  255  +  256  *  255  +  255 ,  0.1 ) 

  # Crouch. 
  motionProxy . rest () 


if  __name__  ==  "__principal__" : 
  if  ( len( sys . argv )  <  2 ): 
    print  ("Uso python almath_robot_guide.py robotIP")
    sys . exit ( 1 ) 

  main ( sys . argv [ 1 ])
