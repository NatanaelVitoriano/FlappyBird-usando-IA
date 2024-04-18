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
        
        elif self.contagem_img < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
            
        elif self.contagem_img < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        
        elif self.contagem_img >= self.TEMPO_ANIMACAO * 4 + 1:
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
        return pygame.mask.from_surface(self.imagem)
        
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
        passaroMask = passaro.getMask()
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
        
class Chao:
    VELOCIDADE = 5
    LARGURA = IMG_CHAO.get_width()
    IMG = IMG_CHAO
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
        
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA
    
    def desenhar(self, tela):
        tela.blit(self.IMG, (self.x1, self.y))        
        tela.blit(self.IMG, (self.x2, self.y))


def desenharTela(tela, passaros, canos, chao, pontos):
    tela.blit(IMG_BACKGROUND, (0, 0))
    
    for passaro in passaros:
        passaro.desenhar(tela)
        
    for cano in canos:
        cano.desenhar(tela)
    
    text = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(text, (TELA_LARGURA - 10 - text.get_width(), 10))
    chao.desenhar(tela)
    
    pygame.display.update()
    
def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()
    
    while True:
        relogio.tick(60)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.QUIT()
                quit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
            
            for passaro in passaros:
                passaro.mover()
                
            chao.mover()
            
            adicionarCano = False
            removerCanos = []
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if cano.colidir(passaro):
                        passaros.pop(i)
                        
                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        adicionarCano = True
                    
                    cano.mover()
                    if cano.x + cano.CANOTOP.get_width() < 0:
                        removerCanos.append(cano)
            
            if adicionarCano:
                pontos += 1
                canos.append(Cano(600))
            
            for cano in removerCanos:
                cano.remove(cano)
                
            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)
            
        desenharTela(tela, passaros, canos, chao, pontos)
        
if __name__ == '__main__':
    main()
os.system("PAUSE")