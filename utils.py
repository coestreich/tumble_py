# Functions for attitude dynamics calculations
# q format = [qx, qy, qz, qw]
# axis-angle format = [ax, ay, az, angle]
# euler angles in X --> Y --> Z order
# angles taken in degrees

import numpy as np
import math

# quaternion to rotation matrix
# tested successfully 12/18/25
def q2R(q):
	qw = q[3]
	qx = q[0]
	qy = q[1]
	qz = q[2]
	R = np.zeros((3,3))
	R[0,0] = qw**2 + qx**2 - qy**2 - qz**2
	R[0,1] = 2*(qx*qy + qw*qz)
	R[0,2] = 2*(qx*qz - qw*qy)
	R[1,0] = 2*(qx*qy - qw*qz)
	R[1,1] = qw**2 - qx**2 + qy**2 - qz**2
	R[1,2] = 2*(qy*qz + qw*qx)
	R[2,0] = 2*(qx*qz + qw*qy)
	R[2,1] = 2*(qy*qz - qw*qx)
	R[2,2] = qw**2 - qx**2 - qy**2 + qz**2
	R = R.transpose()

	return R

# quaternion to angle-axis
# tested succesfully 12/18/25
def q2aa(q):
	qw = q[3]
	qx = q[0]
	qy = q[1]
	qz = q[2]
	alpha = 2*math.atan2(math.sqrt(qx**2 + qy**2 + qz**2), qw)
	alpha = alpha*360/(2*math.pi) # convert from radians to degrees
	ax = qx/math.sqrt(qx**2 + qy**2 + qz**2)
	ay = qy/math.sqrt(qx**2 + qy**2 + qz**2)
	az = qz/math.sqrt(qx**2 + qy**2 + qz**2)
	aa = np.array([ax, ay, az, alpha])
	aa[0:3] = aa[0:3]/np.linalg.norm(aa[0:3])
	return aa


# X-axis rotation matrix
# tested successfully 12/18/25
def R_x(angle):
	angle = angle*2*math.pi/360
	R = np.zeros((3,3))
	R[0,0] = 1.
	R[0,1] = 0.
	R[0,2] = 0.
	R[1,0] = 0.
	R[1,1] = math.cos(angle)
	R[1,2] = -math.sin(angle)
	R[2,0] = 0.
	R[2,1] = math.sin(angle)
	R[2,2] = math.cos(angle)
	return R

# Y-axis rotation matrix
# tested successfully 12/18/25
def R_y(angle):
	angle = angle*2*math.pi/360
	R = np.zeros((3,3))
	R[0,0] = math.cos(angle)
	R[0,1] = 0.
	R[0,2] = math.sin(angle)
	R[1,0] = 0.
	R[1,1] = 1.
	R[1,2] = 0.
	R[2,0] = -math.sin(angle)
	R[2,1] = 0.
	R[2,2] = math.cos(angle)
	return R

# Z-axis rotation matrix
# tested successfully 12/18/25
def R_z(angle):
	angle = angle*2*math.pi/360
	R = np.zeros((3,3))
	R[0,0] = math.cos(angle)
	R[0,1] = -math.sin(angle)
	R[0,2] = 0.
	R[1,0] = math.sin(angle)
	R[1,1] = math.cos(angle)
	R[1,2] = 0.
	R[2,0] = 0.
	R[2,1] = 0.
	R[2,2] = 1.
	return R

# Rotation matrix to quaternion
# tested successfully 12/18/25
def R2q(R):
	tr = R[0,0] + R[1,1] + R[2,2]
	if (tr > 0):
		S = math.sqrt(tr + 1) * 2
		qw = 0.25 * S
		qx = (R[2,1] - R[1,2]) / S
		qy = (R[0,2] - R[2,0]) / S
		qz = (R[1,0] - R[0,1]) / S
	elif (R[0,0] > R[1,1] and R[0,0] > R[2,2]):
		S = math.sqrt(1 + R[1,1] - R[2,2] - R[3,3]) * 2
		qw = (R[2,1] - R[1,2]) / S
		qx = 0.25 * S
		qy = (R[0,1] + R[1,0]) / S
		qz = (R[0,2] + R[2,0]) / S
	elif (R[1,1] > R[2,2]):
		S = math.sqrt(1 + R[1,1] - R[0,0] - R[2,2]) * 2
		qw = (R[0,2] - R[2,0]) / S
		qx = (R[0,1] + R[1,0]) / S
		qy = 0.25 * S
		qz = (R[1,2] + R[2,1]) / S
	else:
		S = math.sqrt(1 + R[2,2] - R[0,0] - R[1,1]) * 2
		qw = (R[1,0] - R[0,1]) / S
		qx = (R[0,2] + R[2,0]) / S
		qy = (R[1,2] + R[2,1]) / S
		qz = 0.25 * S
	q = np.array([qx, qy, qz, qw])
	q = q / np.linalg.norm(q)
	return q


# Euler angles to rotation matrix
# tested successfully 12/18/25
def eul2R(angle_x, angle_y, angle_z):
	R = R_x(angle_x) @ R_y(angle_y) @ R_z(angle_z)
	return R

# Angle-axis to quaternions
# tested successfully 12/18/25
def aa2q(aa):
	alpha = aa[3]*2*math.pi/360
	ax = aa[0]
	ay = aa[1]
	az = aa[2]
	qx = ax*math.sin(alpha/2)
	qy = ay*math.sin(alpha/2)
	qz = az*math.sin(alpha/2)
	qw = math.cos(alpha/2)
	q = np.array([qx, qy, qz, qw])
	q = q / np.linalg.norm(q)
	return q







