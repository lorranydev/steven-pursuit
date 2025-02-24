import pygame
import random
import sys
import math

#colores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
roxinho = (180, 176, 225)
verde_agua = (109, 225, 209)
azul_melodia_suave = (212, 234, 250)
lavanda = (185,168,248)
azul_ceu = (53,94,182)
azulzinho = (61,175,237)

#variáveis
LARGURA_TELA = 900
ALTURA_TELA = 700
chao_y = 675
chao_altura = 100
raio_perso = 20
perso_x = 100
perso_y = chao_y - raio_perso
velocidade_y = 0
gravidade = 0.5
velocidade_x = 2
dist_min_obs = 160  

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("msc_tema.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)  # Volume entre 0.0 e 1.0

screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Steven Pursuit - Racing Game")
clock = pygame.time.Clock()

#fontes - não de água, nem de energia -
crewni = pygame.font.Font("crewni.ttf", 25)
crystal = pygame.font.Font("crystal.ttf", 25)
regcrystal = pygame.font.Font("regcrystal.ttf", 25)


#fundos 
fundo = pygame.image.load("fundo_loop.jpg")
fundo_tela_inicial = pygame.image.load("tela_inicial.jpg")
fundo_tela_inicial = pygame.transform.scale(fundo_tela_inicial, (LARGURA_TELA, ALTURA_TELA))
orig_largura, orig_altura = fundo.get_size()
escala = ALTURA_TELA / orig_altura
nova_largura = int(orig_largura * escala)
fundo = pygame.transform.scale(fundo, (nova_largura, ALTURA_TELA))
fundo_x = 0
velocidade_fundo = 2

#img obstaculo
img_obstaculo = pygame.image.load("obstaculo.png")
#!!obstaculo_img = pygame.transform.scale(obstaculo_img, (50, 50))  # ajuste conforme necessário

#steven
tam_steven = (125, 125)
frames_steven = [
    pygame.transform.scale(pygame.image.load("1.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("2.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("3.png"), tam_steven),
]
frame_atual = 0
tempo_entre_frames = 100  #milissegundos
ultimo_tempo = pygame.time.get_ticks()
altura_personagem = frames_steven[frame_atual].get_height()


#funções
def checa_colisao(perso_x, perso_y, raio_perso, obstaculo_x, obstaculo_y, raio_obstaculo):
    distancia = math.sqrt((obstaculo_x - perso_x) ** 2 + (obstaculo_y - perso_y) ** 2)
    return distancia <= (raio_perso + raio_obstaculo)
def checa_colisao_retangulos(perso_x, perso_y, personagem_img, obstaculo_x, obstaculo_y, obstaculo_img):
    personagem_rect = personagem_img.get_rect(topleft=(perso_x, perso_y))
    personagem_rect = personagem_rect.inflate(-personagem_rect.width * 0.35, -personagem_rect.height * 0.3)
    
    obstaculo_rect = obstaculo_img.get_rect(center=(obstaculo_x, obstaculo_y))
    obstaculo_rect = obstaculo_rect.inflate(-obstaculo_rect.width * 0.35, -obstaculo_rect.height * 0.3)
    
    return personagem_rect.colliderect(obstaculo_rect)

def exibe_texto(texto, cor, x, y, fonte="fonte.ttf", tam=25): 
    fonte = pygame.font.Font(fonte, tam)  
    texto_surface = fonte.render(texto, True, cor)
    screen.blit(texto_surface, (x, y))




def desenha_img_obstaculo(x, y):
#    pygame.draw.circle(screen, lavanda, (x, y), raio)
    largura, altura = img_obstaculo.get_size()
    screen.blit(img_obstaculo, (x - largura // 2, y - altura // 2))

def jogo():
    global perso_x, perso_y, velocidade_y, fundo_x, frame_atual, ultimo_tempo
    perso_y = chao_y - frames_steven[0].get_height()

    obstaculos = []
    pontuacao = 0

    fase2_mostrada = False  
    tempo_fase2 = 0 
    fase2_ativa = False


    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and perso_x > 0:
            perso_x -= velocidade_x
        if teclas[pygame.K_RIGHT] and perso_x < LARGURA_TELA - raio_perso:
            perso_x += velocidade_x
        if teclas[pygame.K_UP] and perso_y + frames_steven[frame_atual].get_height() >= chao_y:
            velocidade_y = -12


        velocidade_y += gravidade
        perso_y += velocidade_y

        altura_personagem = frames_steven[frame_atual].get_height()  # Obtém a altura do frame atual
        if perso_y + altura_personagem >= chao_y:
            perso_y = chao_y - altura_personagem
            velocidade_y = 0


        agora = pygame.time.get_ticks()
        if agora - ultimo_tempo > tempo_entre_frames:
            frame_atual = (frame_atual + 1) % len(frames_steven)
            ultimo_tempo = agora


        if fase2_ativa:
            chance = 1.5  # Aumenta a chance de gerar obstáculos (3% por frame)
            velocidade_obstaculo = 6  # Obstáculos ficam mais rápidos
        else:
            chance = 1  # Chance normal (1% por frame)
            velocidade_obstaculo = 5

        if random.randint(1, 100) <= chance:
            if not obstaculos or (LARGURA_TELA - obstaculos[-1][0] >= dist_min_obs):
                obstaculo_x = LARGURA_TELA
                obstaculo_y = chao_y - 25
                obstaculos.append([obstaculo_x, obstaculo_y])

        for obs in obstaculos:
            obs[0] -= velocidade_obstaculo 


        for obstaculo_x, obstaculo_y in obstaculos:
            if checa_colisao_retangulos(perso_x, perso_y, frames_steven[frame_atual], obstaculo_x, obstaculo_y, img_obstaculo):
                exibe_texto("Colisão!", PRETO, LARGURA_TELA // 3, ALTURA_TELA // 2, "crewni.ttf", 20)                
                pygame.display.update()
                pygame.time.delay(1500)
                tela_inicial()
        
        obstaculos = [obs for obs in obstaculos if obs[0] > 0]

        fundo_x -= velocidade_fundo

        if fundo_x <= -nova_largura:
            fundo_x = 0

        screen.blit(fundo, (fundo_x, 0))
        screen.blit(fundo, (fundo_x + nova_largura, 0))

        pygame.draw.rect(screen, azul_melodia_suave, (0, chao_y, LARGURA_TELA, chao_altura))

        screen.blit(frames_steven[frame_atual], (perso_x, int(perso_y)))


        for obstaculo_x, obstaculo_y in obstaculos:
            desenha_img_obstaculo(obstaculo_x, obstaculo_y)

        pontuacao += 1
        exibe_texto(f"Pontuação: {pontuacao}", lavanda, 10, 10, "crewni.ttf", 20)    

        if pontuacao >= 1500 and not fase2_ativa:
            fase2_ativa = True
            fase2_mostrada = True
            tempo_fase2 = pygame.time.get_ticks()

        if fase2_mostrada:
            screen.blit(crewni.render("Fase 2!", True, (255, 255, 255)), (LARGURA_TELA // 2 - 50, 100))

            if pygame.time.get_ticks() - tempo_fase2 > 2000:
                fase2_mostrada = False



        pygame.display.update()
        clock.tick(60)

    tela_inicial()

def tela_inicial():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogo()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_i:
                    tela_instruções()
                    return
                elif evento.key == pygame.K_c:
                    tela_créditos()
                    return

        screen.blit(fundo_tela_inicial, (0, 0))
        exibe_texto("Steven Pursuit", azul_ceu, LARGURA_TELA // 3-240, ALTURA_TELA // 3, "crystal.ttf", 45)
        exibe_texto("pressione espaco para jogar", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+20, "regcrystal.ttf", 25)
        exibe_texto("pressione i para instruções", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+70, "regcrystal.ttf", 25)
        exibe_texto("pressione c para créditos", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+100, "regcrystal.ttf", 25)

        pygame.display.update()
        clock.tick(30)

def tela_instruções():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogo()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_m:
                    tela_inicial()
                    return   

        screen.fill(PRETO)
        exibe_texto("Como Jogar?", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3-20, "crewni.ttf", 25)
        exibe_texto("Use as setas do teclado", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+40, "crewni.ttf", 25)
        exibe_texto("Evite os obstáculos", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+80, "crewni.ttf", 25)
        exibe_texto("Pressione 'Espaço' para Jogar", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+150, "crewni.ttf", 25)
        exibe_texto("Pressione 'M' para ir ao Menu", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+190, "crewni.ttf", 25)
        exibe_texto("Pressione 'ESC' para Sair", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+220, "crewni.ttf", 25)
        pygame.display.update()
        clock.tick(30)

def tela_créditos():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogo()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_m:
                    tela_inicial()
                    return   

        screen.fill(PRETO)
        exibe_texto("Créditos", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3-20, "crystal.ttf", 30)
        exibe_texto("Desenvolvedora: Lorrany ^^", lavanda, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+50, "crystal.ttf", 35)
        exibe_texto("Pressione 'M' para ir ao Menu", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+150, "crewni.ttf", 25)

        pygame.display.update()
        clock.tick(30)

def tela_endgame():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogo()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_m:
                    tela_inicial()
                    return   
                elif evento.key == pygame.K_p:
                    jogo()
                    return       

        screen.fill(PRETO)
        exibe_texto("Bom trabalho!!", lavanda, LARGURA_TELA // 3 -40, ALTURA_TELA // 3-20, "crystal.ttf", 40)
        exibe_texto("Pressione 'Espaço' para Jogar Novamente", azul_melodia_suave, LARGURA_TELA // 3 -40, ALTURA_TELA // 3+20, "crewni.ttf", 25)

        pygame.display.update()
        clock.tick(30)

tela_inicial()
pygame.quit()