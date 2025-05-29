# -*- coding: utf-8 -*-

'''Instale as bibliotecas pynput e naoqi'''



from pynput import keyboard
from naoqi import ALProxy
import sys

# IP e porta do robô NAO
ROBOT_IP = "192.168.1.100"  # Substitua pelo IP do seu robô
PORT = 9559

# Conecta com o robô
try:
    motionProxy = ALProxy("ALMotion", ROBOT_IP, PORT)
except Exception as e:
    print("Erro ao conectar com ALMotion:", e)
    sys.exit(1)

# Inicializa movimento
motionProxy.stiffnessInterpolation("Body", 1.0, 1.0)
motionProxy.moveInit()

# Velocidade padrão
velocidade_base = 0.2
velocidade_rotacao = 0.5

# Estado atual de velocidade
vx, vy, vtheta = 0.0, 0.0, 0.0

def atualizar_movimento():
    """Aplica o movimento atual ao robô"""
    motionProxy.moveToward(vx, vy, vtheta)

def parar_movimento():
    """Para o robô"""
    global vx, vy, vtheta
    vx, vy, vtheta = 0.0, 0.0, 0.0
    motionProxy.stopMove()

def on_press(key):
    global vx, vy, vtheta, velocidade_base

    try:
        # Controles com teclas de seta
        if key == keyboard.Key.up or key.char == 'w':
            vx = velocidade_base
        elif key == keyboard.Key.down or key.char == 's':
            vx = -velocidade_base
        elif key == keyboard.Key.left or key.char == 'a':
            vtheta = velocidade_rotacao
        elif key == keyboard.Key.right or key.char == 'd':
            vtheta = -velocidade_rotacao

        # Movimento lateral (strafe)
        elif key.char == 'q':
            vy = velocidade_base
        elif key.char == 'e':
            vy = -velocidade_base

        # Aumentar velocidade
        elif key.char == '+':
            velocidade_base = min(velocidade_base + 0.05, 1.0)
            print(f"Velocidade aumentada: {velocidade_base:.2f}")

        # Diminuir velocidade
        elif key.char == '-':
            velocidade_base = max(velocidade_base - 0.05, 0.05)
            print(f"Velocidade reduzida: {velocidade_base:.2f}")

        atualizar_movimento()

    except AttributeError:
        pass  # Teclas sem char (ex: arrows) não têm .char

def on_release(key):
    global vx, vy, vtheta

    if key in [keyboard.Key.up, keyboard.Key.down,
               keyboard.Key.left, keyboard.Key.right]:
        parar_movimento()

    elif hasattr(key, 'char') and key.char in ['w', 's', 'a', 'd', 'q', 'e']:
        parar_movimento()

    elif key == keyboard.Key.esc:
        print("Encerrando...")
        parar_movimento()
        motionProxy.rest()
        return False  # Sai do listener

# Inicia escuta de teclado
print("""
Controles:
  ↑ / w : frente
  ↓ / s : trás
  ← / a : gira esquerda
  → / d : gira direita
  q : andar para a esquerda
  e : andar para a direita
  + : aumentar velocidade
  - : reduzir velocidade
  ESC: parar e sair
""")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


# Inicia o listener de teclado
print("Use as setas do teclado para controlar o NAO. Pressione ESC para sair.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
