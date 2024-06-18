from controller import Robot

# time in [ms] of a simulation step
TIME_STEP = 64

# initialize the Webots API
robot = Robot()

# internal variables
avoid_obstacle_counter = 0

# initialize distance sensors
ds_names = ['ds_left', 'ds_right']
ds = [robot.getDevice(ds_name) for ds_name in ds_names]
for sensor in ds:
    sensor.enable(TIME_STEP)

# initialize motors
wheels_names = ['wheel1', 'wheel2']
wheels = [robot.getDevice(wheel_name) for wheel_name in wheels_names]
for wheel in wheels:
    wheel.setPosition(float('inf'))

# feedback loop
while robot.step(TIME_STEP) != -1:
    # init speeds
    left_speed = 1.0
    right_speed = 1.0
    
    if avoid_obstacle_counter > 0:
        avoid_obstacle_counter -= 1
        left_speed = 1.0
        right_speed = -1.0
    else:
        # read sensors outputs
        ds_values = [ds_sensor.getValue() for ds_sensor in ds]

        # increase counter in case of obstacle
        if ds_values[0] < 950.0 or ds_values[1] < 950.0:
            print(f"ds_values[0] is: {ds_values[0]}")
            print(f"ds_values[1] is: {ds_values[1]}")
            avoid_obstacle_counter = 100

    # write actuators inputs
    for i in range(2):
        if i % 2 == 0:
            wheels[i].setVelocity(left_speed)
        else:
            wheels[i].setVelocity(right_speed)