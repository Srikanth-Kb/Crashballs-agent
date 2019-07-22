import pygame, math, random, time
import numpy as np
from pygame.locals import *
from random import randint
from agent import AIAgent
from keras.utils import to_categorical
import seaborn as sea
import matplotlib.pyplot as plt
import time



ANTICLOCKWISE = 0
CLOCKWISE = 1
FORWARD = 2

class Game:

    def __init__(self,game_width,game_height):
        pygame.display.set_caption('Hitballs_Pygame')
        pygame.mouse.set_visible(0)
        self.game_width = game_width
        self.game_height = game_height
        self.game_display = pygame.display.set_mode((self.game_width,self.game_height+60))
        self.black = (200,200,200)
        self.crash = False
        self.game_display.fill(self.black)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.fps = 100
        self.speed = 6
        self.spawn_count = 10
        self.sound = pygame.mixer.music.load('noise.mp3')
        self.difficulty = 'normal'
        self.explosion = pygame.image.load('crash.png')
        pygame.display.update()



class Player:

    def __init__(self,game):
        self.image = pygame.image.load('player_1.png')
        self.x = game.game_width/2
        self.y = game.game_height/2
        self.angle = 0
        self.direction = None
        self.motion = False
        self.rect_coord = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)
        game.game_display.blit(self.image,(self.x,self.y))

    def rotate_player(self,game):
        
        if self.direction==ANTICLOCKWISE:
            self.angle+=5
        if self.direction==CLOCKWISE:
            self.angle-=5
        if self.motion:
            self.move_player(game)
        new_image = pygame.transform.rotate(self.image,self.angle)
        new_image_center = new_image.get_rect().center
        new_center = (self.rect_coord.center[0]-new_image_center[0],self.rect_coord.center[1]-new_image_center[1])
        game.game_display.blit(new_image,new_center)

    def move_player(self,game):
        y = math.cos(math.radians(self.angle))*game.speed
        x = math.sin(math.radians(self.angle))*game.speed
        self.rect_coord.top -= round(y)
        self.rect_coord.left -= round(x)
    def do_action(self,actions,game):
        if actions[0]==1:
            self.direction=ANTICLOCKWISE
        elif actions[1]==1:
            self.direction=CLOCKWISE
        if actions[2]==1:
            self.motion = True
        else:
            self.motion = False
        self.rotate_player(game)
        
        


class Balls:
    ##def __init__(self,game):
        #self.image = pygame.image.load('ball_rot.png')
        #self.rect = pygame.Rect(randint(0,game.game_width-self.image.get_rect().width),randint(0,game.game_height-self.image.get_rect().height),self.image.get_rect().width,self.image.get_rect().height)
        #self.angle = randint(0,360)
        #self.x = randint(0,game.game_width-21)
        #self.y = randint(0,game.game_height-21)
        
    def moving_balls(self,game):
        if self.angle>360:
            self.angle= self.angle%360
        if self.angle<0:
            self.angle=360+self.angle
        if self.rect.top <=0:
            if 0 < self.angle < 90:
                self.angle = self.angle+90
            elif 270 < self.angle < 360:
                self.angle = self.angle-90
            elif self.angle==0:
                self.angle=180
        if self.rect.bottom >=game.game_height:
            if 90< self.angle<180:
                self.angle=self.angle-90
            elif 180<self.angle<270:
                self.angle=self.angle+90
            elif self.angle==180:
                self.angle=0
        if self.rect.left <=0:
            if 90 < self.angle < 180:
                self.angle+=90
            elif 0 < self.angle < 90:
                self.angle-=90
            elif self.angle==90:
                self.angle=270
        if self.rect.right>=game.game_width:
            if 270 < self.angle < 360:
                self.angle+=90
            elif 180 < self.angle < 270:
                self.angle-=90
            elif self.angle==270:
                self.angle=90
      
        y = math.cos(math.radians(self.angle))*self.speed
        x = math.sin(math.radians(self.angle))*self.speed
        self.rect.top -= round(y)
        self.rect.left -= round(x)
        game.game_display.blit(self.image,(self.rect.left,self.rect.top))

class redBall(Balls):
    def __init__(self,game):
        self.image = pygame.image.load('red_ball.png')
        self.rect = pygame.Rect(randint(0,game.game_width-self.image.get_rect().width),randint(0,game.game_height-self.image.get_rect().height),self.image.get_rect().width,self.image.get_rect().height)
        self.angle = randint(0,360)
        self.x = randint(0,game.game_width-21)
        self.y = randint(0,game.game_height-21)
        self.speed = 2
    def moving_balls(self,game):
        super().moving_balls(game)

class blueBall(Balls):
    def __init__(self,game):
        self.image = pygame.image.load('blue_ball.png')
        self.rect = pygame.Rect(randint(0,game.game_width-self.image.get_rect().width),randint(0,game.game_height-self.image.get_rect().height),self.image.get_rect().width,self.image.get_rect().height)
        self.angle = randint(0,360)
        self.x = randint(0,game.game_width-21)
        self.y = randint(0,game.game_height-21)
        self.speed = 2
    def moving_balls(self,game):
        super().moving_balls(game)

class greenBall(Balls):
    def __init__(self,game):
        self.image = pygame.image.load('green_ball.png')
        self.rect = pygame.Rect(randint(0,game.game_width-self.image.get_rect().width),randint(0,game.game_height-self.image.get_rect().height),self.image.get_rect().width,self.image.get_rect().height)
        self.angle = randint(0,360)
        self.x = randint(0,game.game_width-21)
        self.y = randint(0,game.game_height-21)
        self.speed = 2

    def moving_balls(self,game):
        super().moving_balls(game)


 
        
def display_score(game,agent):
    myfont = pygame.font.SysFont('Segoe UI',20)
    myfont_bold = pygame.font.SysFont('Segoe UI',20,True)
    text_score = myfont.render('SCORE: ',True,(0,0,0))
    text_score_number = myfont.render(str(game.score),True,(0,0,0))
    text_highest = myfont.render('HIGHEST SCORE: ', True,(0,0,0))
    text_highest_number = myfont_bold.render(str(agent.high_score),True,(0,0,0))
    game.game_display.blit(text_score, (145, 620))
    game.game_display.blit(text_score_number, (220, 620))
    game.game_display.blit(text_highest, (300, 620))
    game.game_display.blit(text_highest_number, (470, 620))


def check_collision(player,balls):
    for ball in balls:
        if player.rect_coord.colliderect(ball.rect):
            return True
    return False
            
def player_crashed(player,game):
    if player.rect_coord.top<20 or player.rect_coord.bottom>game.game_height or player.rect_coord.right>game.game_width or player.rect_coord.left<0:
        return True
    else:
        return False

def action_mapping(action):
    move = [0,0,0]
    x = np.argmax(action)
    if x==0:
        move=[0,0,1]
    elif x==1:
        move=[1,0,0]
    elif x==2:
        move=[0,1,0]
    elif x==3:
        move=[1,0,1]
    elif x==4:
        move=[0,1,1]
    return move


def set_first_move(game,player,balls,agent):
    state1 = agent.get_state(game,player,balls)
    action = [0,0,0,0,0]
    action[randint(0,4)] = 1
    move = action_mapping(action)
    player.do_action(move,game)
    state2 = agent.get_state(game,player,balls)
    reward = agent.set_reward(player,game)
    agent.remember(state1,action,reward,state2,game.crash)
    agent.replay_new(agent.memory)

def plot_seaborn(array_counter, array_score):
    sea.set(color_codes=True)
    ax = sea.regplot(np.array([array_counter])[0], np.array([array_score])[0], color="b", x_jitter=.1, line_kws={'color':'green'})
    ax.set(xlabel='games', ylabel='score')
    plt.show()


pygame.init()
pygame.display.init()
pygame.font.init()
agent = AIAgent()
count_game = []
score_game = []
game_number = 0
while game_number < 150:
    
    game = Game(800,600)
    player = Player(game)
    red_ball = redBall(game)
    balls = [red_ball]
    display_score(game,agent)
    set_first_move(game,player,balls,agent)
    pygame.display.update()
    count = 0
    
    while game.crash==False:
        game.score+=1
        game.game_display.fill(game.black)
        for ball in balls:
            ball.moving_balls(game)
        
        agent.epsilon = 80 - game_number
        current_state = agent.get_state(game,player,balls)
        
        if randint(0,200) < agent.epsilon:            
            if randint(0,100)<50:
                #player.angle = randint(0,359)
                player.direction = random.choice([CLOCKWISE,ANTICLOCKWISE])
            if randint(0,100)<25:
                player.motion = random.choice([True,False])
            final_move = [int(player.direction==ANTICLOCKWISE),int(player.direction==CLOCKWISE),int(player.motion)]

        else:
            predicted_action = agent.model.predict(current_state.reshape((1,10)))
            final_move=action_mapping(predicted_action[0])
        '''
        predicted_action = agent.model.predict(current_state.reshape((1,10)))
        final_move=action_mapping(predicted_action[0])
        '''
        player.do_action(final_move,game)
        new_state = agent.get_state(game,player,balls)
        if check_collision(player,balls):
            game.crash=True
        if player_crashed(player,game):
            game.crash=True
        reward = agent.set_reward(player,game)
        agent.short_term_memory(current_state,final_move,reward,new_state,game)
        agent.remember(current_state,final_move,reward,new_state,game.crash)
        
        
        if count>=game.spawn_count and len(balls)<=15:
            x = randint(1,3)
            if x==1:
                balls.append(redBall(game))
            elif x==2:
                balls.append(blueBall(game))
            elif x==3:
                balls.append(greenBall(game))
            count=0
        count=count+1
              
        display_score(game,agent)   
        pygame.display.update()
        game.clock.tick(game.fps)
    game_number = game_number+1
    print('Game number:',game_number,'\t','Score:',game.score)
    if game.score>agent.high_score:
        agent.high_score=game.score
    score_game.append(game.score)
    count_game.append(game_number+1)

plot_seaborn(count_game,score_game)
print('High score by the agent:',agent.high_score)
agent.model.save_weights('fixed_balls.h5')
print('Model Saved')
pygame.display.quit()   
      
                
          
            
            

