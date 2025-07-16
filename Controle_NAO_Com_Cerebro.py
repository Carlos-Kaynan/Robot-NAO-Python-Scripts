# -*- coding: utf-8 -*

#use Python 2.7

'''
Observações:
Troque robot_ip = "192.168.1.100" pelo IP real do seu robô.

O NAO precisa estar em uma superfície estável com espaço para andar.

Certifique-se de que o OpenViBE esteja transmitindo dados via LSL corretamente.
'''

#Baixar a biblioteca NAOQI / SDK Python
import time
import threading
from pylsl import StreamInlet, resolve_byprop
import numpy as np
from scipy.signal import butter, lfilter, welch
from naoqi import ALProxy

# Configurações
fs = 512
window_size = 0.5
samples_per_window = int(fs * window_size)
EEG_comando = "neutro"
tempo_neutro = time.time()

# Configurações do robô NAO
robot_ip = "192.168.1.100"  # Substitua pelo IP do seu NAO
port = 9559

# Proxies
motion = ALProxy("ALMotion", robot_ip, port)
tts = ALProxy("ALTextToSpeech", robot_ip, port)

# Inicializa rigidez e posição
motion.stiffnessInterpolation("Body", 1.0, 1.0)
motion.moveInit()

# Funções de filtro e análise
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band')

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    return lfilter(b, a, data, axis=0)

def band_power(signal):
    freqs, psd = welch(signal, fs)
    return np.sum(psd)

# Leitura contínua do EEG
def ler_sinais_EEG():
    global EEG_comando, tempo_neutro

    streams = resolve_byprop('name', 'openvibeSignal')
    if not streams:
        print("Nenhum stream LSL encontrado.")
        return

    inlet = StreamInlet(streams[0])
    buffer = []

    while True:
        sample, _ = inlet.pull_sample(timeout=1.0)
        if sample:
            buffer.append(sample)

        if len(buffer) >= samples_per_window:
            window = np.array(buffer[-samples_per_window:])
            c3 = window[:, 0]
            c4 = window[:, 1]

            mu_c3 = bandpass_filter(c3, 8, 13, fs)
            beta_c3 = bandpass_filter(c3, 13, 30, fs)
            mu_c4 = bandpass_filter(c4, 8, 13, fs)
            beta_c4 = bandpass_filter(c4, 13, 30, fs)

            mu_power_diff = band_power(mu_c4) - band_power(mu_c3)
            beta_power_diff = band_power(beta_c4) - band_power(beta_c3)

            if mu_power_diff > 0.5 or beta_power_diff > 0.5:
                EEG_comando = "abrir"
            elif mu_power_diff < -0.5 or beta_power_diff < -0.5:
                EEG_comando = "fechar"
            else:
                EEG_comando = "neutro"

# Controle do NAO baseado no EEG
def controlar_nao():
    global EEG_comando, tempo_neutro

    comando_anterior = None
    while True:
        if EEG_comando != comando_anterior:
            comando_anterior = EEG_comando

            if EEG_comando == "abrir":
                print("Comando: Andar")
                motion.moveToward(0.5, 0, 0)  # anda para frente com velocidade 0.5

            elif EEG_comando == "fechar":
                print("Comando: Parar")
                motion.stopMove()

            elif EEG_comando == "neutro":
                print("Comando: Concentre-se")
                motion.stopMove()
                tts.say("Concentre-se!")
        
        time.sleep(0.2)

# Executar em paralelo
t1 = threading.Thread(target=ler_sinais_EEG)
t2 = threading.Thread(target=controlar_nao)

t1.start()
t2.start()
