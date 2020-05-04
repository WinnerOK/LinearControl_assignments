# LQR
Q =   np.array([
                   [1,0,0,0],
                   [0,1,0,0],
                   [0,0,1,0],
                   [0,0,0,1]
])

R = np.array([
              [10, 0],
              [0, 10],
])

L_lqr = lqr(A.T, C.T, Q, R).T

# Pole placement
desired_poles = [-1, -2, -3, -4]
pole = place_poles(A.T, C.T, desired_poles)
L_pole = pole.gain_matrix.T


L = L_lqr  # Change this var to work with calculations of L matrix
def system (x, t):
  ret = (A - B.dot(k)).dot(x)
  if NOISE_DYNAMICS:
    ret += NOISE_SCALE_DYNAMICS * np.random.randn(*(ret.shape)) 
  
  return ret

def luenberg(x_est, t, u, y):
  y_diff = y - C.dot(x_est).reshape((2, ))

  Ax = A.dot(x_est)
  Bu = B.dot(u).reshape((4, ))
  Ly_diff = L.dot(y_diff)
  
  ret = Ax + Bu + Ly_diff
  return ret

time_start = 0
time_finish = 10
time_step = 0.01

x_0 = 0.5
ang_0 = pi/3
diff_x_0 = 0.01
diff_ang_0 = pi/12

x_0_est = 0.5
ang_0_est = pi/6
diff_x_0_est = 0.07
diff_ang_0_est = pi/8

labels = ["x(t)", "theta(t)", "x'(t)", "theta'(t)"]

time = np.arange(time_start, time_finish, time_step)
x = [np.array([x_0, ang_0, diff_x_0, diff_ang_0])]
x_obs = [np.array([x_0_est, ang_0_est, diff_x_0_est, diff_ang_0_est])]

k = place_poles(A, B, desired_poles).gain_matrix

for real_x in np.array(list(RungeKutta(system, x[0], time))):
 x.append(real_x)
  # This trick with odeint was suggested by students of 4th group in order not to
  # implement custom numeric solver but at the same time pass to the observer
  # values from "sensors"
  local_time = np.array([time[i-1], time[i]])

  y = C.dot(x[-1])
  if NOISE_OUTPUT:
    y += NOISE_SCALE_OUTPUT * np.random.randn(*(y.shape))
  
  sensor_data.append(y)
  
  u = -k.dot(x_obs[-1])
  # u = np.array([0])  # uncomment to work with uncontrolled
  x_obs_dot = odeint(luenberg, x_obs[-1], local_time, args=(u, y))
  x_obs.append(x_obs_dot[-1])

x = np.array(x)
x_obs = np.array(x_obs)
error = np.absolute(x - x_obs)
plt.plot(time, error)
plt.xlabel('time')

plt.legend(list(map(lambda x: x + " err", labels)))
plt.show()