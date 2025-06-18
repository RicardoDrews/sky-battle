import pygame
import sys
import random
import math
import datetime
import os

# --- CONFIG ---
LARGURA = 1000
ALTURA = 700
FPS = 60
FRAME_ALTURA = 32
FRAME_LARGURA = 32

PLAYER_LARGURA, PLAYER_ALTURA = 100, 80
BOSS_LARGURA, BOSS_ALTURA = 390, 700

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("✈️ Avião vs Boss Robô")

# --- FONTES ---
font_title = pygame.font.SysFont('consolas', 48)
font_ui = pygame.font.SysFont('consolas', 28)
font_small = pygame.font.SysFont('consolas', 20)

clock = pygame.time.Clock()

# --- CORES ---
COR_FUNDO = (20, 20, 40)
COR_TEXT = (255, 255, 255)
COR_BARRA_BG = (50, 50, 50)
COR_BARRA_HP = (200, 50, 50)

# --- IMAGENS ---
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

# Redimensionar para caber dentro da moldura
ROSTO_SIZE = (FRAME_LARGURA - 10, FRAME_ALTURA - 10)  # ajuste a folga se quiser
rosto_feliz = pygame.transform.scale(rosto_feliz, ROSTO_SIZE)
rosto_medio = pygame.transform.scale(rosto_medio, ROSTO_SIZE)
rosto_ferido = pygame.transform.scale(rosto_ferido, ROSTO_SIZE)

# Carregar a moldura como uma animação
vida_sheet = pygame.image.load('Recursos/imagens/vida.PNG').convert_alpha()

NUM_FRAMES_VIDA = 4  # ajuste de acordo com seu sheet
FRAME_LARGURA = vida_sheet.get_width() // NUM_FRAMES_VIDA
FRAME_ALTURA = vida_sheet.get_height()

frames_vida = []
for i in range(NUM_FRAMES_VIDA):
    frame = vida_sheet.subsurface(pygame.Rect(i * FRAME_LARGURA, 0, FRAME_LARGURA, FRAME_ALTURA))
    frames_vida.append(frame)

# --- SPRITESHEET ---
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

# Player tiro
player_tiro_frames = carregar_frames('Recursos/imagens/tiro_sheet.png', 8)

# Boss tiros (maiores)
boss_tiro1_frames = carregar_frames('Recursos/imagens/tiro1_sheet.png', 8, escala=2)
boss_tiro2_frames = carregar_frames('Recursos/imagens/tiro2_sheet.png', 8, escala=2)
boss_tiro3_frames = carregar_frames('Recursos/imagens/tiro3_sheet.png', 8, escala=2)

# --- DECORATIVOS ---
class Cloud:
    def __init__(self):
        self.image = cloud_img
        self.rect = self.image.get_rect()
        self.rect.bottom = ALTURA
        self.tiles = []
        num_tiles = LARGURA // self.rect.width + 2
        for i in range(num_tiles):
            tile_rect = self.image.get_rect()
            tile_rect.x = i * tile_rect.width
            tile_rect.bottom = ALTURA
            self.tiles.append(tile_rect)

    def update(self, dt):
        pass

    def draw(self, tela):
        for tile_rect in self.tiles:
            tela.blit(self.image, tile_rect)

class Moon:
    def __init__(self):
        self.image = moon_img
        self.base_size = 60
        self.scale = 1
        self.growing = True

    def update(self, dt):
        if self.growing:
            self.scale += 0.5 * dt
            if self.scale >= 1.3:
                self.growing = False
        else:
            self.scale -= 0.5 * dt
            if self.scale <= 0.8:
                self.growing = True

    def draw(self, tela):
        size = int(self.base_size * self.scale)
        resized = pygame.transform.scale(self.image, (size, size))
        tela.blit(resized, (LARGURA - size - 20, 20))

# --- TELAS INICIAIS ---
def tela_input_nome():
    nome = ""
    ativo = True
    while ativo:
        tela.fill(COR_FUNDO)
        msg = font_title.render("Digite seu nome:", True, COR_TEXT)
        entrada = font_title.render(nome, True, (100, 255, 100))
        tela.blit(msg, (LARGURA // 2 - msg.get_width() // 2, 200))
        tela.blit(entrada, (LARGURA // 2 - entrada.get_width() // 2, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome.strip():
                    ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 12 and evento.unicode.isprintable():
                        nome += evento.unicode
        clock.tick(FPS)
    return nome

def tela_boas_vindas(nome):
    botao = pygame.Rect(LARGURA // 2 - 120, 400, 240, 60)
    esperando = True
    while esperando:
        tela.fill(COR_FUNDO)
        boas = font_title.render(f"Bem-vindo, {nome}!", True, COR_TEXT)
        explicacao = font_ui.render("Desvie dos tiros, segure F para atirar, LSHIFT para ESPECIAL.", True, COR_TEXT)
        tela.blit(boas, (LARGURA // 2 - boas.get_width() // 2, 200))
        tela.blit(explicacao, (LARGURA // 2 - explicacao.get_width() // 2, 280))

        pygame.draw.rect(tela, (0, 180, 0), botao)
        txt = font_ui.render("INICIAR PARTIDA", True, COR_TEXT)
        tela.blit(txt, (botao.centerx - txt.get_width() // 2, botao.centery - txt.get_height() // 2))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(evento.pos):
                    esperando = False
        clock.tick(FPS)


# Player tiro
player_tiro_frames = carregar_frames('Recursos/imagens/tiro_sheet.png', 8)

# Boss tiros (maiores)
boss_tiro1_frames = carregar_frames('Recursos/imagens/tiro1_sheet.png', 8, escala=2)
boss_tiro2_frames = carregar_frames('Recursos/imagens/tiro2_sheet.png', 8, escala=2)
boss_tiro3_frames = carregar_frames('Recursos/imagens/tiro3_sheet.png', 8, escala=2)

# --- DECORATIVOS ---
class Cloud:
    def __init__(self):
            self.image = cloud_img
            self.height = self.image.get_height()
            self.rect = self.image.get_rect()
            self.rect.bottom = ALTURA  # fica colada embaixo
            self.tiles = []

            # Calcula quantos blocos precisa para cobrir a tela toda
            num_tiles = LARGURA // self.rect.width + 2
            for i in range(num_tiles):
                tile_rect = self.image.get_rect()
                tile_rect.x = i * tile_rect.width
                tile_rect.bottom = ALTURA
                self.tiles.append(tile_rect)

    def update(self, dt):
            pass  # não faz nada, é fixa

    def draw(self, tela):
            for tile_rect in self.tiles:
                tela.blit(self.image, tile_rect)

class Moon:
    def __init__(self):
        self.image = moon_img
        self.base_size = 50
        self.scale = 1
        self.growing = True

    def update(self, dt):
        if self.growing:
            self.scale += 0.5 * dt
            if self.scale >= 1.2:
                self.growing = False
        else:
            self.scale -= 0.5 * dt
            if self.scale <= 0.8:
                self.growing = True

    def draw(self, tela):
        size = int(self.base_size * self.scale)
        resized = pygame.transform.scale(self.image, (size, size))
        tela.blit(resized, (LARGURA - size - 10, 10))

# --- TIROS ---
class TiroAnimado:
    def __init__(self, frames, x, y, speed=600, direcao=1, vel_y=0):
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.anim_speed = 15
        self.direcao = direcao
        self.vel_y = vel_y

    def update(self, dt):
        self.rect.x += self.speed * dt * self.direcao
        self.rect.y += self.vel_y * dt
        self.index += self.anim_speed * dt
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def draw(self, tela):
        tela.blit(self.image, self.rect)

class BossTiroAnimado:
    def __init__(self, frames, x, y, vel_x, vel_y):
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.anim_speed = 12

    def update(self, dt):
        self.rect.x -= self.vel_x * dt
        self.rect.y += self.vel_y * dt
        self.index += self.anim_speed * dt
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def draw(self, tela):
        tela.blit(self.image, self.rect)

# --- PLAYER ---
class Player:
    def __init__(self):
        self.img = player_img
        self.rect = self.img.get_rect(center=(100, ALTURA // 2))
        self.velocidade = 6
        self.vidas = 3
        self.projeteis = []
        self.poder_especial = 0
        self.carregando_especial = False
        self.direcao_y = 0
        self.atirando = False
        self.tempo_ultimo_tiro = 0

    def mover(self, teclas):
        self.direcao_y = 0
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
            self.direcao_y = -1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade
            self.direcao_y = 1
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))

    def atirar(self):
        tiro = TiroAnimado(player_tiro_frames, self.rect.right, self.rect.centery, vel_y=self.direcao_y * 200)
        self.projeteis.append(tiro)

    def carregar_especial(self):
        self.carregando_especial = True
        self.poder_especial = min(100, self.poder_especial + 2)

    def parar_carga(self):
        self.carregando_especial = False

    def atirar_especial(self):
        if self.poder_especial >= 100:
            for offset in [-20, 0, 20]:
                tiro = TiroAnimado(player_tiro_frames, self.rect.right, self.rect.centery + offset, vel_y=self.direcao_y * 200)
                self.projeteis.append(tiro)
            self.poder_especial = 0

    def desenhar(self, tela):
        tela.blit(self.img, self.rect)

# --- BOSS ---
class Boss:
    def __init__(self, player):
        self.img_original = boss_img
        self.img = boss_img.copy()
        self.rect = self.img.get_rect()
        self.rect.right = LARGURA
        self.rect.centery = ALTURA // 2
        self.vida_maxima = 2000  # mais vida!
        self.vida = self.vida_maxima
        self.projeteis = []
        self.tempo_ultimo_ataque = 0
        self.flash_timer = 0
        self.player = player

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0
        self.flash_timer = 0.1

    def atualizar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_ataque > 2000:
            ataque = random.choice(['energia', 'onda', 'fragmentos'])
            self.atacar_mirando(ataque)
            self.tempo_ultimo_ataque = tempo_atual

        if self.flash_timer > 0:
            self.flash_timer -= 1/60
            self.img = self.img_original.copy()
            self.img.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
        else:
            self.img = self.img_original.copy()

    def atacar_mirando(self, tipo):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        vel_x = abs(300 * (dx / dist))
        vel_y = 300 * (dy / dist)

        frames = boss_tiro1_frames if tipo == 'energia' else boss_tiro2_frames if tipo == 'onda' else boss_tiro3_frames
        proj = BossTiroAnimado(frames, self.rect.left, self.rect.centery, vel_x, vel_y)
        self.projeteis.append(proj)

    def esta_morto(self):
        return self.vida <= 0

    def desenhar(self, tela):
        tela.blit(self.img, self.rect)


# --- GAME ---
class Game:
    def __init__(self):
        self.player = Player()
        self.boss = Boss(self.player)
        self.cloud = Cloud()
        self.moon = Moon()
        self.pontuacao = 0
        self.bg_x1 = 0
        self.bg_x2 = LARGURA
        self.velocidade_fundo = 2
        self.pausado = False
        self.font = pygame.font.SysFont(None, 32)
        self.tempo_inicio = pygame.time.get_ticks()
        self.proximidade_bonus = 0
        self.vida_frame_index = 0
        self.vida_anim_speed = 8  # frames por segundo
        self.vida_anim_timer = 0

    def atualizar_fundo(self):
        self.bg_x1 -= self.velocidade_fundo
        self.bg_x2 -= self.velocidade_fundo
        if self.bg_x1 <= -LARGURA:
            self.bg_x1 = LARGURA
        if self.bg_x2 <= -LARGURA:
            self.bg_x2 = LARGURA

    def atualizar_jogo(self, dt):
        if self.pausado:
            return

        self.atualizar_fundo()
        self.cloud.update(dt)
        self.moon.update(dt)
        self.boss.atualizar()

        if self.player.atirando:
            if pygame.time.get_ticks() - self.player.tempo_ultimo_tiro > 150:
                self.player.atirar()
                self.player.tempo_ultimo_tiro = pygame.time.get_ticks()

        for proj in self.boss.projeteis:
            dist = abs(proj.rect.centerx - self.player.rect.centerx)
            if dist < 100:
                self.proximidade_bonus += dt * 10

        for tiro in self.player.projeteis[:]:
            tiro.update(dt)
            if tiro.rect.left > LARGURA:
                self.player.projeteis.remove(tiro)
            elif tiro.rect.colliderect(self.boss.rect):
                self.boss.receber_dano(10)
                self.pontuacao += 20
                self.player.projeteis.remove(tiro)

        for proj in self.boss.projeteis[:]:
            proj.update(dt)
            if proj.rect.right < 0 or proj.rect.top < 0 or proj.rect.bottom > ALTURA:
                self.boss.projeteis.remove(proj)
            elif proj.rect.colliderect(self.player.rect):
                self.player.vidas -= 1
                self.boss.projeteis.remove(proj)

    def desenhar(self):
        tela.blit(background, (self.bg_x1, 0))
        tela.blit(background, (self.bg_x2, 0))

        self.boss.desenhar(tela)
        self.cloud.draw(tela)
        self.player.desenhar(tela)
        self.moon.draw(tela)

        for tiro in self.player.projeteis:
            tiro.draw(tela)
        for proj in self.boss.projeteis:
            proj.draw(tela)

        # Atualiza animação da moldura
        self.vida_anim_timer += 1
        if self.vida_anim_timer >= FPS // self.vida_anim_speed:
            self.vida_anim_timer = 0
            self.vida_frame_index = (self.vida_frame_index + 1) % NUM_FRAMES_VIDA

        # Escolhe rosto baseado na vida
        if self.player.vidas >= 3:
            rosto = rosto_feliz
        elif self.player.vidas == 2:
            rosto = rosto_medio
        else:
            rosto = rosto_ferido

        # Posição HUD
        pos_x = 20
        pos_y = ALTURA - FRAME_ALTURA - 20

        # Desenha rosto centralizado dentro do frame
        rosto_x = pos_x + (FRAME_LARGURA - ROSTO_SIZE[0]) // 2
        rosto_y = pos_y + (FRAME_ALTURA - ROSTO_SIZE[1]) // 2
        tela.blit(rosto, (rosto_x, rosto_y))

        # Desenha moldura animada por cima
        tela.blit(frames_vida[self.vida_frame_index], (pos_x, pos_y))

        # Número de vidas e score
        vidas_txt = self.font.render(f"x{self.player.vidas}", True, (255, 255, 255))
        tela.blit(vidas_txt, (pos_x + FRAME_LARGURA + 10, pos_y + FRAME_ALTURA // 2 - 10))
        pontos = self.font.render(f"Pontos: {int(self.pontuacao)}", True, (255, 255, 255))
        tela.blit(pontos, (20, 20))

        if self.pausado:
            pause_text = self.font.render("PAUSADO", True, (255, 0, 0))
            tela.blit(pause_text, (LARGURA // 2 - pause_text.get_width() // 2, ALTURA // 2))

        pygame.display.flip()



    def salvar_log(self, pontuacao):
        agora = datetime.datetime.now()
        data_str = agora.strftime("%Y-%m-%d")
        hora_str = agora.strftime("%H:%M:%S")
        with open("log.dat", "a") as f:
            f.write(f"{data_str} {hora_str} Pontuação: {int(pontuacao)}\n")

    def mostrar_logs(self):
        tela.fill((0, 0, 0))
        titulo = self.font.render("Últimos 5 Registros:", True, (255, 255, 255))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))

        if os.path.exists("log.dat"):
            with open("log.dat", "r") as f:
                linhas = f.readlines()[-5:]
            for i, linha in enumerate(linhas):
                texto = self.font.render(linha.strip(), True, (255, 255, 255))
                tela.blit(texto, (100, 100 + i * 40))
        else:
            texto = self.font.render("Nenhum registro ainda.", True, (255, 255, 255))
            tela.blit(texto, (100, 100))

        pygame.display.flip()
        pygame.time.wait(5000)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(FPS) / 1000

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.pausado = not self.pausado
                    if not self.pausado:
                        if evento.key == pygame.K_f:
                            self.player.atirando = True
                        if evento.key == pygame.K_LSHIFT:
                            self.player.carregar_especial()
                if evento.type == pygame.KEYUP:
                    if not self.pausado:
                        if evento.key == pygame.K_f:
                            self.player.atirando = False
                        if evento.key == pygame.K_LSHIFT:
                            self.player.parar_carga()
                            self.player.atirar_especial()

            if not self.pausado:
                teclas = pygame.key.get_pressed()
                self.player.mover(teclas)
                self.atualizar_jogo(dt)

            if self.player.vidas <= 0:
                self.fim_de_jogo(False)
            if self.boss.esta_morto():
                self.fim_de_jogo(True)

            self.desenhar()

    def fim_de_jogo(self, venceu):
        tempo_total = (pygame.time.get_ticks() - self.tempo_inicio) / 1000
        self.pontuacao += max(0, (1000 - tempo_total) * 2)
        self.pontuacao += self.proximidade_bonus

        self.salvar_log(int(self.pontuacao))

        tela.fill((0, 0, 0))
        msg = "VOCÊ VENCEU!" if venceu else "VOCÊ PERDEU!"
        texto = self.font.render(msg, True, (255, 255, 255))
        pontos = self.font.render(f"Pontuação final: {int(self.pontuacao)}", True, (255, 255, 255))
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 200))
        tela.blit(pontos, (LARGURA // 2 - pontos.get_width() // 2, 250))

        pygame.display.flip()
        pygame.time.wait(3000)
        self.mostrar_logs()
        pygame.quit()
        sys.exit()


def desenhar(self):
    tela.blit(background, (self.bg_x1, 0))
    tela.blit(background, (self.bg_x2, 0))

    # 1) Boss primeiro
    self.boss.desenhar(tela)

    # 2) Nuvem por cima do boss
    self.cloud.draw(tela)

    # 3) Player por cima de tudo
    self.player.desenhar(tela)

    # 4) Lua decorativa por cima
    self.moon.draw(tela)

    # 5) Tiros (player e boss)
    for tiro in self.player.projeteis:
        tiro.draw(tela)
    for proj in self.boss.projeteis:
        proj.draw(tela)

    # HUD
    vidas = self.font.render(f"Vidas: {self.player.vidas}", True, (255, 255, 255))
    pontos = self.font.render(f"Pontos: {int(self.pontuacao)}", True, (255, 255, 255))
    pause = self.font.render("Espaço: Pausar | F: Atirar", True, (255, 255, 255))
    tela.blit(vidas, (10, 10))
    tela.blit(pontos, (10, 40))
    tela.blit(pause, (LARGURA - pause.get_width() - 10, 10))

    if self.pausado:
        pause_text = self.font.render("PAUSADO", True, (255, 0, 0))
        tela.blit(pause_text, (LARGURA // 2 - pause_text.get_width() // 2, ALTURA // 2))

    pygame.display.flip()

    def salvar_log(self, pontuacao):
        agora = datetime.datetime.now()
        data_str = agora.strftime("%Y-%m-%d")
        hora_str = agora.strftime("%H:%M:%S")
        with open("log.dat", "a") as f:
            f.write(f"{data_str} {hora_str} Pontuação: {pontuacao}\n")

    def mostrar_logs(self):
        tela.fill((0, 0, 0))
        titulo = self.font.render("Últimos 5 Registros:", True, (255, 255, 255))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))

        if os.path.exists("log.dat"):
            with open("log.dat", "r") as f:
                linhas = f.readlines()[-5:]
            for i, linha in enumerate(linhas):
                texto = self.font.render(linha.strip(), True, (255, 255, 255))
                tela.blit(texto, (100, 100 + i * 40))
        else:
            texto = self.font.render("Nenhum registro ainda.", True, (255, 255, 255))
            tela.blit(texto, (100, 100))

        pygame.display.flip()
        pygame.time.wait(5000)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(FPS) / 1000

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.pausado = not self.pausado
                    if not self.pausado:
                        if evento.key == pygame.K_f:
                            self.player.atirando = True
                        if evento.key == pygame.K_LSHIFT:
                            self.player.carregar_especial()
                if evento.type == pygame.KEYUP:
                    if not self.pausado:
                        if evento.key == pygame.K_f:
                            self.player.atirando = False
                        if evento.key == pygame.K_LSHIFT:
                            self.player.parar_carga()
                            self.player.atirar_especial()

            if not self.pausado:
                teclas = pygame.key.get_pressed()
                self.player.mover(teclas)
                self.atualizar_jogo(dt)

            if self.player.vidas <= 0:
                self.fim_de_jogo(False)
            if self.boss.esta_morto():
                self.fim_de_jogo(True)

            self.desenhar()

    def fim_de_jogo(self, venceu):
        tempo_total = (pygame.time.get_ticks() - self.tempo_inicio) / 1000
        self.pontuacao += max(0, (1000 - tempo_total) * 2)
        self.pontuacao += self.proximidade_bonus

        self.salvar_log(int(self.pontuacao))

        tela.fill((0, 0, 0))
        msg = "VOCÊ VENCEU!" if venceu else "VOCÊ PERDEU!"
        texto = self.font.render(msg, True, (255, 255, 255))
        pontos = self.font.render(f"Pontuação final: {int(self.pontuacao)}", True, (255, 255, 255))
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 200))
        tela.blit(pontos, (LARGURA // 2 - pontos.get_width() // 2, 250))

        pygame.display.flip()
        pygame.time.wait(3000)
        self.mostrar_logs()
        pygame.quit()
        sys.exit()

# --- INICIAR ---
if __name__ == "__main__":
    nome = tela_input_nome()
    tela_boas_vindas(nome)
    jogo = Game()
    jogo.run()
