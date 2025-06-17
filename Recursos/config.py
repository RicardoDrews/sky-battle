import pygame
import sys
import random
import math
import datetime
import os

LARGURA_TELA, ALTURA_TELA = 1000, 700
FPS = 60
FRAME_ALTURA = 32
FRAME_LARGURA = 32
PLAYER_LARGURA, PLAYER_ALTURA = 100, 80
BOSS_LARGURA, BOSS_ALTURA = 390, 700

COR_FUNDO = (20, 20, 40)
COR_TEXT = (255, 255, 255)
COR_BARRA_BG = (50, 50, 50)
COR_BARRA_HP = (200, 50, 50)


font_title = pygame.font.SysFont('consolas', 48)
font_ui = pygame.font.SysFont('consolas', 28)
font_small = pygame.font.SysFont('consolas', 20)