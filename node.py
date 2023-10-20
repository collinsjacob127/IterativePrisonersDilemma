# Lucas Butler

# Code for a node class and a node list generator
class Node():

    score = None
    coop_prob = float()

    def __init__(self, score, coop_prob):
        self.score=score
        self.coop_prob=coop_prob

    def __repr__(self):
        return f"({self.score}, {self.coop_prob})"
    
    def test(self):
        return 'success'