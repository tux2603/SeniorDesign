from pca9685 import PCA9685
from time import sleep

if __name__ == '__main__':
    motor_control = PCA9685(0x40, debug=False)
    motor_control.setPWMFreq(50)

    while True():
        for i in range(500, 2500, 10):
            motor_control.setServoPulse(0, i)
            motor_control.setServoPulse(1, 3000 - i)
            sleep(0.02)

        for i in range(2500, 500, -10):
            motor_control.setServoPulse(0, i)
            motor_control.setServoPulse(1, 3000 - i)
            sleep(0.02)

        