import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.linalg import inv, solve_continuous_are
from math import pi

def lqr(A, B, Q, R):
  """
  dx/dt = Ax+ Bu

  J = integral of x.T * Q * x + u.T *R * u
  """
  # solve Algebraic Riccati equation
  S = solve_continuous_are(A, B, Q, R)
  
  # Compute gain 
  K = inv(R) * B.T.dot(S)

  return np.asarray(K)

time_start = 0
time_finish = 7
time_step = 0.01

x_0 = 100
ang_0 = 0
diff_x_0 = 0
diff_ang_0 = 100

labels = ["x(t)", "theta(t)", "x'(t)", "theta'(t)"]

time = np.arange(time_start, time_finish, time_step)
init = [x_0, ang_0, diff_x_0, diff_ang_0]
init_obs = [x_0 + 5, ang_0 + pi/6, diff_x_0, diff_ang_0]

Q = np.eye(4) * 100
R = np.eye(1)
k = lqr(A, B, Q, R)

def u(x, t):
  return -k.dot(x)

def differential(x, t):
  Ax = A.dot(x)
  Bu = B.dot(u(x, t))
  ret = Ax + Bu
  return ret


real = odeint(differential, init, time)
observed = odeint(differential, init_obs, time)
error =  np.absolute(real - observed)

plt.plot(time, error)
plt.xlabel('time')
plt.legend(list(map(lambda x: x + " err", labels)))
plt.show()
