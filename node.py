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
            u.score += u.reward
            # no take over

        # Big wins
        if (not self_choice and opponent_choice):
            self.score += self.temptation
            u.score += u.sucker

            # U is taken over by self
            u.taken_over_by(self.coop_prob)

        # Huge L
        if (self_choice and not opponent_choice):
            self.score += self.sucker
            u.score += u.temptation

            # self is taken over by u
            self.taken_over_by(u.get_coop_prob())

        # Both were evil
        if (not self_choice and not opponent_choice):
            self.score += self.punishment
            u.score += u.punishment
            #No Take Over

        return self_choice
<<<<<<< HEAD
=======
        
    def taken_over_by(self, new_strategy):
        # Gets called on a node that is getting taken over
        # gets strategy passed as an argument
        increment =0.1
        current_strategy = self.coop_prob

        if current_strategy > new_strategy:
            current_strategy -= increment
        else:
            current_strategy += increment

        # Bounds check 
        if current_strategy < 0:    current_strategy = float(0)
        if current_strategy > 1:    current_strategy = float(1)

        # update to the new strategy
        self.coop_prob = current_strategy
>>>>>>> 10fe856fc5a495e7685aa8c8fc6f63ef00ae1160
