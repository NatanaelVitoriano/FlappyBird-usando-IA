import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMGS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:
    IMGS = IMGS_PASSARO
    #Animação da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.IMGS[0]
        
    def pular(self):
        self.velocidade = -10,5
        self.tempo = 0
        self.altura = self.y
        
    def mover(self):
        #calcular deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        
        #restringir deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        
        self.y += deslocamento
        
        #angulo do passaro
        if deslocamento < 0 or self.y <(self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
                
    def desenhar(self, tela):
        #Definir img do passaro
        self.contagem_img += 1
        if self.contagem_img < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        
        elif self.contagem_img < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        
        elif self.imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
            
        elif self.imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        
        elif self.imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_img = 0
            
        #se passaro caindo, não bate asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_img = self.TEMPO_ANIMACAO * 2
        
        #desenhar a img
        imagemRotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicaoCentroImg = self.imagem.get_rect(topleft = (self.x, self.y)).center
        retangulo = imagemRotacionada.get_rect(center = posicaoCentroImg)
        tela.blit(imagemRotacionada, retangulo.topleft)
        
    def getMask(self):
        pygame.mask.from_surface(self.imagem)
        
class Cano: 
    DISTANCIA = 200
    VELOCIDADE = 5
    
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posicaoTop = 0
        self.posicaoBot = 0
        self.CANOTOP = pygame.transform.flip(IMG_CANO, False, True)
        self.CANOBOT = IMG_CANO
        self.passou = False
        self.definirAltura()
        
    def definirAltura(self):
        self.altura = random.randrange(50,450)
        self.posicaoTop = self.altura - self.CANOTOP.get_height()
        self.posicaoBot = self.altura + self.DISTANCIA
        
    def mover(self):
        self.x -= self.VELOCIDADE
        
    def desenhar(self, tela):
        tela.blit(self.CANOTOP, (self.x, self.posicaoTop))        
        tela.blit(self.CANOBOT, (self.x, self.posicaoBot))
        
    def colidir(self, passaro):
        passaroMask = passaro.get_mask()
        topMask = pygame.mask.from_surface(self.CANOTOP)
        botMask = pygame.mask.from_surface(self.CANOBOT)
        
        distanciaTop = (self.x - passaro.x, self.posicaoTop - round(passaro.y))
        distanciaBot = (self.x - passaro.x, self.posicaoBot - round(passaro.y))
        
        colisaoTop = passaroMask.overlap(topMask, distanciaTop)
        colisaoBot = passaroMask.overlap(botMask, distanciaBot)
        
        if colisaoTop or colisaoBot:
            return True
        else:
            return False