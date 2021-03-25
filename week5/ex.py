import random

pool = []
isVisited = [0 for i in range(46)]

def GetLotteryNumber(N):
    num = random.randrange(1,N+1)
    return num

while len(pool)<6:
    num = GetLotteryNumber(45)
    if isVisited[num] != True:
        isVisited[num] = True;
        pool.append(num)     

print(pool)
