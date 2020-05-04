
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import pi

time_start = 0
time_finish = 1
time_step = 0.01

x_0 = 100
ang_0 = 0
diff_x_0 = 0
diff_ang_0 = 100

labels = ["x(t)", "theta(t)", "x'(t)", "theta'(t)"]

time = np.arange(time_start, time_finish, time_step)
init = [x_0, ang_0, diff_x_0, diff_ang_0]

init_obs = [x_0 + 5, ang_0 + pi/6, diff_x_0, diff_ang_0]

def u(t):
  return 1

def differential(x, t):
  Ax = A.dot(x)

  Bu = B.dot(u(t))
  Bu = Bu.reshape(Bu.shape[0])  # original shape is (4, 1) instead of just (4, )

  ret = Ax + Bu
  return ret

real = odeint(differential, init, time)
observed = odeint(differential, init_obs, time)
error =  np.absolute(real - observed)

plt.plot(time, error)
plt.xlabel('time')

plt.legend(list(map(lambda x: x + " err", labels)))
plt.show()