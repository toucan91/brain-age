import time
import random
import math

def count_digit(n, d = 0):
    if n == 0:
        return 1
        
    while n >= 1:
        n = n / 10 
        d += 1
        count_digit(n, d)
    
    return d

def makeAns(a, b, opp):
    result = {
        0: a + b,
        1: abs(a - b),
        2: a * b,
        3: a * b,
        }[opp]
    return int(round(result,0))


class question:
    def __init__(self, low = 1, hi = 9, opp = -1):
        self._init_(low, hi, opp)

    def _init_(self, low = 1, hi = 9, opp = -1):
        self.a = int(random.uniform(low,hi)) 
        self.b = int(random.uniform(low,hi)) 
        self.sol = False
    
        # choose random operation +, -, *, /
        self._dict = {
                0: ' + ',
                1: ' - ',
                2: ' \u00d7 ',
                3: ' \u00f7 '
            }

        # randomize operations unless specified
        if opp < 0:
            self.oppCode = int(random.getrandbits(2))
        else:
            self.oppCode = opp
        
        self.ans = makeAns(self.a, self.b, self.oppCode)

        if self.oppCode == 3:
            temp = self.ans
            self.ans = self.a
            self.a = temp
        
        if self.oppCode == 1:
            if self.a < self.b:
                    temp = self.a
                    self.a = self.b
                    self.b = temp


    def solve(self):
        self.sol = True

    def ask(self):
        val = str(self.a) + self._dict[self.oppCode] + str(self.b) + " = ?"
        return val
        
    def ans_digit(self):
        return count_digit(self.ans)



class question_div(question):
    def __init__(self, low = 1, hi = 9):
        self._init_(low, hi, 3)

class question_mult(question):
    def __init__(self, low = 1, hi = 9):
        self._init_(low, hi, 2) 

class question_arth(question):
    def __init__(self, low = 1, hi = 9):
    # initiate question as a (operation) b 
    # with integers from range [low,hi]
    # self.sol = false initiaze question as `unsolved`
    
    # choose random operation + or -
        self.sign = int(random.getrandbits(1))
        self._init_(low, hi, self.sign)