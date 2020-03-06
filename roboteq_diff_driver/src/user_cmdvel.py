#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16MultiArray
#from geometry_msgs.msg import Accel

import sys, select, termios, tty

MOTOR_MAX_LINEAR_VEL = 20
MOTOR_MAX_ANGULAR_VEL = 20

MOTOR_MIN_LINEAR_VEL = -20
MOTOR_MIN_ANGULAR_VEL = -20

msg = """
Control Your Motor
---------------------------
MOTOR_MAX_LINEAR_VEL = 20
MOTOR_MAX_ANGULAR_VEL = 20

MOTOR_MIN_LINEAR_VEL = -20
MOTOR_MIN_ANGULAR_VEL = -20

space key: force stop
x : init

CTRL-C to quit
----------------------------
"""

e = """
Communications Failed
"""

def getLinearKey():
    key = input("Enter the linear speed you want  ")
    return key


def getAngularKey():
    key = input("Enter the angular speed you want  ")
    return key


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def constrain(input, low, high):
    if input < low:
        input = low
    elif input > high:
        input = high
    else:
        input = input

    return input

def checkLINEARLimitVelocity(vel):
    vel = constrain(vel, MOTOR_MIN_LINEAR_VEL, MOTOR_MAX_LINEAR_VEL)
    return vel

def checkANGULARLimitVelocity(vel):
    vel = constrain(vel, MOTOR_MIN_ANGULAR_VEL, MOTOR_MAX_ANGULAR_VEL)
    return vel

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    pub = rospy.Publisher('motor_teleop_cmd_vel', UInt16MultiArray, queue_size=10)
    rospy.init_node('motor_teleop',anonymous=True)

    teleop_int = UInt16MultiArray()
    teleop_int.data = [0,0]
    status = 0
    target_linear_vel = 0   # initialize linear vel
    target_angular_vel = 0 # initialize angular vel
    try:
        print msg
        while not rospy.is_shutdown():
            linear_key = getLinearKey()

            target_linear_vel = checkLINEARLimitVelocity(linear_key)

            angular_key = getAngularKey()
            target_angular_vel = checkLINEARLimitVelocity(angular_key)
            
            print vels(target_linear_vel,target_angular_vel)
            status += 1
            if status == 20 :
                print msg
                status = 0

            teleop_int.data[0] = target_linear_vel
            teleop_int.data[1] = target_angular_vel
            pub.publish(teleop_int)

    except rospy.ROSInterruptException:
        pass

    finally:
        pub.publish(teleop_int)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
