# -*- codificação: UTF-8 -*- 

# Use Python 2.7
# instalar o SDK NaoQi

from naoqi import ALProxy
import time

# Defina o IP e a porta do NAO
ip_nao = "192.168.1.100"  # Substitua pelo IP do seu robo
porta_nao = 9559

# Conectar aos modulos necessarios
movimento = ALProxy("ALMotion", ip_nao, porta_nao)
postura = ALProxy("ALRobotPosture", ip_nao, porta_nao)
fala = ALProxy("ALTextToSpeech", ip_nao, porta_nao)

# Ativar o modo de movimento
movimento.wakeUp()

# Fazer o robo sentar
postura.goToPosture("Sit", 1.0)
time.sleep(2)

# Fazer o robo levantar
postura.goToPosture("Stand", 1.0)
time.sleep(2)

# Fazer o robo andar 30 cm para frente
movimento.moveTo(0.3, 0, 0)  # (x, y, theta) -> 30 cm para frente
time.sleep(2)

# Fazer o robo virar 90 graus para a esquerda
movimento.moveTo(0, 0, 1.57)  # 1.57 radianos ≈ 90 graus à esquerda
time.sleep(2)

# Falar a frase final
fala.say("Cheguei ao meu destino")

# Relaxar o robo
movimento.rest()



""" Depois tentar testar controlar o andar do NAO com as setas do computador """


