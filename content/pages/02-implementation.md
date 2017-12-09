Title: Implementation
Date: 2017-12-08

##Lego EV3 Mindstorm bike
For the scope of this project, we end up building a model of a E-bike using the Lego EV3 parts. We found a EV3 bike model from another students’ course project: “Control of a LEGO mindstorms EV3 bike model ”[2] and borrowed their hardware assembly. On the rear wheel, we have a EV3 “large” motor which work as the same as the hub motor of a normal E-bike. We have a EV3 controller brick as the microcontroller and a EV3 “medium” motor to actuate the steering. We add an non-EV3 IMUto sense the lean angle of the bike model. The hardware design is shown in Figure 1.

##MPU2950
We use this 9 Degree of Freedom(3-axis accelerometer, 3-axis gyroscope, 3-axis magnetometer) IMU to measure the lean angle and its velocity. It is shown as the New non-EV3 gyro in Figure 1 and the chip on the right in Figure 2. We use I2C communication between the IMU and the EV3 controller brick. With the 9 DOF, we can get the angular velocity of lean angle from the gyroscope measurement on x-axis.

We then use the algorithm from Madgwick[3] to process all data from the IMU to get the quaternion of the IMU and then calculate the lean angle from the quaternion. The basic idea of the algorithm is correct the noise of gyroscope using the values of accelerometers and magnetometers because gravitational acceleration always points vertically towards to the ground and magnetic field is parallel to the ground. The diagram showing the correction process is shown in Figure 3

##Software Environment: EV3 Dev and Python
We use the open sourced library called EV3 Dev which allow us to program our system in python. 

##Simulation
We first plot out the eigenvalues of the system when there is no control applied to it to make sure our system is unstable without a control system. Then, we check the controllability of our system to make sure it is controllable. Finally, we run software simulation based on the second order linearized model we used in the design part.

##Implementation in Software
1. Calculate the M, C1, K0, K2 matrixes based on the parameters and pick a
   forward velocity(≈0.6 m/s) for our system.
2. Calculate the A and B matrices and based on our parts, pick a sample rate
   (=20Hz). Using the sample rate, convert the matrices to discrete time Ad and
   Bd.
3. Using the weighting matrices Q and R, and discrete time LQR algorithm to
   calculate the optimal proportional factor K.
4. We define the state of the system as we stated in the design part. The four
   state variables can be observed by:
   Lean angle -- applying Magwick algorithm to the IMU values
   Steer angle -- reading the steer motor encoder
   Lean anglular velocity -- reading gyroscope on x-axis of the IMU
   Steer angular velocity -- calculate the change of the steer angle and divide
   by the sampling time
5. Actuate the steer motor based on the current state and the proportional
   factor K.

##Deployment
We deploy the code onto the EV3 controller brick. The file will first calibrate the sensors then apply a constant torque on the hub motor to ensure constant velocity. Then, the LQR control is applied as stated in part (e). A simple state diagram of the system is shown in Figure 4
