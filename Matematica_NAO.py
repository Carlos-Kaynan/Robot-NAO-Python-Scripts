# -*- codificação: UTF-8 -*- 
#use Python 2.7 
'''
🤖💡 Projeto: “NAO, o Professor de Matemática Interativo”
🎯 Objetivo:
Ensinar e testar conceitos básicos de matemática (adição, subtração, multiplicação, divisão) de forma interativa com fala, gestos e reconhecimento de resposta por voz ou botões.

📚 Público-alvo:
Alunos do ensino fundamental (ou alfabetizados).

Pode ser adaptado para alunos com dificuldades de aprendizagem.

🧠 Conceito:
O robô faz perguntas de matemática em voz alta, por exemplo:

“Quanto é 3 + 4?”

Ele então oferece opções:

“A: cinco. B: sete. C: nove.”

O aluno pode responder de forma verbal ou apertando botões (em interface externa ou virtual). O NAO então:

Confirma se a resposta está correta.

Reage com alegria se o aluno acertar (dança, comemoração).

Dá dicas ou reforça a explicação se errar.

🛠️ Funcionalidades técnicas:
Uso de ALTextToSpeech para perguntas/respostas.

Expressões faciais e corporais simples com ALMotion.

Aleatoriedade nas perguntas com Python.

Reconhecimento de fala simples (com ALSpeechRecognition) ou simulação por botões.

Pode evoluir para reconhecimento facial e personalização para cada aluno.



'''



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


'''
🚀 Possíveis extensões:
🎨 Integração com painel gráfico no computador ou tablet.

🎤 Adição de reconhecimento de fala real.

🧠 Níveis de dificuldade adaptativos.

📊 Coleta de dados sobre desempenho dos alunos.

🧩 Gamificação (pontuação, fases, etc.).

'''
