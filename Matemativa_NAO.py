
from naoqi import ALProxy
import random
import time

ip = "Digite o IP do seu ROBÔ"
port = 9559
tts = ALProxy("ALTextToSpeech", ip, port)
motion = ALProxy("ALMotion", ip, port)

# Lista de perguntas simples
perguntas = [
    {"pergunta": "Quanto é três mais quatro?", "resposta": "sete"},
    {"pergunta": "Quanto é cinco menos dois?", "resposta": "três"},
    {"pergunta": "Quanto é dois vezes três?", "resposta": "seis"},
    {"pergunta": "Quanto é oito dividido por dois?", "resposta": "quatro"}
]

# Escolher aleatoriamente
q = random.choice(perguntas)
tts.say("Vamos aprender matemática!")
tts.say(q["pergunta"])
tts.say("Você sabe a resposta?")

# (Aqui entraria o reconhecimento da fala ou simulação da resposta)
resposta_aluno = "sete"  # simulação

if resposta_aluno.lower() == q["resposta"]:
    tts.say("Muito bem! Você acertou!")
    # robô comemora
    motion.setAngles("HeadYaw", 1.0, 0.3)
    time.sleep(1)
    motion.setAngles("HeadYaw", -1.0, 0.3)
    time.sleep(1)
    motion.setAngles("HeadYaw", 0.0, 0.3)
else:
    tts.say("Hmm... quase! A resposta certa é " + q["resposta"] + ".")
