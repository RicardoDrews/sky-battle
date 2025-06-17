from Recursos.config import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Sky Battle")
        self.clock = pygame.time.Clock()


background = pygame.image.load('Recursos/imagens/background.png').convert()
background = pygame.transform.scale(background, (LARGURA_TELA, ALTURA_TELA))

player_img = pygame.image.load('Recursos/imagens/aviao.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_LARGURA, PLAYER_ALTURA))

boss_img = pygame.image.load('Recursos/imagens/boss.png').convert_alpha()
boss_img = pygame.transform.scale(boss_img, (BOSS_LARGURA, BOSS_ALTURA))

cloud_img = pygame.image.load('Recursos/imagens/nuvem.png').convert_alpha()
moon_img = pygame.image.load('Recursos/imagens/lua.png').convert_alpha()

rosto_feliz = pygame.image.load('Recursos/imagens/rosto_feliz.png').convert_alpha()
rosto_medio = pygame.image.load('Recursos/imagens/rosto_machucado.png').convert_alpha()
rosto_ferido = pygame.image.load('Recursos/imagens/rosto_muito_machucado.png').convert_alpha()

ROSTO_SIZE = (FRAME_LARGURA - 10, FRAME_ALTURA - 10)
rosto_feliz = pygame.transform.scale(rosto_feliz, ROSTO_SIZE)
rosto_medio = pygame.transform.scale(rosto_medio, ROSTO_SIZE)
rosto_ferido = pygame.transform.scale(rosto_ferido, ROSTO_SIZE)

vida_sheet = pygame.image.load('Recursos/imagens/vida.PNG').convert_alpha()

NUM_FRAMES_VIDA = 4 
FRAME_LARGURA = vida_sheet.get_width() // NUM_FRAMES_VIDA
FRAME_ALTURA = vida_sheet.get_height()

frames_vida = []
for i in range(NUM_FRAMES_VIDA):
    frame = vida_sheet.subsurface(pygame.Rect(i * FRAME_LARGURA, 0, FRAME_LARGURA, FRAME_ALTURA))
    frames_vida.append(frame)

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


def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


if __name__ == "__main__":
    game = Game()
    game.run()