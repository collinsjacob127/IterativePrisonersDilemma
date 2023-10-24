# Lucas Butler
from numpy.random import rand

# Code for a node class and a node list generator
class Node():

    score = None
    coop_prob = float()

    def __init__(self, score, coop_prob):
        self.score=score
        self.coop_prob=coop_prob

    def __repr__(self):
        return f"({self.score}, {self.coop_prob})"
    
    # 1 = cooperate
    # 0 = defect
    def strategy(self):
        return int(rand() < self.coop_prob)

    # u is an instance of another node
    # Compare their strategies and update score accordingly
    def updateScore(self, u):
        opponent_choice = u.strategy()
        self_choice = self.strategy()
        return