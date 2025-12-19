import utils
import numpy as np
import argparse

"""
command line args:
-t, --test = name of test to be performed (optional, if excluded, all tests are performed)

"""

# test quat to rotation matrix
def test_q2R():
    print("Testing q to R conversion.")
    print()
    print("Rotation example of 60 deg (x), 30 deg (y).")
    q_test = np.array([0.482963, 0.224144, 0.129410, 0.836516])
    q_test = q_test/np.linalg.norm(q_test)
    print("Test q: " + str(q_test))
    R_test = utils.q2R(q_test)
    print("Resulting R: ")
    print(R_test)
    print()
    print()

# test quat to angle-axis matrix
def test_q2aa():
    print("Testing q to aa conversion.")
    print()
    print("Rotation example of 60 deg (x), 30 deg (y).")
    q_test = np.array([0.482963, 0.224144, 0.129410, 0.836516])
    q_test = q_test/np.linalg.norm(q_test)
    print("Test q: " + str(q_test))
    aa_test = utils.q2aa(q_test)
    print("Resulting aa: ")
    print(aa_test)
    print()
    print()

def test_Rsingle():
    print("Testing single R rotations.")
    print()
    print("Rotation angle example = 60 deg.")
    angle = 60
    Rx_test = utils.R_x(angle)
    Ry_test = utils.R_y(angle)
    Rz_test = utils.R_z(angle)
    print("Resulting R_x:")
    print(Rx_test)
    print("Resulting R_y:")
    print(Ry_test)
    print("Resulting R_z:")
    print(Rz_test)
    print()
    print()

def test_R2q():
    print("Testing R to q rotations.")
    print()
    print("Rotation example of 60 deg (x), 30 deg (y), 50 deg (z)")
    angle_x = 60
    angle_y = 30
    angle_z = 50
    R = utils.eul2R(angle_x, angle_y, angle_z)
    q = utils.R2q(R)
    print("Resulting q:")
    print(q)
    print()
    print()

def test_eul2R():
    print("Testing eul to R conversion")
    print()
    print("Rotation example of 60 deg (x), 30 deg (y), 50 deg (z)")
    angle_x = 60
    angle_y = 30
    angle_z = 50
    R = utils.eul2R(angle_x, angle_y, angle_z)
    print("Resulting R:")
    print(R)
    print()
    print()

def test_aa2q():
    print("Testing angle-axis to quaternion conversion.")
    print()
    print("Rotation example of 60 deg (x), 30 deg (y), 50 deg (z)")
    e_x = 0.749131
    e_y = -0.001359
    e_z = 0.662421
    angle = 90.591018
    aa = np.array([e_x, e_y, e_z, angle])
    aa[0:3] = aa[0:3]/np.linalg.norm(aa[0:3])
    print("Test angle-axis:")
    print(aa)
    q = utils.aa2q(aa)
    print("Resutling q:")
    print(q)
    print()
    print()



def test(test_name):

    # set print output to normal notation, 6 decimal places
    np.set_printoptions(suppress=True, formatter={'float_kind':'{:0.6f}'.format})

    if (test_name == "q2R"): 
        test_q2R()

    elif (test_name == "q2aa"):
        test_q2aa()

    elif (test_name == "Rsingle"):
        test_Rsingle()

    elif (test_name == "eul2R"):
        test_eul2R()

    elif (test_name == "R2q"):
        test_R2q()

    elif (test_name == "aa2q"):
        test_aa2q()

    else:
        print("Performing all tests.")
        print()
        test_q2R()
        test_q2aa()
        test_Rsingle()
        test_eul2R()
        test_R2q()
        test_aa2q()


if __name__ == "__main__":
    
    # command line parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', default = "")
    args = parser.parse_args()

    test(args.test)
