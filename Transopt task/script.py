from cvxopt.modeling import variable, op

A = [6421*0.67, 3700*0.67, 5600*0.67, 3200*0.67]
B = [3400, 3400, 3200, 2600, 3700]

x = variable(20, 'x')
C = [5.7, 2.6, 6.2, 7.8, 6.2,
     3.3, 2.7, 6.6, 7.1, 5.2,
     7.7, 5.5, 2.3, 6.7, 3.4,
     6.9, 6.6, 2.8, 7.0, 3.2]

def getRestrictions (x, A, B):
    restrictions= list()
    row = 0
    for Ai in A:
        xRow = 0
        for j in range(row*len(B), row*len(B)+len(B)):
            xRow = xRow + x[j]
        restrictions.append(xRow <= Ai)
        row = row + 1
    row = 0
    for Bi in B:
        xRow = 0
        for j in range(0, len(A)):
            xRow = xRow + x[j*len(B)+row]
        restrictions.append(xRow == Bi)
        row = row + 1
    restrictions.append(x >= 0)
    return restrictions

Atotal = A[0] + A[1] + A[2] + A[3]
Btotal = B[0] + B[1] + B[2] + B[3] + B[4]

print("##############################################################")
if(Atotal == Btotal):
    print("Stocks equal needs")
elif(Atotal > Btotal):
    print("There is an excess of stocks")
    difference = Atotal - Btotal
    if(difference <= 0.15*Btotal):
        print("Excess does not exceed 15%")
        x = variable(24, 'x')
        C = [5.7, 2.6, 6.2, 7.8, 6.2, 0,
             3.3, 2.7, 6.6, 7.1, 5.2, 0,
             7.7, 5.5, 2.3, 6.7, 3.4, 0,
             6.9, 6.6, 2.8, 7.0, 3.2, 0]
        B.append(difference)
    else:
        print("Excess exceed 15%")
        for i in range(0, 5):
            B[i] = B[i] + difference*(B[i]/Btotal)
else:
    print("There is a lack of stocks")
    difference = Btotal - Atotal
    if(difference > 0.15*Btotal):
        print("Stock shortage exceed 15%")
        x = variable(25, 'x')
        C = [5.7, 2.6, 6.2, 7.8, 6.2,
             3.3, 2.7, 6.6, 7.1, 5.2,
             7.7, 5.5, 2.3, 6.7, 3.4,
             6.9, 6.6, 2.8, 7.0, 3.2,
             0,   0,   0,   0,   0  ]
        A.append(difference)
    else:
        print("Stock shortage does not exceed 15%")
        for i in range(0, 5):
            B[i] = Atotal*(B[i]/Btotal)
        x = variable(20, 'x')
print("##############################################################")

z = 0
for i in range(0, len(x)):
    z = z + x[i]*C[i]
conditions = getRestrictions (x, A, B)

problem =op(z, restrictions)
problem.solve(solver='glpk')
print("##############################################################")
print("Result Xopt:")
k = 0
for i in range(0, len(A)):
    for j in range(0, len(B)):
        print("from A{} to B{}: {}".format(i+1, j+1, round(x.value[k])), end = " ")
        k = k + 1
    print("\n")
print("##############################################################")
print("Cost:")
print(round(problem.objective.value()[0]))
print("##############################################################")
