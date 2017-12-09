Title: Design
Date: 2017-12-08

##Design Criteria

* The system should be an add-on system to a normal E-bike. It should not change
  the physical structure of a E-bike and should not distinctly affect human’s
  control when a human rider is on the bike.
* The sensors and actuators should not significantly increase the power
  consumption of the E-bike.
* The sensing and actuating should operate fast enough for the bike to balance
  itself.
 
##Desired functionality
The desired goal is to balance the E-bike when no human rider is on it while
moving at a relatively low speed(depends on the size of the bike)
 
##Design
###System overview
We add an IMU to sense the lean angle and its velocity, a microcontroller to read the sensor values and to command the actuators, a small motor to actuate the fork of the bike. The small motor can also be used to sense the steer angle and its velocity. Since the E-bikes already have a hub motor to actuate forward moving, we can connect the hub motor to our microcontroller to control the forward speed of the bike.The overview of the system is shown in Figure 1.
By choosing this kind of design, criteria (a)&(b) can be met: the system can be easily added to an existing E-bike, we can disable the control when human rider is on the bike, and the added parts does not significantly increase the power consumption. However, since we add a motor on the steering fork, rider’s control to the handle bar will be minorly affected.

![System block diagram]({filename}/static/Design_fig1.png)
 
###Linearized Bike Model
Our design is based on a linearized bike model characterized in the paper: “Linearized dynamics equations for the balance and steer of a bicycle: a benchmark and review”[1]. This model linearized the bike when it is straight up and moving forward at a constant velocity ‘v’. Two assumption this model makes are: knife-edge rolling point contact and negligible friction on steering axis. This model divides the bike into four rigid parts: rear wheel(R frame), rear frame(B frame), front frame(H frame), front wheel(F frame) as shown in Figure 2.

![Bike model]({filename}/static/Design_fig2.png)

The bike then can be characterized using the physical parameters of four parts shown in Table 1[1]. one unusual parameters is the trail of the bike which means the distance between the front wheel/ground contact point to the point where the axis of front fork and ground intersect.

![Bike parameter table]({filename}/static/Design_fig3.png)

According to the paper, the linearized equation of bike motion can be summarized as follow:

![Bike model equation]({filename}/static/Design_fig4.png)

Where θ is the lean angle and δ is the steer angle, M is the symmetric mass matrix, C1 captures gyroscopic torques due to lean and steer rate and inertial reaction due to steer rate, K0 and K2 define the stiffness matrix K. M, C1, K0, K2 are constant matrixes and can be calculated using the 25 bike parameters as shown in Appendix A of the paper. (The paper can be found in additional materials)
However, by using this model, we have to place the bike straight up every time we want to apply our control system. Also, if the lean and the steer angle is too big, the linearized equation does not describe the dynamics of the bike anymore. In real life scenario, we need to design a special stick stand to keep the bike straight up when it is at stationary. 

###State Based Model
We use standard technique to convert the equation to a first order state based model. We choose our state “x” to be the lean/steer angle and their derivatives and construct a model as follow:

![Bike state space equation]({filename}/static/Design_fig5.png)

Where “u” is the input we are applying on steering using the steering motor. Since there is no external torque applied on lean angle axis and the external torque on steer angle is determined by our input. We can calculate the matrix A and B using the second order linearized equation:

![Bike AB equation]({filename}/static/Design_fig6.png)

Next, since the control on a microcontroller is in discrete time, we convert our state model to discrete time:

![Bike discrete time equation]({filename}/static/Design_fig7.png)

The sampling rate and operating rate depend on the kind of sensors and microcontroller we choose to use in order to meet criteria (c).

###Linear Quadratic Regulator(LQR) Control
The basic block diagram of LQR control is shown in Figure 3.

![LQR diagram]({filename}/static/Design_fig8.png)

It is a closed loop proportional feedback system and it fits our state based model. The estimator calculates the proportional constant matrix ‘K’ based on the Q and R values we choose. The value on the diagonal of Q indicates the weight of each input and the value of R indicates the weight of the input. Figure 4 shows one set of weights we choose for our system:

![LQR code]({filename}/static/Design_fig9.png)

The estimator will calculate the optimal K which minizes the cost function:

![LQR equation]({filename}/static/Design_fig10.png)
![LQR equation]({filename}/static/Design_fig11.png)
