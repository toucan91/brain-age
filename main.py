import time
import random
import math
import ans

def main(n=10):
    dig = 100
    print(ans.count_digit(dig))
    
    print("Hello, here are " + str(n) + " questions for brain age:")

    ls = [ans.question() for i in range(n)]
    next_q = ls[0]

    # tries
    lim = 5

    # start timer
    t0 = time.time()
    
    while bool(n):

        print( next_q.ask() )
        tries = lim 

        while not next_q.sol:
            # ask
            if not tries:
                print(":O ok time to skip, by the way it's " + str(next_q.ans))
                guess = next_q.ans

            try:
                guess = int(input())
                if guess == next_q.ans:
                    next_q.solve()
     
            except Exception:
                print("Oops! not an integer")
            
                   
            tries -= 1

                   # goto next question
        n -= 1
        next_q = ls[-n]

    print("Your time is")
    print(time.time() - t0)

if __name__ == "__main__":
    main()
