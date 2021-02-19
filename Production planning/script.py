from scipy.optimize import linprog
from math import *

Y = 139

timeFund = [860, 1440, 1100]

        #A1     #A3    #B1     #B2    #C2    #C3
A_ub = [[0.13,  0,     0.17,  0,     0,     0    ],#1
        [0,     0,     0,     0.15,  0.2,   0    ],#2
        [0,     0.18,  0,     0,     0,     0.28 ],#3
        [0.004, 0.004, 0.008, 0.009, 0.001, 0.003]]#Y

A_eq = [[1, 1, -1, -1, 0, 0],
        [1, 1, 0, 0, -1, -1]]
b_eq = [0, 0];

c = [-1, -1, -1, -1, -1, -1]

b_ub = [timeFund[0], timeFund[1], timeFund[2], Y]

def Result(b_ub = [timeFund[0], timeFund[1], timeFund[2], Y]):
	result = linprog(c, A_ub, b_ub, A_eq, b_eq)
	print(
"Result:\nA1 = {}, A3 = {}\nB1 = {}, B2 = {}\nC2 = {}, C3 = {}\nTotal = {}”.format(floor(result.x[0]),floor(result.x[1]),
	floor(result.x[2]),
	floor(result.x[3]),									floor(result.x[4]),
		floor(result.x[5]),									(floor(result.x[0]+									floor(result.x[1]+										floor(result.x[2]+										floor(result.x[3]+
floor(result.x[4]+
floor(result.x[5]))))
return result

result = Result()

def makeLoaded(x):
	global b_ub
	global Y
	equipLoad = equipmentLoad(linprog(c, A_ub, b_ub).x)
while equipLoad.count(0) == 3:
	Y = Y + Y*0.01
	b_ub = [timeFund[0], timeFund[1], timeFund[2]]
	equipLoad = equipmentLoad(linprog(c, A_ub, b_ub).x)

def parametricResearch(eqNum):
	timeFundNew = timeFund[:]
print("When increasing time fund of the equipment group {}\n".format(eqNum+1))
for i in range(1, 4):
	timeFundNew[eqNum] = timeFundNew[eqNum] + 100*i
	print("time fund = {}".format(timeFundNew[eqNum]))
Result([timeFundNew[0],timeFundNew[1],timeFundNew[2], Y])
print("When deacreasing time fund of the equipment group {}\n".format(eqNum+1))
timeFundNew = timeFund[:]
for i in range(1, 4):
timeFundNew[eqNum] = timeFundNew[eqNum] - 100*i
	print("time fund = {}".format(timeFundNew[eqNum]))
Result([timeFundNew[0],timeFundNew[1],timeFundNew[2], Y])

def equipmentLoad(x):
return ((round(0.13*x[0] + 0.17*x[2]) == timeFund[0]),
    		(round(0.15*x[3] + 0.2*x[4]) == timeFund[1]),
    		(round(0.18*x[1] + 0.28*x[5]) == timeFund[2]))

if result.success:
    equipLoad = equipmentLoad(result.x)
if equipLoad.count(0) == 3:
print("\nThere is no loaded equipment group\n Will change Y until one of the equipment group become loaded\n")
makeLoaded(result.x)
result = linprog(c, A_ub, b_ub)
equipLoad = equipmentLoad(result.x)
print("New Y is {}\n".format(Y))

if result.success:
print("We have {} loaded equipment group\n".format(equipLoad.count(1)))
    for i in range(0, 3):
    		if equipLoad[i]:
print('Explore the change in the time fund of the equipment group {} on the structure of the solution\n'.format(i+1))
    			parametricResearch(i)
 else:
    print("unsuccessful result")
else:
     print("unsuccessful result")
