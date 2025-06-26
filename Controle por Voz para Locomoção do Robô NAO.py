from naoqi import ALProxy
import time




# Endereço IP e porta do robô
NAO_IP = "192.168.1.10"  # Substitua pelo IP real do seu NAO
PORT = 9559

# Inicializa proxies
speech_recognition = ALProxy("ALSpeechRecognition", NAO_IP, PORT)
memory = ALProxy("ALMemory", NAO_IP, PORT)
motion = ALProxy("ALMotion", NAO_IP, PORT)
posture = ALProxy("ALRobotPosture", NAO_IP, PORT)

# Palavras-chave que o robô vai escutar
vocabulary = ["andar", "esquerda", "direita", "sentar"]

# Função principal
def main():
    # Acorda o robô e o coloca em posição inicial
    motion.wakeUp()
    posture.goToPosture("StandInit", 0.5)

    # Configura reconhecimento de voz
    speech_recognition.setLanguage("Portuguese")
    speech_recognition.setVocabulary(vocabulary, False)

    # Subscreve para começar a escutar
    speech_recognition.subscribe("Test_ASR")
    print("Ouvindo comandos: 'andar', 'esquerda', 'direita', 'sentar'...")

    try:
        while True:
            time.sleep(1)
            word = memory.getData("WordRecognized")

            if word and word[1] > 0.4:  # Confiança maior que 40%
                command = word[0]
                print("Comando reconhecido:", command)

                if command == "andar":
                    motion.moveTo(1.0, 0.0, 0.0)  # 1 metro para frente
                elif command == "esquerda":
                    motion.moveTo(0.0, 0.2, 0.0)  # 20 cm para esquerda
                elif command == "direita":
                    motion.moveTo(0.0, -0.2, 0.0)  # 20 cm para direita
                elif command == "sentar":
                    posture.goToPosture("Sit", 0.5)
                    break

                # Limpa o buffer de palavras reconhecidas
                memory.removeData("WordRecognized")

    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")

    finally:
        # Para o reconhecimento de voz
        speech_recognition.unsubscribe("Test_ASR")
        print("Encerrado.")

if __name__ == "__main__":
    main()
