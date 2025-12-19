import utils
import numpy as np  

class Target(object):

	def __init__(self):
		# inertia (kg*m^2) (Envisat)
		Jxx = 17023.3
		Jxy = 397.1
		Jxz = -2171.4
		Jyx = 397.1
		Jyy = 124825.7
		Jyz = 344.4
		Jzx = -2171.4
		Jzy = 344.2
		Jzz = 129112.2
		self.J = np.array([[Jxx, Jxy, Jxz], 
						   [Jyx, Jyy, Jyz], 
						   [Jzx, Jzy, Jzz]])
		self.Jinv = np.linalg.inv(self.J)

		# state
		self.state = np.zeros(7)

		# initial orientation (q)
		self.state[0] = 0. # qx
		self.state[1] = 0. # qy
		self.state[2] = 0. # qz
		self.state[3] = 1. # qw

		# initial angular velocity (deg/s)
		self.state[4] = 0. # wx
		self.state[5] = 0. # wy
		self.state[6] = 0. # wz

		# torque
		self.torque = np.zeros(3)
