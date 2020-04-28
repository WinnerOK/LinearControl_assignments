import numpy as np
from numpy.linalg import matrix_power, matrix_rank

A = np.array([
               [0,0,      1,0],
               [0,0,      0,1],
               [0,5.7552, 0,0],
               [0,12.971, 0,0],
])

B = np.array([
               [0],
               [0],
               [0.133],
               [0.111],
])

C = np.array([
              [1, 0, 0, 0],
              [0, 1, 0, 0],
])

# finding observability matrix
O = np.concatenate(
    (
        C, 
        C.dot(A),
        C.dot(matrix_power(A, 2)),
        C.dot(matrix_power(A, 3)),
     )
)



