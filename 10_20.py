from utils import preprocess
import numpy as np
import time
import math

STEERING_GAIN = 1.0

STEERING_BIAS = 0.05


car.throttle = 0.2

pre_x = 0
d = 1.1
cnt = 0
past = 0
v = 12

while True:
    image = camera.read()
    image = preprocess(image).half()
    output = model_trt(image).detach().cpu().numpy().flatten()
    x = float(output[0])
    error = float(output[1])
    #print(error)
    y = -1 / (0.9 * math.cos(1.4 * x)) + 3.1
    y /= 10
    #print(x)
    
    if abs(x) < 0.03:
        x = 0
    
    if error < -0.66:
        y = 0.06
        cnt = 0
    elif error > 0.66:
        y = 0.3
        cnt += 1
    else:
        y = 0.11
        cnt = 0
        
    if cnt > v and cnt < 100:
        print("hi")
        y = 0.07
    
    '''
    if abs(x) > 0.3 and abs(x) < 0.7 and error < - 0.66:
        #print("hhi")
        y = 0.09
    if abs(x) > 0.3 and abs(x) < 0.7 and error >= - 0.66 and error <= 0.66:
        #print("hhhi")
        y = 0.1
    '''

    if y < 0.06:
        car.throttle = 0.06
    else:
        car.throttle = y
        
        '''
    if -0.12 < x < 0.12:
        car.throttle = 0.2
    elif x > 0.95 or x < -0.95:
        car.throttle = 0.03
    elif x > 0.7 or x > -0.7:
        car.throttle = 0.045
    else:
        car.throttle = 0.085 
'''
    
    car.steering = -(STEERING_GAIN * x + d * (x - pre_x) + STEERING_BIAS)
        
    pre_x = x
