import pygame
import random

#colores
PRETO = (0,0,0)
branco = (255,255,255)

#paleta 1 (principal)
azul_melodia_suave = (212,234,250)
azul_ceu = (53,94,182)
azul_azul = (61,175,237)
azul_mirtilo = (57,121,195)
lavanda = (185,168,248)
#paleta 2 (creditos)
rosa = (242,121,153)
rosa_claro = (242,187,201)
salmão = (242,137,114)
açaí = (166,96,122)
magenta = (166,86,145)
#paleta 3 (instrucoes)
rosa_seco = (242,148,173)
roxo = (115,47,91)
roxo_tom_claro = (203, 83, 161)
verde = (90,140,126)
verde_peridot = (196,242,208)
#paleta 4 (derrota)
amarelo = (242, 208, 145)
rosa_vermelho = (242, 107, 131)
rosa_bege = (242, 178, 172)
cinza_roxo = (134, 121, 140)
#paleta 5 (win1)
amarelo_ouro = (255, 239, 155)
marrom = (64, 44, 40)
milkshake_de_acai = (107, 79, 98)
rosa_salmao = (242, 144, 184)
vitamina_de_abacate = (216, 217, 180)
#paleta 6 (niveis)
amarelo_niveis = (242, 203, 87)
rosa_niveis = (239, 44, 149)

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
dist_min_obs = 250  
pontuacao = 0
nivel = 0

pygame.init()
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Steven Pursuit")
clock = pygame.time.Clock()

#audio
pygame.mixer.init()
pygame.mixer.music.load("msc_tema.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)
gameoversound = pygame.mixer.Sound("gameover.ogg")
jumpsound = pygame.mixer.Sound("jump.ogg")

#fontes
crewni = pygame.font.Font("crewni.ttf", 85)
crystal = pygame.font.Font("crystal.ttf", 55)
regcrystal = pygame.font.Font("regcrystal.ttf", 55)

#fundos
fundo = pygame.image.load("fundo_loop.jpg")
fundo_tela_inicial = pygame.image.load("tela_inicial.jpg")
fundo_tela_creditos = pygame.image.load("tela_creditos.jpg")
fundo_tela_intro = pygame.image.load("tela_intro.png")
fundo_tela_intro_2 = pygame.image.load("tela_intro_2.png")
fundo_tela_derrota = pygame.image.load("tela_derrota.png")
fundo_tela_win1 = pygame.image.load("tela_win1.png")
fundo_tela_niveis = pygame.image.load("tela_niveis.jpg")
fundo_tela_inicial = pygame.transform.scale(fundo_tela_inicial, (LARGURA_TELA, ALTURA_TELA))
fundo_tela_creditos= pygame.transform.scale(fundo_tela_creditos, (LARGURA_TELA, ALTURA_TELA))
fundo_tela_intro = pygame.transform.scale(fundo_tela_intro, (LARGURA_TELA, ALTURA_TELA))
fundo_tela_intro_2 = pygame.transform.scale(fundo_tela_intro_2, (LARGURA_TELA, ALTURA_TELA))
fundo_tela_derrota = pygame.transform.scale(fundo_tela_derrota, (LARGURA_TELA, ALTURA_TELA))
fundo_tela_win1 = pygame.transform.scale(fundo_tela_win1, (LARGURA_TELA, ALTURA_TELA))
fundo_tela_niveis = pygame.transform.scale(fundo_tela_niveis, (LARGURA_TELA, ALTURA_TELA))

orig_largura, orig_altura = fundo.get_size()
escala = ALTURA_TELA / orig_altura
nova_largura = int(orig_largura * escala)
fundo = pygame.transform.scale(fundo, (nova_largura, ALTURA_TELA))
fundo_x = 0
velocidade_fundo = 2

#imagens
img_obstaculo = pygame.image.load("obstaculo.png")
setas = pygame.image.load("setas.png")
tam_setas = (110, 110)
img_setas = pygame.transform.scale(setas, tam_setas)
tam_bisc_gat = (100, 225)

#steven
tam_steven = (120, 120)
frames_steven = [
    pygame.transform.scale(pygame.image.load("1.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("2.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("3.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("4.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("5.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("6.png"), tam_steven),
    pygame.transform.scale(pygame.image.load("7.png"), tam_steven),

]
frame_atual = 0
tempo_entre_frames = 85  #milissegundos
ultimo_tempo = pygame.time.get_ticks()
altura_personagem = frames_steven[frame_atual].get_height()

#funções
def fade_out(screen, color=PRETO, speed=10):
    fade = pygame.Surface(screen.get_size())
    fade.fill(color)
    for alpha in range(0, 255, speed):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(30) 

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
    largura, altura = img_obstaculo.get_size()
    screen.blit(img_obstaculo, (x - largura // 2, y - altura // 2))

def tela_inicial():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    fade_out(screen, rosa_niveis)
                    tela_niveis()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_i:
                    fade_out(screen)
                    tela_intro()
                    return
                elif evento.key == pygame.K_c:
                    fade_out(screen, rosa_seco)
                    tela_creditos()
                    return

        screen.blit(fundo_tela_inicial, (0, 0))
        exibe_texto("Steven Pursuit", azul_ceu, LARGURA_TELA // 3-205, ALTURA_TELA // 3-150, "crystal.ttf", 50)
        exibe_texto("pressione espaco para jogar", azul_ceu, LARGURA_TELA // 3 -140, ALTURA_TELA // 3-15, "regcrystal.ttf", 25)
        exibe_texto("I para instrucoes", azul_melodia_suave, LARGURA_TELA // 3 -8, ALTURA_TELA // 3+350, "crystal.ttf", 25)
        exibe_texto("C para créditos", azul_melodia_suave, LARGURA_TELA // 3 -9, ALTURA_TELA // 3+405, "crystal.ttf", 25)

        pygame.display.update()
        clock.tick(30)

def tela_niveis():
    global nivel
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_KP_1 or evento.key == pygame.K_1:
                    nivel = 1
                    fade_out(screen, azul_melodia_suave)
                    jogo()
                    return
                elif evento.key == pygame.K_KP_2 or evento.key == pygame.K_2:
                    nivel = 2
                    fade_out(screen, azul_melodia_suave)
                    jogo()
                    return
                elif evento.key == pygame.K_KP_3 or evento.key == pygame.K_3:
                    nivel = 3
                    fade_out(screen, azul_melodia_suave)
                    jogo()
                    return
                elif evento.key == pygame.K_m:
                    fade_out(screen, lavanda)
                    tela_inicial()
                    return   
      

        screen.blit(fundo_tela_niveis, (0, 0))
        exibe_texto("Escolha o nivel", amarelo_niveis, 35, 50, "regcrystal.ttf", 40)
        exibe_texto("Pressione 1, 2 ou 3", amarelo_niveis, 60, 175, "crewni.ttf", 40)

        exibe_texto("1", amarelo_niveis, 251, 300, "crewni.ttf", 50)
        exibe_texto("2", amarelo_niveis, 250, 410, "crewni.ttf", 50)
        exibe_texto("3", amarelo_niveis, 250, 520, "crewni.ttf", 50)


        pygame.display.update()
        clock.tick(30)

def jogo():
    global perso_x, perso_y, velocidade_y, fundo_x, frame_atual, ultimo_tempo, pontuacao, nivel
    perso_x = 50
    perso_y = chao_y - frames_steven[0].get_height()
    velocidade_y = 0

    obstaculos = []
    pontuacao = 0

    fase1_mostrada = False  
    tempo_fase1 = 0 
    fase1_ativa = False

    fase2_mostrada = False  
    tempo_fase2 = 0 
    fase2_ativa = False

    fase3_mostrada = False  
    tempo_fase3 = 0 
    fase3_ativa = False

    fase4_mostrada = False  
    tempo_fase4 = 0 
    fase4_ativa = False

    fase5_mostrada = False  
    tempo_fase5 = 0 
    fase5_ativa = False

    fase6_mostrada = False  
    tempo_fase6 = 0 
    fase6_ativa = False

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
            jumpsound.play() 
            jumpsound.set_volume(0.15)


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


        if fase6_ativa:
            chance = 6 
            velocidade_obstaculo = 7 
        elif fase5_ativa:
            chance = 5 
            velocidade_obstaculo = 7  
        elif fase4_ativa:
            chance = 4 
            velocidade_obstaculo = 6.5   
        elif fase3_ativa:
            chance = 3 
            velocidade_obstaculo = 6  
        elif fase2_ativa:
            chance = 2
            velocidade_obstaculo = 5.5
        elif fase1_ativa:
            chance = 1
            velocidade_obstaculo = 5
        else:
            chance = 1  # Chance normal (1% por frame)
            velocidade_obstaculo = 4.75


        if random.randint(1, 100) <= chance:
            if not obstaculos or (LARGURA_TELA - obstaculos[-1][0] >= dist_min_obs):
                obstaculo_x = LARGURA_TELA
                obstaculo_y = chao_y - 25
                obstaculos.append([obstaculo_x, obstaculo_y])

        for obs in obstaculos:
            obs[0] -= velocidade_obstaculo 


        for obstaculo_x, obstaculo_y in obstaculos:
            if checa_colisao_retangulos(perso_x, perso_y, frames_steven[frame_atual], obstaculo_x, obstaculo_y, img_obstaculo):
                #exibe_texto("Colisão!", PRETO, LARGURA_TELA // 3, ALTURA_TELA // 2, "crewni.ttf", 20)  
                pygame.mixer.music.set_volume(0.055)              
                gameoversound.play() 
                pygame.display.update()
                pygame.time.delay(1000)
                pygame.mixer.music.set_volume(0.15)        
                fade_out(screen, amarelo)
                tela_derrota()
        
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
        exibe_texto(f"Score: {pontuacao}", lavanda, 10, 10, "crewni.ttf", 20)    


        #niveis
        if nivel == 1 and pontuacao >= 6000:
                pygame.mixer.music.stop() 
                pygame.mixer.music.load("msc_win.ogg")  
                pygame.mixer.music.play(-1) 
                pygame.mixer.music.set_volume(0.15)
                fade_out(screen, rosa_salmao,10)
                pygame.display.update()
                tela_win1()       
                return
        if nivel == 2 and pontuacao >= 7500:
                pygame.mixer.music.stop() 
                pygame.mixer.music.load("msc_win.ogg")  
                pygame.mixer.music.play(-1) 
                pygame.mixer.music.set_volume(0.15)
                fade_out(screen, rosa_salmao,10)
                pygame.display.update()
                tela_win1()       
                return
        if nivel == 3 and pontuacao >= 10000:
                pygame.mixer.music.stop() 
                pygame.mixer.music.load("msc_win.ogg")  
                pygame.mixer.music.play(-1) 
                pygame.mixer.music.set_volume(0.15)
                fade_out(screen, rosa_salmao,10)
                pygame.display.update()
                tela_win1()       
                return
        if nivel == 1 and pontuacao >= 150 and pontuacao <=300:    
            exibe_texto("Consiga              de score!", azul_ceu, 160, 295, "regcrystal.ttf", 30)
            exibe_texto("6.000", azul_ceu, 385, 300, "crewni.ttf", 40)
        if nivel == 2 and pontuacao >= 150 and pontuacao <=300:    
            exibe_texto("Consiga              de score!", azul_ceu, 160, 295, "regcrystal.ttf", 30)
            exibe_texto("7.500", azul_ceu, 385, 300, "crewni.ttf", 40)
        if nivel == 3 and pontuacao >= 150 and pontuacao <=300:    
            exibe_texto("Consiga               de score!", azul_ceu, 160, 295, "regcrystal.ttf", 30)
            exibe_texto("10.000", azul_ceu, 383, 300, "crewni.ttf", 40)
   
        #quase la
        if nivel == 1 and pontuacao >= 5000 and pontuacao <=5150:    
            exibe_texto("quase la!", azul_ceu, 315, 295, "crystal.ttf", 35)
        if nivel == 2 and pontuacao >= 6750 and pontuacao <=6900:    
            exibe_texto("quase la!", azul_ceu, 315, 295, "crystal.ttf", 35)
        if nivel == 3 and pontuacao >= 9000 and pontuacao <=9150:    
            exibe_texto("quase la!", azul_ceu, 315, 295, "crystal.ttf", 35)
        
        #fases
        if pontuacao >= 500 and not fase1_ativa:
            fase1_ativa = True
            fase1_mostrada = True
            tempo_fase1 = pygame.time.get_ticks()
        if pontuacao >= 1250 and not fase2_ativa:
            fase2_ativa = True
            fase2_mostrada = True
            tempo_fase2 = pygame.time.get_ticks()
        if pontuacao >= 2250 and not fase3_ativa:
            fase3_ativa = True
            fase3_mostrada = True
            tempo_fase3 = pygame.time.get_ticks()
        if pontuacao >= 3500 and not fase4_ativa:
            fase4_ativa = True
            fase4_mostrada = True
            tempo_fase4 = pygame.time.get_ticks()    
        if pontuacao >= 4500 and not fase5_ativa:
            fase5_ativa = True
            fase5_mostrada = True
            tempo_fase5 = pygame.time.get_ticks()
        if pontuacao >= 6500 and not fase6_ativa:
            fase6_ativa = True
            fase6_mostrada = True
            tempo_fase6 = pygame.time.get_ticks() 
         
        if fase1_mostrada:
            screen.blit(regcrystal.render("Fase", True, azul_melodia_suave), (285, 295))
            screen.blit(crewni.render("1", True, azul_melodia_suave), (580, 290))
            if pygame.time.get_ticks() - tempo_fase1 > 2250:
                fase1_mostrada = False
        if fase2_mostrada:
            screen.blit(regcrystal.render("Fase", True, azul_melodia_suave), (285, 295))
            screen.blit(crewni.render("2", True, azul_melodia_suave), (580, 290))
            if pygame.time.get_ticks() - tempo_fase2 > 2250:
                fase2_mostrada = False
        if fase3_mostrada:
            screen.blit(regcrystal.render("Fase", True, azul_melodia_suave), (285, 295))
            screen.blit(crewni.render("3", True, azul_melodia_suave), (580, 290))           
            if pygame.time.get_ticks() - tempo_fase3 > 2250:
                fase3_mostrada = False
        if fase4_mostrada:
            screen.blit(regcrystal.render("Fase", True, azul_melodia_suave), (285, 295))
            screen.blit(crewni.render("4", True, azul_melodia_suave), (580, 290))
            if pygame.time.get_ticks() - tempo_fase4 > 2250:
                fase4_mostrada = False
        if fase5_mostrada:
            screen.blit(regcrystal.render("Fase", True, azul_melodia_suave), (285, 295))
            screen.blit(crewni.render("5", True, azul_melodia_suave), (580, 290))
            if pygame.time.get_ticks() - tempo_fase5 > 2250:
                fase5_mostrada = False
        if fase6_mostrada:
            screen.blit(regcrystal.render("Fase", True, azul_melodia_suave), (285, 295))
            screen.blit(crewni.render("6", True, azul_melodia_suave), (580, 290))
            if pygame.time.get_ticks() - tempo_fase6 > 2250:
                fase6_mostrada = False        


        pygame.display.update()
        clock.tick(60)

    tela_inicial()

def tela_intro():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    fade_out(screen, rosa_niveis)
                    tela_niveis()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:  
                    fade_out(screen)
                    tela_intro_2()
                    return
                elif evento.key == pygame.K_m:
                    fade_out(screen)
                    tela_inicial()
                    return   

        screen.blit(fundo_tela_intro, (0, 0))
        exibe_texto("O Steven precisa chegar", verde_peridot, 270, 30, "regcrystal.ttf", 28)
        exibe_texto("ao Big Rosquinha para", verde_peridot, 337, 95, "regcrystal.ttf", 28)
        exibe_texto("Comprar biscoito gatinho", verde_peridot, 264, 165, "regcrystal.ttf", 28)
        exibe_texto("pressione enter para continuar *", roxo, 97, 620, "regcrystal.ttf", 25)
        
        pygame.display.update()
        clock.tick(30)

def tela_intro_2():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    fade_out(screen, rosa_niveis)
                    tela_niveis()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_m:
                    fade_out(screen)
                    tela_inicial()
                    return   

        screen.blit(fundo_tela_intro_2, (0, 0))
        exibe_texto("Utilize as setas:", rosa_claro, 240, 75, "regcrystal.ttf", 30)
        screen.blit(img_setas,(395, 145))

        exibe_texto("Nao bata nas pedras!", rosa_claro, 190, 300, "regcrystal.ttf", 30)
        screen.blit(img_obstaculo,(410, 390))

        #exibe_texto("escudos e cachorros-quentes podem ajudar na missão", rosa_claro, 15, 150, "regcrystal.ttf", 25)

        exibe_texto("pressione M para ir ao menu", roxo, 107, 595, "regcrystal.ttf", 30)
        exibe_texto("pressione espaco para Jogar", roxo, 90, 505, "regcrystal.ttf", 30)
        pygame.display.update()
        clock.tick(30)

def tela_creditos():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    fade_out(screen, rosa_niveis)
                    tela_niveis()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_t:
                    fade_out(screen, rosa_seco)
                    tela_beta_testers()  
                    return
                elif evento.key == pygame.K_m:
                    fade_out(screen, rosa_seco)
                    tela_inicial()
                    return   

        screen.blit(fundo_tela_creditos, (0, 0))
        exibe_texto("Créditos", rosa_claro, LARGURA_TELA // 3+85, ALTURA_TELA // 3-160, "crystal.ttf", 45)
        exibe_texto("Desenvolvedora:", açaí , LARGURA_TELA // 3+15, ALTURA_TELA // 3-5, "regcrystal.ttf", 35)
        exibe_texto("Lorrany Silva", açaí, LARGURA_TELA // 3+25, ALTURA_TELA // 3+70, "regcrystal.ttf", 40)
        exibe_texto("orientador:", salmão, LARGURA_TELA // 3+165, ALTURA_TELA // 3+210, "regcrystal.ttf", 20)
        exibe_texto("jorgiano vidal", salmão, LARGURA_TELA // 3+145, ALTURA_TELA // 3+240, "regcrystal.ttf", 20)
        exibe_texto("pressione T para ver a equipe de testes", rosa_claro, LARGURA_TELA // 3 -257, ALTURA_TELA // 3+380, "regcrystal.ttf", 25)

        pygame.display.update()
        clock.tick(30)

def tela_beta_testers():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    fade_out(screen, rosa_niveis)
                    tela_niveis()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_m:
                    fade_out(screen, rosa_seco)
                    tela_inicial()
                    return   

        screen.blit(fundo_tela_creditos, (0, 0))
        exibe_texto("Beta Testers", rosa_claro, LARGURA_TELA // 3+5, ALTURA_TELA // 3-90, "crystal.ttf", 45)
        exibe_texto("Julio Gleison", açaí , LARGURA_TELA // 3+60, ALTURA_TELA // 3+30, "regcrystal.ttf", 35)
        exibe_texto("Leticia Campos", açaí, LARGURA_TELA // 3+55, ALTURA_TELA // 3+115, "regcrystal.ttf", 35)
        exibe_texto("", salmão, LARGURA_TELA // 3+165, ALTURA_TELA // 3+210, "regcrystal.ttf", 20)
        exibe_texto("", salmão, LARGURA_TELA // 3+145, ALTURA_TELA // 3+240, "regcrystal.ttf", 20)
        exibe_texto("pressione M para voltar ao menu", rosa_claro, LARGURA_TELA // 3 -200, ALTURA_TELA // 3+380, "regcrystal.ttf", 25)

        pygame.display.update()
        clock.tick(30)

def tela_derrota():
    global pontuacao
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    fade_out(screen, rosa_niveis)
                    tela_niveis()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_m:
                    fade_out(screen, lavanda)
                    tela_inicial()
                    return   

        screen.blit(fundo_tela_derrota, (0, 0))
  
        exibe_texto("Score", rosa_vermelho, LARGURA_TELA/1.168, ALTURA_TELA/38.888, "regcrystal.ttf", 20)  
        exibe_texto(f"{pontuacao}", rosa_vermelho, LARGURA_TELA/1.125, ALTURA_TELA/12.28, "crewni.ttf", 25)

        exibe_texto("Nao foi dessa vez...", rosa_vermelho, LARGURA_TELA/36, ALTURA_TELA/28, "crystal.ttf", 40)
        exibe_texto("Mas nao desista!", cinza_roxo, LARGURA_TELA/45, ALTURA_TELA/7.368, "crystal.ttf", 40)

        exibe_texto("pressione espaco para Jogar", amarelo, LARGURA_TELA/9, ALTURA_TELA/1.228, "regcrystal.ttf", 30)
        exibe_texto("pressione M para ir ao menu", amarelo, LARGURA_TELA/8.57, ALTURA_TELA/1.12, "regcrystal.ttf", 30)

        pygame.display.update()
        clock.tick(30)

def tela_win1():
    global pontuacao
    pygame.mixer.music.set_volume(0.15) 

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pygame.mixer.music.stop() 
                    pygame.mixer.music.load("msc_tema.ogg")  
                    pygame.mixer.music.play(-1) 
                    pygame.mixer.music.set_volume(0.15)
                    fade_out(screen, rosa_niveis)
                    tela_niveis()
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif evento.key == pygame.K_m:
                    pygame.mixer.music.stop() 
                    pygame.mixer.music.load("msc_tema.ogg")  
                    pygame.mixer.music.play(-1) 
                    pygame.mixer.music.set_volume(0.15)
                    fade_out(screen, lavanda)
                    tela_inicial()
                    return   
      

        screen.blit(fundo_tela_win1, (0, 0))
        exibe_texto("Score:", vitamina_de_abacate, LARGURA_TELA//7+5, ALTURA_TELA//20+11, "regcrystal.ttf", 25)  
        exibe_texto(f"{pontuacao}", vitamina_de_abacate, LARGURA_TELA/5.5, ALTURA_TELA/8.75+15, "crewni.ttf", 35)
    

        exibe_texto("Parabéns!", rosa_salmao, LARGURA_TELA/36, ALTURA_TELA/2.97, "crystal.ttf", 40)
        exibe_texto("voce", rosa_salmao, LARGURA_TELA/45, ALTURA_TELA/2.09, "crystal.ttf", 40)
        exibe_texto("arrasou!!", rosa_salmao, LARGURA_TELA/45, ALTURA_TELA/1.75, "crystal.ttf", 40)

        exibe_texto("Steven esta", marrom, LARGURA_TELA/1.52, ALTURA_TELA/2.96+17, "regcrystal.ttf", 25)
        exibe_texto("muito feliz", marrom, LARGURA_TELA/1.487, ALTURA_TELA/2.22+1, "regcrystal.ttf", 25)
        exibe_texto("com o seu", marrom, LARGURA_TELA/1.463,ALTURA_TELA/1.912+2, "regcrystal.ttf", 25)
        exibe_texto("biscoito gatinho", marrom, LARGURA_TELA/1.63, ALTURA_TELA/1.75+20, "regcrystal.ttf", 25)

        exibe_texto("pressione M para voltar ao menu", milkshake_de_acai, LARGURA_TELA/8.18, ALTURA_TELA/1.129, "regcrystal.ttf", 25)

        pygame.display.update()
        clock.tick(30)

tela_inicial()
pygame.quit()