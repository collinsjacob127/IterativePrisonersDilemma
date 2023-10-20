# Lucas Butler

# Code for a node class and a node list generator
class Node():

    score = None
    id = None
    coop_prob = float()

    def __init__(self, id, score, coop_prob):
        self.id=id
        self.score=score
        self.coop_prob=coop_prob

    def __repr__(self):
        return f"({self.score}, {self.coop_prob})"
    