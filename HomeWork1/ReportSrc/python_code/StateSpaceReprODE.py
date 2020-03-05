import numpy as np

def constructStateSpace(coefficients:np.ndarray) -> (np.ndarray, np.ndarray):
    #Used comments instead of doctring due to latex formatting problem
    #degree = len(coefficients)
    #:param coefficients: 1 dimensional array in format [ak a(k-1) ... a0] 
    #:return: state matrix ([degree-2]x[degree-2]) and input matrix [degree-2]x[1]
    
    if len(coefficients.shape) != 1:
        raise ValueError("coefficients are expected to be passed as 1 dimensional array")
    deg = len(coefficients)
    
    input_matrix =np.zeros((deg-1))
    input_matrix[-1] = 1/coefficients[0] # normalize coefficient of input
    
    coefficients = coefficients[1:]/coefficients[0] # normalize coefficients
    coefficients = np.flip(coefficients) # flip coefficients before adding to matrix
    
    state_matrix = np.zeros((deg-1, deg-1))
    state_matrix[-1, 0:] = -coefficients
    state_matrix[:-1, 1:] = np.eye(deg-2)
    
    
    return state_matrix, input_matrix
    

degree = 7
coefs = np.random.rand(degree) #[ak a(k-1) ... a0]
b0 = np.random.rand()
state_m,input_m =  constructStateSpace(coefs)
def input_func(x,t):
    return b0

from scipy.integrate import odeint
from typing import Tuple

def constructLabels(var:str, cnt:int) -> Tuple[str]:
    # Utility function to make labels.
    # Ex: var = x, cnt = 2. Return = ("x", "x'")
    # this function renders poorly in lstlisting, see the source code
    # ...
    res = []
    for i in range(0, cnt):
        res.append(f"""{var}{"'"*i}""")
    return tuple(res)
    
def StateSpace(x,t):
    return state_m.dot(x) + input_m * input_func(x,t)

time = np.linspace(0,100,10000)
x0 = np.asarray([-1, 5]) # x, x'

solution = odeint(StateSpace, x0, time)

lines=plt.plot(time, solution)
plt.legend(lines, constructLabels("x", len(lines)))
plt.xlabel('time')
plt.show()

n = len(coefs) 
def LinODE(x, t):
    dx = np.zeros(n-1)
    dx[0] = state_m[-1].dot(x) + input_func(x,t)
    dx[1:] = x[0:(n-2)]
    return dx
    
solution_ode = odeint(LinearODE, np.flip(x0), time)
lines=plt.plot(time, solution_ode)
plt.legend(lines, reversed(constructLabels("x", len(lines))))
plt.xlabel('time_ode')
plt.show()