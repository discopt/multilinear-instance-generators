import sys
from gurobipy import *

def generate(N, R, outFilePrefix, factor=1):
  if R < N:
    raise Exception('Not implemented')
  model = Model()
  
  x = {}
  for i in range(1, N+1):
    x[i] = model.addVar(name=f'x_{i}', vtype=GRB.BINARY)
  
  y = {}
  for i in range(1, N+1):
    for j in range(i+1, N+1):
      y[i,j] = model.addVar(name=f'y_{i}_{j}', vtype=GRB.BINARY)
  
  z = {}
  for i in range(1, N-R+2):
    for d in range(1, R):
      for k in range(-R-d, R+d+1, 2):
        z[i,d,k] = model.addVar(name=f'z_{i}_{d}_{k}'.replace('-', 'm'), vtype=GRB.BINARY, obj=k*k)
  
  model.update()
  
  for i in range(1, N+1):
    for j in range(i+1, N+1):
      # y[i,j]=1 <=> x[i] == x[j]
      # Forbidden:
      # x_i x_j y_ij
      #  0   0   0 -> x_i + x_j + y_ij >= 1
      #  0   1   1 -> x_i - x_j >= y_ij - 1
      #  1   0   1 -> x_j - x_i >= y_ij - 1
      #  1   1   0 -> x_i + x_j <= 1 + y_ij
      model.addConstr( x[i] + x[j] + y[i,j] >= 1) # forbids (x_i,x_j,y_ij) = (0,0,0)
      model.addConstr( x[i] - x[j] >= y[i,j] - 1) # forbids (x_i,x_j,y_ij) = (0,1,1)
      model.addConstr( x[j] - x[i] >= y[i,j] - 1) # forbids (x_i,x_j,y_ij) = (1,0,1)
      model.addConstr( x[i] + x[j] <= 1 + y[i,j]) # forbids (x_i,x_j,y_ij) = (1,1,0)
  
  for i in range(1, N-R+2):
    for d in range(1, R):
      model.addConstr( quicksum( z[i,d,k] for k in range(-R-d, R+d+1, 2) ) == 1 )
      model.addConstr( quicksum( k * z[i,d,k] for k in range(-R-d, R+d+1, 2) ) == quicksum( (2*y[j,j+d]-1) for j in range(i, i+R-d) ) )
  
  model.write(outFilePrefix)

if __name__ == '__main__':
  try:
    N = int(sys.argv[1])
    R = int(sys.argv[2])
    outFilePrefix = sys.argv[3]
  except:
    print(f'Usage: {sys.argv[0]} N R OUTFILEPREFIX')
    print('Creates OUTFILEPREFIX.lp')
    sys.exit(1)

  generate(N, R, outFilePrefix)

