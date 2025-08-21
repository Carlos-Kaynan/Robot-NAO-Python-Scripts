# -*- codificação: UTF-8 -*- 
#use python 2.7
#intale o SDK naoQi

from naoqi import ALProxy
import time

#:)
# IP e porta do seu robô
ip = "192.168.1.10"  # troque pelo IP do seu NAO
port = 9559

# Conectar aos módulos necessários
tts = ALProxy("ALTextToSpeech", ip, port)
motion = ALProxy("ALMotion", ip, port)
posture = ALProxy("ALRobotPosture", ip, port)

# Acordar o robô
motion.wakeUp()

# Começar em postura inicial
posture.goToPosture("StandInit", 0.5)

# Alongamento do pescoço
tts.say("Vamos começar com alongamento do pescoço.")
tts.say("Olhem para o lado direito.")
motion.setAngles("HeadYaw", -1.0, 0.2)  # gira cabeça para direita
time.sleep(2)

tts.say("Agora olhem para o lado esquerdo.")
motion.setAngles("HeadYaw", 1.0, 0.2)  # gira cabeça para esquerda
time.sleep(2)

# Voltar cabeça para frente
motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.2)
time.sleep(1)

tts.say("Agora olhem para cima.")
motion.setAngles("HeadPitch", -0.5, 0.2)  # cabeça para cima
time.sleep(2)

# Voltar cabeça para frente
motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.2)
time.sleep(1)

# Levantar braços
tts.say("Agora, levantem os braços comigo!")
# Braços para cima
names = ["LShoulderPitch", "RShoulderPitch"]
angles = [-1.0, -1.0]  # ângulo para levantar os braços
motion.setAngles(names, angles, 0.2)
time.sleep(3)

# Voltar braços
angles = [1.5, 1.5]  # posição de descanso
motion.setAngles(names, angles, 0.2)
time.sleep(2)

# Agachamento
tts.say("Agora, vamos agachar três vezes juntos!")
for i in range(3):
    tts.say("Agacha!")
    motion.setAngles("KneePitch", 1.0, 0.2)  # dobra os joelhos para agachar
    time.sleep(1)
    motion.setAngles("KneePitch", 0.0, 0.2)  # volta a ficar em pé
    time.sleep(1)

# Finalizar
tts.say("Muito bem! Terminamos nosso alongamento!")
posture.goToPosture("StandInit", 0.5)

# Dormir o robô
motion.rest()


'''
Observações importantes:
"HeadYaw" controla rotação horizontal da cabeça (olhar para os lados).

"HeadPitch" controla inclinação vertical da cabeça (olhar para cima/baixo).

"LShoulderPitch" e "RShoulderPitch" controlam levantar os braços.

"KneePitch" dobra os joelhos para simular um agachamento.

Esse script precisa ser rodado com o NAOqi SDK instalado.

O NAO precisa estar com motion enabled (ou seja, com motores ligados).




'''

