class KalmanFilter():
  def __init__(self, A, C, Q, R, B = None, P = None, x_init = None):

    self.n = A.shape[1]

    self.A = A
    self.B = 0 if B is None else B
    self.C = C
    self.Q = Q
    self.R = R
    self.P = np.eye(self.n) if P is None else P 
    self.x = np.zeros((self.n, )) if x_init is None else x_init

  def predict(self, u = np.array([0, ])):
    self.x = np.dot(self.A, self.x) + np.dot(self.B, u)
    self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q

  def update(self, y_sensor):
    y_diff = y_sensor - np.dot(self.C, self.x)
    K_denum = self.R + np.dot(self.C, np.dot(self.P, self.C.T))
    K = np.dot(np.dot(self.P, self.C.T), inv(K_denum))
    self.x = self.x + np.dot(K, y_diff)
    I = np.eye(self.n)
    self.P = np.dot(
        np.dot(I - np.dot(K, C), self.P),
        (I - np.dot(K, self.C)).T
    ) + np.dot(np.dot(K, self.R), K.T)
    return self.x