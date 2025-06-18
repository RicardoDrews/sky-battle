
import pygame
import sys
import random
import math
import datetime
import os
import speech_recognition as sr
import pyttsx3


LARGURA = 1000
ALTURA = 700
FPS = 60

PLAYER_LARGURA, PLAYER_ALTURA = 100, 80
BOSS_LARGURA, BOSS_ALTURA = 390, 700

pygame.init()
pygame.mixer.init() 
musica =('Recursos/sons/musica.wav')
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sky Battle")
clock = pygame.time.Clock()

COR_BRONZE_ESCURO = (80, 42, 4)
COR_LATÃO = (205, 127, 50)
COR_COBRE_HOVER = (218, 165, 32)
COR_PERGAMINHO = (235, 225, 200)
COR_TEXTO_ESCURO = (48, 25, 15)
COR_PAINEL = (48, 25, 15, 200) 

try:
    font_titulo_steampunk = pygame.font.Font('Recursos/fontes/Metamorphous-Regular.ttf', 68)
    font_texto_steampunk = pygame.font.Font('Recursos/fontes/Lora-Regular.ttf', 26)
    font_texto_bold_steampunk = pygame.font.Font('Recursos/fontes/Lora-Bold.ttf', 28)
    font_input_steampunk = pygame.font.Font('Recursos/fontes/Lora-Regular.ttf', 40)
except FileNotFoundError:
    print("ERRO: Fontes Steampunk não encontradas! Verifique a pasta 'Recursos/fontes/'.")
    font_titulo_steampunk = pygame.font.SysFont("serif", 72)
    font_texto_steampunk = pygame.font.SysFont("serif", 30)
    font_texto_bold_steampunk = pygame.font.SysFont("serif", 32, bold=True)
    font_input_steampunk = pygame.font.SysFont("serif", 42)


fundo_menu_img = None
try:
    fundo_menu_img = pygame.image.load('Recursos/imagens/fundo_menu_steampunk.jpg').convert()
except FileNotFoundError:
    try:
        fundo_menu_img = pygame.image.load('Recursos/imagens/fundo_menu_steampunk.png').convert_alpha()
    except FileNotFoundError:
        print("ERRO CRÍTICO: Imagem de fundo não encontrada!")
        print("Certifique-se que o arquivo 'fundo_menu_steampunk.jpg' ou '.png' existe na pasta 'Recursos/imagens/'.")
if fundo_menu_img:
    fundo_menu_img = pygame.transform.scale(fundo_menu_img, (LARGURA, ALTURA))


engine = pyttsx3.init()


background = pygame.image.load('Recursos/imagens/background.png').convert()
background = pygame.transform.scale(background, (LARGURA, ALTURA))
player_img = pygame.image.load('Recursos/imagens/aviao.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_LARGURA, PLAYER_ALTURA))
boss_img = pygame.image.load('Recursos/imagens/boss.png').convert_alpha()
boss_img = pygame.transform.scale(boss_img, (BOSS_LARGURA, BOSS_ALTURA))
cloud_img = pygame.image.load('Recursos/imagens/nuvem.png').convert_alpha()
moon_img = pygame.image.load('Recursos/imagens/lua.png').convert_alpha()
rosto_feliz = pygame.image.load('Recursos/imagens/rosto_feliz.png').convert_alpha()
rosto_medio = pygame.image.load('Recursos/imagens/rosto_machucado.png').convert_alpha()
rosto_ferido = pygame.image.load('Recursos/imagens/rosto_muito_machucado.png').convert_alpha()
vida_sheet = pygame.image.load('Recursos/imagens/vida.PNG').convert_alpha()


NUM_FRAMES_VIDA = 4
FRAME_LARGURA_VIDA = vida_sheet.get_width() // NUM_FRAMES_VIDA
FRAME_ALTURA_VIDA = vida_sheet.get_height()
ESCALA_HUD = 2.0
frames_vida = []
for i in range(NUM_FRAMES_VIDA):
    frame = vida_sheet.subsurface(pygame.Rect(i * FRAME_LARGURA_VIDA, 0, FRAME_LARGURA_VIDA, FRAME_ALTURA_VIDA))
    frame = pygame.transform.scale(frame, (int(FRAME_LARGURA_VIDA * ESCALA_HUD), int(FRAME_ALTURA_VIDA * ESCALA_HUD)))
    frames_vida.append(frame)
FRAME_LARGURA = frames_vida[0].get_width()
FRAME_ALTURA = frames_vida[0].get_height()
ROSTO_SIZE = (FRAME_LARGURA - 20, FRAME_ALTURA - 20)
rosto_feliz = pygame.transform.scale(rosto_feliz, ROSTO_SIZE)
rosto_medio = pygame.transform.scale(rosto_medio, ROSTO_SIZE)
rosto_ferido = pygame.transform.scale(rosto_ferido, ROSTO_SIZE)

def carregar_frames(path, num_quadros, escala=1):
    sheet = pygame.image.load(path).convert_alpha()
    largura_frame = sheet.get_width() // num_quadros
    altura_frame = sheet.get_height()
    frames = []
    for i in range(num_quadros):
        frame = sheet.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
        if escala != 1:
            frame = pygame.transform.scale(frame, (int(largura_frame * escala), int(altura_frame * escala)))
        frames.append(frame)
    return frames

player_tiro_frames = carregar_frames('Recursos/imagens/tiro_sheet.png', 8)
boss_tiro1_frames = carregar_frames('Recursos/imagens/tiro1_sheet.png', 8, escala=2)
boss_tiro2_frames = carregar_frames('Recursos/imagens/tiro2_sheet.png', 8, escala=2)
boss_tiro3_frames = carregar_frames('Recursos/imagens/tiro3_sheet.png', 8, escala=2)

class Moon:
    def __init__(self):
        self.image = moon_img
        self.base_size = 150
        self.scale = 1
        self.growing = True
    def update(self, dt):
        if self.growing:
            self.scale += 0.5 * dt
            if self.scale >= 1.2: self.growing = False
        else:
            self.scale -= 0.5 * dt
            if self.scale <= 0.8: self.growing = True
    def draw(self, tela):

        size = int(self.base_size * self.scale)
        resized = pygame.transform.scale(self.image, (size, size))
        tela.blit(resized, (20, 20))

class Cloud:
    def __init__(self):
        self.image = cloud_img
        self.rect = self.image.get_rect(bottom=ALTURA)
        self.tiles = []
        num_tiles = LARGURA // self.rect.width + 2
        for i in range(num_tiles):
            tile_rect = self.image.get_rect(x=(i * self.rect.width), bottom=ALTURA)
            self.tiles.append(tile_rect)
    def update(self, dt): pass
    def draw(self, tela):
        for tile_rect in self.tiles:
            tela.blit(self.image, tile_rect)

class TiroAnimado:
    def __init__(self, frames, x, y, speed=600, direcao=1, vel_y=0):
        self.frames, self.index = frames, 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed, self.anim_speed = speed, 15
        self.direcao, self.vel_y = direcao, vel_y
    def update(self, dt):
        self.rect.x += self.speed * dt * self.direcao
        self.rect.y += self.vel_y * dt
        self.index = (self.index + self.anim_speed * dt) % len(self.frames)
        self.image = self.frames[int(self.index)]
    def draw(self, tela):
        tela.blit(self.image, self.rect)

class TiroEspecial(TiroAnimado):
    def __init__(self, frames, x, y, nivel_carga):
        super().__init__(frames, x, y, speed=800)
        self.nivel_carga = nivel_carga 
        self.dano = 50 + (150 * self.nivel_carga)
        self.escala = 1.0 + (5.0 * self.nivel_carga)
        self.largura_original, self.altura_original = self.frames[0].get_rect().size
        self.image = pygame.transform.scale(self.frames[0], (int(self.largura_original * self.escala), int(self.altura_original * self.escala)))
        self.rect = self.image.get_rect(midleft=(x, y))

    def update(self, dt):
        self.rect.x += self.speed * dt * self.direcao
        self.rect.y += self.vel_y * dt
        self.index = (self.index + self.anim_speed * dt) % len(self.frames)
        imagem_original_do_frame = self.frames[int(self.index)]
        centro_anterior = self.rect.center
        self.image = pygame.transform.scale(imagem_original_do_frame, (int(self.largura_original * self.escala), int(self.altura_original * self.escala)))
        self.rect = self.image.get_rect(center=centro_anterior)

class BossTiroAnimado:
    def __init__(self, frames, x, y, vel_x, vel_y):
        self.frames, self.index = frames, 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x, self.vel_y, self.anim_speed = vel_x, vel_y, 12
    def update(self, dt):
        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt
        self.index = (self.index + self.anim_speed * dt) % len(self.frames)
        self.image = self.frames[int(self.index)]
    def draw(self, tela):
        tela.blit(self.image, self.rect)

class Laser:
    def __init__(self, y_inicial, x_inicial, x_alvo):
        self.y = y_inicial
        self.x_inicial = x_inicial
        self.x_alvo = x_alvo
        self.cor_carregando = (0, 255, 0, 150)
        self.cor_ativo = (255, 0, 0)
        self.altura = 25 
        self.estado = "carregando"
        self.timer = 0
        self.duracao_carga = 1.5
        self.duracao_ativo = 0.5
        self.aviso_rect = pygame.Rect(min(self.x_inicial, self.x_alvo), self.y - 2, abs(self.x_alvo - self.x_inicial), 4)
        self.rect = pygame.Rect(0, 0, 0, 0)
    def update(self, dt):
        self.timer += dt
        if self.estado == "carregando" and self.timer >= self.duracao_carga:
            self.estado = "ativo"
            self.timer = 0
            self.rect = pygame.Rect(min(self.x_inicial, self.x_alvo), self.y - self.altura // 2, abs(self.x_alvo - self.x_inicial), self.altura)
        elif self.estado == "ativo" and self.timer >= self.duracao_ativo:
            self.estado = "desvanecendo"
            self.rect = pygame.Rect(0, 0, 0, 0)
    def draw(self, tela):
        if self.estado == "carregando":
            if int(self.timer * 10) % 2 == 0:
                surface = pygame.Surface(self.aviso_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(surface, self.cor_carregando, surface.get_rect())
                tela.blit(surface, self.aviso_rect.topleft)
        elif self.estado == "ativo":
            pygame.draw.rect(tela, self.cor_ativo, self.rect)
            pygame.draw.rect(tela, (255, 255, 255), self.rect, 3)

class Player:
    def __init__(self):
        self.img = player_img
        self.rect = self.img.get_rect(center=(100, ALTURA // 2))
        self.velocidade, self.vidas = 6, 3
        self.projeteis, self.direcao_y = [], 0
        self.atirando, self.tempo_ultimo_tiro = False, 0
        self.carregando_especial = False
        self.tempo_inicio_carga = 0
        self.nivel_carga = 0.0
        self.tempo_max_carga = 2000
    def mover(self, teclas):
        self.direcao_y = 0
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade; self.direcao_y = -1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade; self.direcao_y = 1
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))
    def atirar(self):
        self.projeteis.append(TiroAnimado(player_tiro_frames, self.rect.right, self.rect.centery, vel_y=self.direcao_y * 200))
    def comecar_carga(self):
        self.carregando_especial = True
        self.tempo_inicio_carga = pygame.time.get_ticks()
        self.nivel_carga = 0
    def atualizar_carga(self):
        if self.carregando_especial:
            tempo_carregado = pygame.time.get_ticks() - self.tempo_inicio_carga
            self.nivel_carga = min(1.0, tempo_carregado / self.tempo_max_carga)
    def atirar_especial(self):
        if self.carregando_especial or self.nivel_carga > 0.1:
            tiro_especial = TiroEspecial(player_tiro_frames, self.rect.right, self.rect.centery, self.nivel_carga)
            self.projeteis.append(tiro_especial)
        self.carregando_especial = False
        self.nivel_carga = 0
    def desenhar(self, tela):
        tela.blit(self.img, self.rect)
        if self.carregando_especial:
            raio = int(PLAYER_LARGURA / 2 * self.nivel_carga)
            cor = (255, 255, 0, 100)
            if self.nivel_carga >= 1.0:
                cor = (255, 100, 0, 150)
            if raio > 5:
                aura_surf = pygame.Surface((raio*2, raio*2), pygame.SRCALPHA)
                pygame.draw.circle(aura_surf, cor, (raio, raio), raio)
                tela.blit(aura_surf, (self.rect.centerx - raio, self.rect.centery - raio))

class Boss:
    def __init__(self, player):
        self.img_original = boss_img
        self.img = boss_img.copy()
        self.rect = self.img.get_rect(right=LARGURA, centery=ALTURA // 2)
        self.vida_maxima, self.vida = 2000, 2000
        self.projeteis = []
        self.lasers = []
        self.tempo_ultimo_ataque = 0
        self.intervalo_ataque = 2500
        self.flash_timer, self.player = 0, player
        self.angulo_espiral = 0
        self.ataque_espiral_ativo = False
        self.timer_espiral = 0
        self.inicio_espiral = 0
    def receber_dano(self, dano):
        self.vida = max(0, self.vida - dano)
        self.flash_timer = 0.1
    def atualizar(self, dt):
        tempo_atual = pygame.time.get_ticks()
        if self.ataque_espiral_ativo:
            self.timer_espiral += dt
            if self.timer_espiral > 0.1: 
                self.ataque_espiral()
                self.timer_espiral = 0
            if pygame.time.get_ticks() - self.inicio_espiral > 3000:
                self.ataque_espiral_ativo = False
        if not self.ataque_espiral_ativo and tempo_atual - self.tempo_ultimo_ataque > self.intervalo_ataque:
            lista_de_ataques_pesada = [
                'laser_teleguiado', 'laser_teleguiado',
                'barragem_horizontal', 'barragem_horizontal',
                'tiro_mirado', 'tiro_mirado',
                'barragem_giratoria'
            ]
            ataque = random.choice(lista_de_ataques_pesada)
            self.iniciar_ataque(ataque)
            self.tempo_ultimo_ataque = tempo_atual
        if self.flash_timer > 0:
            self.flash_timer -= dt
            self.img = self.img_original.copy()
            self.img.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
        else:
            self.img = self.img_original.copy()
    def iniciar_ataque(self, tipo):
        if tipo == 'barragem_giratoria':
            self.ataque_espiral_ativo = True
            self.inicio_espiral = pygame.time.get_ticks()
        elif tipo == 'laser_teleguiado':
            novo_laser = Laser(self.rect.centery, self.rect.left, self.player.rect.centerx)
            self.lasers.append(novo_laser)
        elif tipo == 'barragem_horizontal':
            tamanho_gap = self.player.rect.height * 3.0
            posicao_gap_y = random.randint(0, ALTURA - int(tamanho_gap))
            y = 0
            while y < ALTURA:
                if not (posicao_gap_y < y < posicao_gap_y + tamanho_gap):
                    proj = BossTiroAnimado(boss_tiro2_frames, self.rect.left, y, -300, 0)
                    self.projeteis.append(proj)
                y += 40
        elif tipo == 'tiro_mirado':
            dx = self.player.rect.centerx - self.rect.left 
            dy = self.player.rect.centery - self.rect.centery
            dist = max(1, math.hypot(dx, dy))
            velocidade_tiro = 250
            vel_x = velocidade_tiro * (dx / dist)
            vel_y = velocidade_tiro * (dy / dist)
            proj = BossTiroAnimado(boss_tiro1_frames, self.rect.left, self.rect.centery, vel_x, vel_y)
            self.projeteis.append(proj)
    def ataque_espiral(self):
        velocidade_espiral = 180
        for i in range(4):
            angulo = self.angulo_espiral + (i * math.pi / 2)
            vel_x = velocidade_espiral * math.cos(angulo)
            vel_y = velocidade_espiral * math.sin(angulo)
            proj = BossTiroAnimado(boss_tiro3_frames, self.rect.left, self.rect.centery, vel_x, vel_y)
            self.projeteis.append(proj)
        self.angulo_espiral += 0.15
    def esta_morto(self): return self.vida <= 0
    def desenhar(self, tela): 
        tela.blit(self.img, self.rect)
        for laser in self.lasers:
            laser.draw(tela)

class Game:
    def __init__(self):
        self.player = Player()
        self.boss = Boss(self.player)
        self.cloud = Cloud()
        self.moon = Moon()
        self.pontuacao, self.proximidade_bonus = 0, 0
        self.bg_x1, self.bg_x2 = 0, LARGURA
        self.velocidade_fundo, self.pausado = 2, False
        self.tempo_inicio = pygame.time.get_ticks()
        self.vida_frame_index, self.vida_anim_timer = 0, 0
        self.vida_anim_speed = 8
    def atualizar_fundo(self):
        self.bg_x1 -= self.velocidade_fundo
        self.bg_x2 -= self.velocidade_fundo
        if self.bg_x1 <= -LARGURA: self.bg_x1 = LARGURA
        if self.bg_x2 <= -LARGURA: self.bg_x2 = LARGURA
    def atualizar_jogo(self, dt):
        if self.pausado: return
        self.atualizar_fundo()
        self.cloud.update(dt)
        self.moon.update(dt)
        self.player.atualizar_carga()
        self.boss.atualizar(dt)
        
        if self.player.atirando and pygame.time.get_ticks() - self.player.tempo_ultimo_tiro > 150:
            self.player.atirar()
            self.player.tempo_ultimo_tiro = pygame.time.get_ticks()
            
        for proj in self.boss.projeteis:
            if abs(proj.rect.centerx - self.player.rect.centerx) < 100:
                self.proximidade_bonus += dt * 10
        for tiro in self.player.projeteis[:]:
            tiro.update(dt)
            if tiro.rect.left > LARGURA: self.player.projeteis.remove(tiro)
            else:
                tiro_hitbox = tiro.rect.inflate(-tiro.rect.width * 0.6, -tiro.rect.height * 0.6)
                boss_hitbox = self.boss.rect.inflate(-self.boss.rect.width * 0.4, -self.boss.rect.height * 0.2)
                if tiro_hitbox.colliderect(boss_hitbox):
                    dano = getattr(tiro, 'dano', 10)
                    self.boss.receber_dano(dano)
                    pontos_base = 20
                    pontos_bonus = 0
                    if isinstance(tiro, TiroEspecial):
                        pontos_bonus = int(100 * tiro.nivel_carga)
                    self.pontuacao += pontos_base + pontos_bonus
                    if tiro in self.player.projeteis: self.player.projeteis.remove(tiro)
        for proj in self.boss.projeteis[:]:
            proj.update(dt)
            if not tela.get_rect().inflate(100, 100).colliderect(proj.rect):
                if proj in self.boss.projeteis: self.boss.projeteis.remove(proj)
            else:
                proj_hitbox = proj.rect.inflate(-proj.rect.width * 0.5, -proj.rect.height * 0.5)
                player_hitbox = self.player.rect.inflate(-self.player.rect.width * 0.3, -self.player.rect.height * 0.4)
                if proj_hitbox.colliderect(player_hitbox):
                    self.player.vidas -= 1
                    if proj in self.boss.projeteis: self.boss.projeteis.remove(proj)
        for laser in self.boss.lasers[:]:
            laser.update(dt)
            if laser.estado == "ativo":
                player_hitbox = self.player.rect.inflate(-self.player.rect.width * 0.3, -self.player.rect.height * 0.4)
                if laser.rect.colliderect(player_hitbox):
                    self.player.vidas -= 1
                    laser.estado = "desvanecendo"
            if laser.estado == "desvanecendo" and laser.timer > 0.1:
                self.boss.lasers.remove(laser)
    def desenhar_hud(self):
        self.vida_anim_timer += 1
        if self.vida_anim_timer >= FPS // self.vida_anim_speed:
            self.vida_anim_timer = 0
            self.vida_frame_index = (self.vida_frame_index + 1) % NUM_FRAMES_VIDA
        rosto = rosto_feliz if self.player.vidas >= 3 else rosto_medio if self.player.vidas == 2 else rosto_ferido
        pos_x, pos_y = 20, ALTURA - FRAME_ALTURA - 20
        rosto_x = pos_x + (FRAME_LARGURA - ROSTO_SIZE[0]) // 2
        rosto_y = pos_y + (FRAME_ALTURA - ROSTO_SIZE[1]) // 2
        tela.blit(rosto, (rosto_x, rosto_y))
        tela.blit(frames_vida[self.vida_frame_index], (pos_x, pos_y))
        vidas_txt = font_input_steampunk.render(f"x{self.player.vidas}", True, COR_PERGAMINHO)
        tela.blit(vidas_txt, (pos_x + FRAME_LARGURA + 15, pos_y + FRAME_ALTURA // 2 - vidas_txt.get_height() // 2 + 5))
        pontos_txt = font_texto_bold_steampunk.render(f"Pontos: {int(self.pontuacao)}", True, COR_PERGAMINHO)
        tela.blit(pontos_txt, (20, 20))
    def desenhar(self):
        tela.blit(background, (self.bg_x1, 0))
        tela.blit(background, (self.bg_x2, 0))
        self.boss.desenhar(tela)
        self.cloud.draw(tela)
        self.player.desenhar(tela)
        self.moon.draw(tela)
        for tiro in self.player.projeteis: tiro.draw(tela)
        for proj in self.boss.projeteis: proj.draw(tela)
        self.desenhar_hud()
        if self.pausado:
            pause_surface = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            pause_surface.fill((0, 0, 0, 150))
            tela.blit(pause_surface, (0, 0))
            pause_text = font_titulo_steampunk.render("PAUSADO", True, (255, 80, 80))
            tela.blit(pause_text, (LARGURA//2 - pause_text.get_width()//2, ALTURA//2 - pause_text.get_height()//2))
        pygame.display.flip()
    def salvar_log(self, pontuacao, tempo_total):
        agora = datetime.datetime.now()
        data_str, hora_str = agora.strftime("%d-%m-%Y"), agora.strftime("%H:%M:%S")
        with open("log.dat", "a") as f:
            f.write(f"{data_str};{hora_str};Pontuação: {int(pontuacao)};Tempo: {int(tempo_total)}s\n")
    def mostrar_logs(self):

        painel_rect = pygame.Rect(0, 0, LARGURA - 150, ALTURA - 200)
        painel_rect.center = (LARGURA // 2, ALTURA // 2 + 50)
        
        esperando = True
        while esperando:
            tela.fill(COR_BRONZE_ESCURO)
            desenhar_placa_metalica(tela, painel_rect)
            titulo = font_titulo_steampunk.render("Registro de Batalhas", True, COR_PERGAMINHO)
            titulo_rect = titulo.get_rect(center=(painel_rect.centerx, painel_rect.top + 50))
            tela.blit(titulo, titulo_rect)
            
            if os.path.exists("log.dat"):
                with open("log.dat", "r") as f:
                    linhas = f.readlines()[-10:] 
                
                y_offset = titulo_rect.bottom + 40
                for linha in reversed(linhas):
                    partes = linha.strip().split(';')
                    if len(partes) >= 4:
                        log_str = f"Data: {partes[0]} | Pontos: {partes[2].split(': ')[1]} | Tempo: {partes[3].split(': ')[1]}"
                        texto_surf = font_texto_steampunk.render(log_str, True, COR_PERGAMINHO)
                        texto_rect = texto_surf.get_rect(midleft=(painel_rect.left + 40, y_offset))
                        tela.blit(texto_surf, texto_rect)
                        y_offset += 35
            else:
                texto_surf = font_texto_steampunk.render("Nenhum registro encontrado.", True, COR_PERGAMINHO)
                texto_rect = texto_surf.get_rect(center=painel_rect.center)
                tela.blit(texto_surf, texto_rect)
            
            info_surf = font_texto_steampunk.render("(O jogo fechará em alguns segundos...)", True, COR_LATÃO)
            info_rect = info_surf.get_rect(center=(LARGURA / 2, painel_rect.bottom + 40))
            tela.blit(info_surf, info_rect)

            pygame.display.flip()
            pygame.time.wait(8000)
            esperando = False
    def run(self):
        while True:
            dt = clock.tick(FPS) / 1000
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'sair'
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE: self.pausado = not self.pausado
                    if not self.pausado:
                        if evento.key == pygame.K_f: self.player.atirando = True
                        if evento.key == pygame.K_LSHIFT:
                            self.player.comecar_carga()
                if evento.type == pygame.KEYUP and not self.pausado:
                    if evento.key == pygame.K_f: self.player.atirando = False
                    if evento.key == pygame.K_LSHIFT:
                        self.player.atirar_especial()
            if not self.pausado:
                self.player.mover(pygame.key.get_pressed())
                self.atualizar_jogo(dt)
            if self.player.vidas <= 0:
                return self.fim_de_jogo(False)
            if self.boss.esta_morto():
                return self.fim_de_jogo(True)
            self.desenhar()
    def fim_de_jogo(self, venceu):
        tempo_total = (pygame.time.get_ticks() - self.tempo_inicio) / 1000
        bonus_de_tempo = 0
        if venceu:
            tempo_base_bonus = 60 
            pontos_por_segundo = 50
            bonus_de_tempo = max(0, (tempo_base_bonus - tempo_total) * pontos_por_segundo)
            self.pontuacao += bonus_de_tempo
        self.salvar_log(self.pontuacao, tempo_total)
        
        msg = "Vitória Gloriosa!" if venceu else "Derrota Honrosa"
        cor_msg = (180, 255, 180) if venceu else (255, 180, 180)
        
        botao_reiniciar_rect = pygame.Rect(0, 0, 250, 70)
        botao_sair_rect = pygame.Rect(0, 0, 250, 70)

        while True:
            tela.fill((0, 0, 0)) 
            
            texto = font_titulo_steampunk.render(msg, True, cor_msg)
            texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 180))
            tela.blit(texto, texto_rect)

            pontos = font_texto_bold_steampunk.render(f"Pontuação Final: {int(self.pontuacao)}", True, COR_PERGAMINHO)
            pontos_rect = pontos.get_rect(center=(LARGURA // 2, texto_rect.bottom + 50))
            tela.blit(pontos, pontos_rect)

            if venceu and bonus_de_tempo > 0:
                bonus_txt = font_texto_steampunk.render(f"Bônus por Tempo: +{int(bonus_de_tempo)}", True, (255, 255, 100))
                bonus_rect = bonus_txt.get_rect(center=(LARGURA // 2, pontos_rect.bottom + 30))
                tela.blit(bonus_txt, bonus_rect)
                botao_reiniciar_rect.center = (LARGURA // 2, bonus_rect.bottom + 70)
            else:
                botao_reiniciar_rect.center = (LARGURA // 2, pontos_rect.bottom + 70)
            
            botao_sair_rect.center = (LARGURA // 2, botao_reiniciar_rect.bottom + 40)
            
            mouse_pos = pygame.mouse.get_pos()
            
            reiniciar_hover = botao_reiniciar_rect.collidepoint(mouse_pos)
            desenhar_botao_steampunk(tela, botao_reiniciar_rect, "REINICIAR", font_texto_bold_steampunk, reiniciar_hover)

            sair_hover = botao_sair_rect.collidepoint(mouse_pos)
            desenhar_botao_steampunk(tela, botao_sair_rect, "SAIR", font_texto_bold_steampunk, sair_hover)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'sair'
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if reiniciar_hover:
                        return 'reiniciar'
                    if sair_hover:
                        self.mostrar_logs()
                        return 'sair'

def desenhar_fundo_steampunk(tela):
    if fundo_menu_img:
        tela.blit(fundo_menu_img, (0,0))
    else:
        tela.fill(COR_BRONZE_ESCURO)
def desenhar_placa_metalica(tela, rect, cor_borda=COR_LATÃO, espessura=4):
    sombra_rect = rect.copy(); sombra_rect.move_ip(5, 5)
    pygame.draw.rect(tela, (0, 0, 0, 100), sombra_rect)
    pygame.draw.rect(tela, COR_PAINEL, rect)
    pygame.draw.rect(tela, cor_borda, rect, espessura)
    rebite_raio = espessura * 1.5
    pygame.draw.circle(tela, cor_borda, rect.topleft, rebite_raio)
    pygame.draw.circle(tela, cor_borda, rect.topright, rebite_raio)
    pygame.draw.circle(tela, cor_borda, rect.bottomleft, rebite_raio)
    pygame.draw.circle(tela, cor_borda, rect.bottomright, rebite_raio)
def desenhar_botao_steampunk(tela, rect, texto, font, is_hovered):
    cor_borda = COR_COBRE_HOVER if is_hovered else COR_LATÃO
    desenhar_placa_metalica(tela, rect, cor_borda, 4 if is_hovered else 3)
    txt_surf = font.render(texto, True, COR_PERGAMINHO)
    tela.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, rect.centery - txt_surf.get_height()//2))
def falar(msg):
    try:
        engine.say(msg); engine.runAndWait()
    except Exception: pass

def tela_input_nome():
    nome, ativo = "", True
    cursor_visivel, cursor_timer = True, 0
    dt = 0
    painel_rect = pygame.Rect(0, 0, 800, 500)
    painel_rect.center = (LARGURA // 2, ALTURA // 2)
    while ativo:
        desenhar_fundo_steampunk(tela)
        input_box = pygame.Rect(0, 0, 500, 70)
        input_box.center = (LARGURA / 2, ALTURA/ 1.5)
        desenhar_placa_metalica(tela, input_box)
        entrada_surf = font_input_steampunk.render(nome, True, COR_PERGAMINHO)
        pos_x_texto = input_box.centerx - entrada_surf.get_width() // 2
        pos_y_texto = input_box.centery - entrada_surf.get_height() // 2
        tela.blit(entrada_surf, (pos_x_texto, pos_y_texto))
        cursor_timer += dt * 1000
        if cursor_timer > 500:
            cursor_timer %= 500
            cursor_visivel = not cursor_visivel
        if cursor_visivel:
            cursor_x = pos_x_texto + entrada_surf.get_width() + 3 
            pygame.draw.line(tela, COR_PERGAMINHO, (cursor_x, input_box.y + 15), (cursor_x, input_box.y + input_box.height - 15), 2)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and nome.strip(): ativo = False
                elif e.key == pygame.K_BACKSPACE: nome = nome[:-1]
                elif len(nome) < 15 and e.unicode.isprintable(): nome += e.unicode
    falar(f"Bem-vindo a bordo, Capitão {nome}!")
    return nome
def tela_boas_vindas(nome):
    painel_rect = pygame.Rect(0, 0, 800, 600)
    painel_rect.center = (LARGURA // 2, ALTURA // 2)
    botao_rect = pygame.Rect(0, 0, 350, 70)
    botao_rect.center = (painel_rect.centerx, painel_rect.bottom - 60)
    esperando = True
    dt = 0
    falar("Diga 'iniciar' ou acione o painel para começar a expedição.")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try: recognizer.adjust_for_ambient_noise(source, duration=0.5)
        except Exception: pass
        while esperando:
            desenhar_fundo_steampunk(tela)
            desenhar_placa_metalica(tela, painel_rect)
            titulo = font_titulo_steampunk.render(f"Capitão {nome}", True, COR_PERGAMINHO)
            titulo_rect = titulo.get_rect(center=(painel_rect.centerx, painel_rect.top + 45))
            tela.blit(titulo, titulo_rect)
            subtitulo = font_texto_bold_steampunk.render("--- Ordem de Missão ---", True, COR_LATÃO)
            subtitulo_rect = subtitulo.get_rect(center=(painel_rect.centerx, titulo_rect.bottom + 40))
            tela.blit(subtitulo, subtitulo_rect)
            

            instrucoes = [
                "Navegue com as TECLAS DE SETA ou W/S.",
                "Pressione F para tiro rápido.",
                "Segure SHIFT para carregar o especial.",
                "Solte para disparar um tiro poderoso.",
                "Evite os projéteis da autômata inimiga.",
                "Use ESPAÇO para uma pausa tática."
            ]
            y_inicial_instrucoes = subtitulo_rect.bottom + 40
            for i, linha in enumerate(instrucoes):
                linha_surf = font_texto_steampunk.render(linha, True, COR_PERGAMINHO)
                linha_rect = linha_surf.get_rect(center=(painel_rect.centerx, y_inicial_instrucoes + (i * 38)))
                tela.blit(linha_surf, linha_rect)
                
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = botao_rect.collidepoint(mouse_pos)
            desenhar_botao_steampunk(tela, botao_rect, "INICIAR EXPEDIÇÃO", font_texto_bold_steampunk, is_hovered)
            pygame.display.flip()
            dt = clock.tick(FPS) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and is_hovered: esperando = False
            if esperando:
                try:
                    audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=3)
                    comando = recognizer.recognize_google(audio, language="pt-BR").lower()
                    if "começar" in comando or "iniciar" in comando: esperando = False
                except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
                    pass

if __name__ == "__main__":
    pygame.mixer.music.load(musica)
    pygame.mixer.music.set_volume(0.07)
    pygame.mixer.music.play(-1)

    nome_jogador = tela_input_nome()
    while True:
        tela_boas_vindas(nome_jogador)
        jogo = Game()
        acao_final = jogo.run()
        if acao_final == 'sair':
            break
        elif acao_final == 'reiniciar':
            continue
        pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
