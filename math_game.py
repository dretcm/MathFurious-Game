import pygame, sys, random, time
from pygame.locals import *

class GameMath:
        clock = pygame.time.Clock()
        WINDOW_SIZE = (810, 500)

        pygame.init()

        pygame.display.set_caption('Math and furious') 
        screen = pygame.display.set_mode(WINDOW_SIZE)

        def __init__(self):
                self.restart_game()

        def restart_game(self):
                self.a,self.b,self.c=0,0,0
                self.op = '+'

                self.table_1, self.table_2, = [],[]
                
                # players:
                self.damage = 20

                self.player1 = 300
                self.player1_select = 0
                self.player1_can = False
                self.turn1 = True

                self.player2 = 300
                self.player2_select = 0
                self.player2_can = False
                self.turn2 = True

                self.state_win = False

        
        def life_bar(self,life, x, y):
                pygame.draw.rect(self.screen, (255,0,0), [x,y,300,40]) # red
                pygame.draw.rect(self.screen, (0,255,0), [x,y,life,40]) # green
                

        def problem(self,x,y,operator):
                if operator == '/':
                        if y != 0:
                                return x//y
                        else:
                                return 'None'
                elif operator == 'X':
                        return x*y
                elif operator == '-':
                        return x-y
                else:
                        return x+y
                
        def generate_problem(self,changue):
                operators = '+-X/'
                if changue:
                        self.op = random.choice(operators)
                        self.a,self.b = random.randint(-10,10),random.randint(-10,10)
                        self.c = self.problem(self.a,self.b,self.op)
                pygame.draw.rect(self.screen, (255,255,255), [290,350,220,100]) # blackboard
                font = pygame.font.Font(None, 80)
                text = font.render(f'{self.a}{self.op}{self.b}=?',1,(0,0,0))
                self.screen.blit(text,(300,375))
                return self.c
        
        def alternatives(self,reply, changue):
                if changue:
                        x,y=random.randint(-10,10),random.randint(-10,10)
                        self.table_1 = [x,y,reply]
                        self.table_2 = [x,y,reply]
                        #random.seed(10)
                        random.shuffle(self.table_1)
                        #random.seed(50)
                        random.shuffle(self.table_2)
        ##        pygame.draw.rect(screen, (0,0,0), [60,360,230,100]) # 1 player
        ##        pygame.draw.rect(screen, (0,0,0), [560,370,230,100]) # 2 player
                font = pygame.font.Font(None, 70)
                x,y,z = self.table_1
                text = font.render(f'{x}|{y}|{z}',1,(255,255,255))
                x,y,z = self.table_2
                text2 = font.render(f'{x}|{y}|{z}',1,(255,255,255))
                self.screen.blit(text,(55,380))
                self.screen.blit(text2,(565,380))


        def animation(self, part='base'):
                if part == 'base':
                        p1 = pygame.transform.scale(pygame.image.load('images\\p1.png'), (180,250))
                        p2 = pygame.transform.scale(pygame.image.load('images\\p2.png'), (180,250))
                elif part == 'p1':
                        p1 = pygame.transform.scale(pygame.image.load('images\\p1_attack.png'), (300,350))
                        p2 = pygame.transform.scale(pygame.image.load('images\\p2.png'), (180,250))
                elif part == 'p2':
                        p1 = pygame.transform.scale(pygame.image.load('images\\p1.png'), (180,250))
                        p2 = pygame.transform.scale(pygame.image.load('images\\p2_attack.png'), (300,350))
                        
                self.screen.blit(p1,(80,110))
                self.screen.blit(p2,(500,110))

                pygame.display.update()

                if part in ('p1','p2'):
                        time.sleep(1)
                else:
                        pass
                

        def win_game(self):
                cade = ''
                if self.player1 < 1:
                        cade = 'Player 2'
                if self.player2 < 1:
                        cade = 'Player 1'
                        
                while cade:
                        font = pygame.font.Font(None,70)
                        message = font.render(f'WINER: {cade}',1,(255,255,255))
                        self.screen.blit(message, (160,200))
                        
                        button = pygame.Rect(250,300, 300,70)
                        pygame.draw.rect(self.screen, (255,100,0), button)
                        message = font.render('Play Again',1,(0,0,0))
                        self.screen.blit(message, (265,310))
                                                
                        pygame.display.update()
                                                
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1 and button.collidepoint(event.pos):
                                                self.restart_game()
                                                self.run_game()
                

        def run_game(self):
                while True:
                        self.screen.fill((128, 128, 128))
                        self.win_game()
                        
                        self.life_bar(self.player1, 50,50) # 1 player
                        self.life_bar(self.player2,450,50) # 2 player


                        if not self.state_win:
                                reply = self.generate_problem(True)
                                self.alternatives(reply, True)
                                self.state_win = True
                                self.turn1 = True
                                self.turn2 = True
                        else:
                                reply = self.generate_problem(False)
                                self.alternatives(reply, False)

                        if self.player1_can and self.turn1:
                                if self.table_1[self.player1_select] == reply:
                                        self.player2 -= self.damage
                                        self.state_win = False
                                        self.animation('p1')
                                else:
                                        self.player1 -= self.damage
                                self.turn1 = False
                                
                        if self.player2_can and self.turn2:
                                if self.table_2[self.player2_select] == reply:
                                        self.player1 -= self.damage
                                        self.state_win = False
                                        self.animation('p2')
                                else:
                                        self.player2 -= self.damage
                                self.turn2 = False
                                        
                        if not self.turn1 and not self.turn2:
                                self.player1 -= self.damage
                                self.player2 -= self.damage
                                self.state_win = False
                                
                        self.player1_can, self.player2_can = False, False

                        self.animation()
                        
                        
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == KEYDOWN:
                                        if event.key == K_z:
                                                self.player1_select = 0
                                                self.player1_can = True
                                        if event.key == K_x:
                                                self.player1_select = 1
                                                self.player1_can = True
                                        if event.key == K_c:
                                                self.player1_select = 2
                                                self.player1_can = True
                                        if event.key == K_KP1:
                                                self.player2_select = 0
                                                self.player2_can = True
                                        if event.key == K_KP2:
                                                self.player2_select = 1
                                                self.player2_can = True
                                        if event.key == K_KP3:
                                                self.player2_select = 2
                                                self.player2_can = True
                                        
                        pygame.display.update()
                        self.clock.tick(60)


game = GameMath()
game.run_game()

        
