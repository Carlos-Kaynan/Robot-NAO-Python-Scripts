# -*- coding: utf-8 -*-

'''Instale as bibliotecas pynput e naoqi'''

from pynput import keyboard
from naoqi import ALProxy
import sys

# Substitua pelo IP do seu robô
ROBOT_IP = "192.168.1.100"
PORT = 9559

# Cria o proxy para ALMotion
try:
    motionProxy = ALProxy("ALMotion", ROBOT_IP, PORT)
except Exception as e:
    print("Erro ao conectar com ALMotion:", e)
    sys.exit(1)

# Inicializa o movimento
motionProxy.stiffnessInterpolation("Body", 1.0, 1.0)
motionProxy.moveInit()

# Velocidades (ajuste conforme necessário)
velocidade_frente = 0.2
velocidade_re = -0.2
velocidade_rotacao = 0.5

def on_press(key):
    try:
        if key == keyboard.Key.up:
            print("Frente")
            motionProxy.moveToward(velocidade_frente, 0.0, 0.0)

        elif key == keyboard.Key.down:
            print("Ré")
            motionProxy.moveToward(velocidade_re, 0.0, 0.0)

        elif key == keyboard.Key.left:
            print("Girar para a esquerda")
            motionProxy.moveToward(0.0, 0.0, velocidade_rotacao)

        elif key == keyboard.Key.right:
            print("Girar para a direita")
            motionProxy.moveToward(0.0, 0.0, -velocidade_rotacao)

    except Exception as e:
        print("Erro ao processar tecla:", e)

def on_release(key):
    # Quando soltar qualquer tecla de seta, o NAO para de se mover
    if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
        print("Parar movimento")
        motionProxy.stopMove()

    # Encerra o programa ao pressionar ESC
    if key == keyboard.Key.esc:
        print("Encerrando programa...")
        motionProxy.stopMove()
        motionProxy.rest()
        return False  # Retorna False para parar o listener

# Inicia o listener de teclado
print("Use as setas do teclado para controlar o NAO. Pressione ESC para sair.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
