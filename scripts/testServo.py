import RPi.GPIO as GPIO
import pigpio
import time

servoPIN = 23
pwm = pigpio.pi()
pwm.set_mode(servoPIN, pigpio.OUTPUT)

pwm.set_PWM_frequency(servoPIN, 50)
time.sleep(0.5)

def SetAngle(angle):
    pwm.set_servo_pulsewidth(servoPIN, 500 + (angle * 11.11))
    # time.sleep(0.5)

def Stop():
    pwm.set_servo_pulsewidth(servoPIN, 0)
    pwm.set_PWM_frequency(servoPIN, 0)
# try:
#     while True:
#         #Ask user for angle and turn servo to it
#         angle = float(input('Enter angle between 0 & 180: '))
#         p.ChangeDutyCycle(2+(angle/18))
#         time.sleep(0.5)
#         p.ChangeDutyCycle(0)
# finally:
#     #Clean things up at the end
#     p.stop()
#     GPIO.cleanup()
#     print("Servo Stop")


SetAngle(0)
time.sleep(2)

for i in range(0, 20):
    SetAngle(i)
    time.sleep(0.5)
    Stop()

# pwm.set_PWM_frequency(servoPIN, 0)

