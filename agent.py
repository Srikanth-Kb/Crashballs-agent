import random
import numpy as np
from keras.optimizers import Adam
from keras.models import Sequential,load_model
from keras.layers.core import Dense, Dropout

ANTICLOCKWISE='anticlockwise'
CLOCKWISE='clockwise'
FORWARD='forward'


class AIAgent(object):

    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.model = self.network()
        self.memory = list()
        self.epsilon = 0.3
        self.learning_rate = 0.0005
        self.high_score = 0
        

    def get_state(self,game,player,balls):
        #balls_position=list()
        state = [ #Danger on top
                player.rect_coord.top<=30, self.ball_above(player,balls),
                  #Danger to left
                player.rect_coord.left<=0, self.ball_left(player,balls),
                  #Danger to right
                player.rect_coord.right>=game.game_width, self.ball_right(player,balls),
                  #Danger below
                player.rect_coord.bottom>=game.game_height, self.ball_below(player,balls),
                    self.angle(player.angle),
                    int(player.motion)]
        for i in range(len(state)):
            if state[i]==True:
                state[i]=1
            elif state[i]==False:
                state[i]=0
            else:
                continue
        return np.asarray(state)

    def angle(self,theta):
        return theta%360
    def ball_above(self,player,balls):
        for ball in balls:
           if player.rect_coord.top-40<=ball.rect.bottom and player.rect_coord.bottom > ball.rect.bottom and ball.rect.right>=player.rect_coord.left and player.rect_coord.right>=ball.rect.left:
                return True
        return False
    def ball_left(self,player,balls):
        for ball in balls: 
            if player.rect_coord.left-40<=ball.rect.right and ball.rect.right<player.rect_coord.right and player.rect_coord.bottom>=ball.rect.top and player.rect_coord.top<=ball.rect.bottom:
                    return True
        return False
    def ball_right(self,player,balls):
        for ball in balls:
            if player.rect_coord.right+40>=ball.rect.left and ball.rect.left>player.rect_coord.left and player.rect_coord.bottom>=ball.rect.top and player.rect_coord.top<=ball.rect.bottom:
                return True
        return False
    def ball_below(self,player,balls):
        for ball in balls:
            if ball.rect.top<=player.rect_coord.bottom+40 and player.rect_coord.top < ball.rect.top and ball.rect.right>=player.rect_coord.left and player.rect_coord.right>=ball.rect.left:
                return True
        return False
    
    
            

    def set_reward(self,player,game):
        self.reward = 0
        if game.crash:
            self.reward = -1
        return self.reward

    def network(self,weights=None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation = 'relu', input_dim=10))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam(0.0005)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))


    def replay_new(self,memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory,1000)
        else:
            minibatch = memory
        for state1,action,reward,state2, crash in minibatch:
            target = reward
            if not crash:
                target = reward + self.gamma*np.amax(self.model.predict(np.array([state2]))[0])
            predicted_target = self.model.predict(np.array([state1]))       #predicted reward for next state\
            predicted_target[0][np.argmax(action)] = target
            self.model.fit(np.array([state1]), predicted_target, epochs=1, verbose=0)

    def short_term_memory(self,state,action,reward,state2,game):
        target = reward
        if not game.crash:
            target = reward + self.gamma * np.amax(self.model.predict(np.array([state2]))[0])
        predicted_target = self.model.predict(state.reshape((1,10)))
        predicted_target[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1,10)), predicted_target, epochs=1,verbose=0)

    
        

    
        
                    
                    

                    
            
