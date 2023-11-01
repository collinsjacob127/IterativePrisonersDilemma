# Lucas Butler
from numpy.random import rand

# Code for a node class and a node list generator
class Node():

    score = None
    id = None
    coop_prob = float()
    sucker = float()
    punishment = float()
    reward = float()
    temptation = float()

    def __init__(self, score, coop_prob, id=0):
        self.score=score
        self.id=id
        self.coop_prob=coop_prob
        self.sucker = 3
        self.punishment = 2
        self.reward = 1
        self.tempation = 0

    def __repr__(self):
        return f"{self.id}: ({self.score}, {self.coop_prob})"

        
    def get_score(self):
        return self.score
    
    def get_coop_prob(self):
        return self.coop_prob
    
    # 1 = cooperate
    # 0 = defect
    def strategy(self):
        return bool(rand() < self.coop_prob)

    # u is an instance of another node
    # Compare their strategies and update score accordingly
    def update_score(self, u):
        opponent_choice = u.strategy()
        self_choice = self.strategy()
        # Both cooperate
        if (self_choice and opponent_choice):
            self.score += self.reward
        # Big wins
        if (not self_choice and opponent_choice):
            self.score += self.temptation
        # Huge L
        if (self_choice and not opponent_choice):
            self.score += self.sucker
        # Both were evil
        if (not self_choice and not opponent_choice):
            self.score += self.punishment
        return self_choice
        
        