import utils
import numpy as np
import argparse 
import target_class
import scipy
from scipy.integrate import odeint
import math

"""
command line args:
-total_t = total simulation time, sec
-dt = integration step interval, sec
-x = initial euler angle x, deg
-y = initial euler angle y, deg
-z = initial euler angle z, deg
-wx = initial angular velocity, deg/s
-wy = initial angular velocity, deg/s
-wz = initial angular velocity, deg/s
-Lx = initial torque (x), N-m
-Ly = initial torque (y), N-m
-Lz = initial torque (z), N-m

euler angles in X --> Y --> Z order

initial values from old thesis on angular velocity: [0, 3.53, 3.53] deg/s

apply torques?

"""

# main tumbling function
def tumble(total_t, dt, x, y, z, wx, wy, wz, Lx, Ly, Lz):
	# initialize target
	target = target_class.Target()
	target.state[0:4] = utils.R2q(utils.eul2R(x, y, z))
	
	# if comparing to thesis trajectory of envisat
	target.state[0] = 0.622
	target.state[1] = 0.307
	target.state[2] = -0.449
	target.state[3] = -0.564


	target.state[4:7] = np.array([wx, wy, wz])
	target.torque = np.array([Lx, Ly, Lz])

	# initialize dynamics integration
	t = 0 # step
	total_steps = round(total_t / dt)

	# initialize tumbling data
	state_data = np.zeros((total_steps, 7))
	state_data[0][:] = target.state
	torque_data = np.zeros((total_steps, 3)) # future could have a pre-set torque dataset
	torque_data[0][:] = target.torque 
	t_data = np.zeros(total_steps)

	# overall loop for tumbling
	for i in range(0, total_steps - 1):
		# integrate tumbling step
		t0 = t
		tf = t + dt
		x = target.state
		L = target.torque
		J = target.J
		Jinv = target.Jinv
		x_prop = scipy.integrate.odeint(eqom, x, np.array([t0, tf]), args=(J, Jinv, L))

		# update states
		target.state = x_prop[1]
		target.state[0:4] = target.state[0:4]/np.linalg.norm(target.state[0:4])
		t = t + dt

		# update tumbling data
		state_data[i + 1][:] = target.state
		t_data[i + 1]= t
		target.torque = torque_data[i + 1][:]

	# save tumbling data
	# set print output to normal notation, 6 decimal places
	np.set_printoptions(suppress=True, formatter={'float_kind':'{:0.6f}'.format})

	print("State data: ")
	print(state_data)
	print()
	print()




# equations of motion for integration step
def eqom(x, t, J, Jinv, L):
	q = x[0:4]
	w = x[4:7] * 2*math.pi/360

	# quaternion kinematics
	B = np.array([[0,     w[2], -w[1],  w[0]],
		 		  [-w[2], 0,     w[0],  w[1]],
		 		  [w[1],  -w[0], 0,     w[2]],
		 		  [-w[0], -w[1], -w[2], 0]])
	qdot = 0.5 * B @ q


	# Euler's dynamics
	wdot = Jinv @ (L - np.cross(w, J @ w))
	wdot = wdot * 360/(2*math.pi)

	xdot = np.zeros(7)
	xdot[0:4] = qdot
	xdot[4:7] = wdot
	return xdot



if __name__ == "__main__":
    
    # command line parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-total_t', type=float, default = 120)
    parser.add_argument('-dt', type=float, default = 0.1)
    parser.add_argument('-x', type=float, default = 0.)
    parser.add_argument('-y', type=float, default = 0.)
    parser.add_argument('-z', type=float, default = 0.)
    parser.add_argument('-wx', type=float, default = 0.)
    parser.add_argument('-wy', type=float, default = 3.53)
    parser.add_argument('-wz', type=float, default = 3.53)
    parser.add_argument('-Lx', type=float, default = 0.)
    parser.add_argument('-Ly', type=float, default = 0.)
    parser.add_argument('-Lz', type=float, default = 0.)
    args = parser.parse_args()

    tumble(args.total_t, args.dt, args.x, args.y, args.z, args.wx, args.wy, args.wz, args.Lx, args.Ly, args.Lz)


