#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import threading

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import LargeMotor, MediumMotor, SpeedPercent


class RoboDancarino:
    def __init__(self):
        self.leds = Leds()
        self.som = Sound()

        try:
            self.perna_esquerda = LargeMotor(OUTPUT_B)
            self.perna_direita = LargeMotor(OUTPUT_C)
            self.bracos = MediumMotor(OUTPUT_D)
        except:
            print("ERRO: Verifique os motores!")
            exit()

        self.rodando = False

    def tocar_musica(self):
        # Ode a Alegria
        self.som.play_song((
            ('E4', 'q'), ('E4', 'q'), ('F4', 'q'), ('G4', 'q'),
            ('G4', 'q'), ('F4', 'q'), ('E4', 'q'), ('D4', 'q'),
            ('C4', 'q'), ('C4', 'q'), ('D4', 'q'), ('E4', 'q'),
            ('E4', 'h'), ('D4', 'h'),

            ('E4', 'q'), ('E4', 'q'), ('F4', 'q'), ('G4', 'q'),
            ('G4', 'q'), ('F4', 'q'), ('E4', 'q'), ('D4', 'q'),
            ('C4', 'q'), ('C4', 'q'), ('D4', 'q'), ('E4', 'q'),
            ('D4', 'h'), ('C4', 'h')
        ))

    def iniciar(self, bpm=120):
        print("Iniciando danca com BPM: {}".format(bpm))
        self.rodando = True

        self.leds.set_color("LEFT", "GREEN")
        self.leds.set_color("RIGHT", "GREEN")

        # Musica em paralelo
        threading.Thread(target=self.tocar_musica, daemon=True).start()

        # Loop da danca
        threading.Thread(target=self._loop_danca, args=(bpm,), daemon=True).start()

    def parar(self):
        print("Parando danca...")
        self.rodando = False
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")

    def mover_bracos(self):
        # Movimento suave
        self.bracos.on_for_degrees(SpeedPercent(30), 40)
        self.bracos.on_for_degrees(SpeedPercent(30), -40)

    def girar_esquerda(self, vel, tempo):
        self.perna_direita.run_timed(speed_sp=vel, time_sp=tempo)
        self.perna_esquerda.run_timed(speed_sp=-vel, time_sp=tempo)

    def girar_direita(self, vel, tempo):
        self.perna_direita.run_timed(speed_sp=-vel, time_sp=tempo)
        self.perna_esquerda.run_timed(speed_sp=vel, time_sp=tempo)

    def _loop_danca(self, bpm):
        cores = ["GREEN", "RED", "AMBER", "YELLOW"]
        velocidade = 100

        tempo_batida = min(1000, (round(60000 / bpm)) * 0.65)
        print("Tempo por batida: {} ms".format(tempo_batida))

        while self.rodando:
            # LEDs mudando
            cor = random.choice(cores)
            self.leds.set_color("LEFT", cor)
            self.leds.set_color("RIGHT", cor)

            # Bracos
            self.mover_bracos()

            # Gira pra esquerda
            self.girar_esquerda(velocidade, 300)
            time.sleep(tempo_batida / 1000)

            # Gira pra direita
            self.girar_direita(velocidade, 300)
            time.sleep(tempo_batida / 1000)

            # Movimento rapido (efeito danca)
            self.girar_esquerda(velocidade + 50, 150)
            self.girar_direita(velocidade + 50, 150)

        print("Danca finalizada.")


if __name__ == '__main__':
    robo = RoboDancarino()

    try:
        bpm = random.randint(80, 140)
        robo.iniciar(bpm)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        robo.parar()