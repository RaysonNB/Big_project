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
    if -0.12 < x < 0.12:
        car.throttle = 0.2
    elif x > 0.95 or x < -0.95:
        car.throttle = 0.03
    elif x > 0.7 or x > -0.7:
        car.throttle = 0.045
    else:
        car.throttle = 0.085 
    
    car.steering = -(STEERING_GAIN * x + d * (x - pre_x) + STEERING_BIAS)
        
    pre_x = x
