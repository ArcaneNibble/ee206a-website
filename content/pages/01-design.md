Title: Design
Date: 2017-12-08

##Design Criteria and Desired Functionality

The goal for the MEng capstone project is to build a system that:

* Is an add-on system that can be easily retrofitted to a normal E-bike. It
  should not change the physical structure of a E-bike and should not affect a
  human's ability to control the bike.
* Does not significantly increase the power consumption of the E-bike.
* Successfully stabilizes the bike.

In the context of EE206A, the goal was to prototype control algorithms for such
a bike. Therefore, we wanted to build a model of a bike with a controller that
could:

* Stabilize a bike while traveling at a "high" speed
* Stabilize a bike while traveling at near-zero speed
* Make the bike slowly follow a line
 
##Design Details
###System Overview
Due to time constraints, we are not yet able to build a "real" E-bike. For
this class, we have built a model bike using LEGO EV3 parts. Our hardware
platform is heavily based on an
[existing design](https://www.mathworks.com/matlabcentral/fileexchange/58231-lego-mindstorms-ev3-bike-project)
built by students at the University of Florence (however, the software platform
is completely different and described in the "implementation" section). This
model still allows us to test control algorithms, and it should still be
possible to achieve the desired features.

We built a fairly-typical digital feedback control system centered around a
CPU connected to sensors and actuators. We use a MEMS IMU to sense the lean
angle of the bike as well as its derivative. Because our model is built using
the LEGO EV3 system, we use a EV3 "medium" motor to actuate the fork of the
bike. This motor can also be used to sense the steer angle and its derivative.
We use an EV3 "large" motor to control the rear wheel on our model
bike. On a real E-bike, this is instead done with a hub motor. A block diagram
of the system is shown below.

This design (both the EV3 model and the modifications needed for future "real"
E-bike that will be built for the MEng project) uses cheap and
commonly-available parts, and most of the design criteria are easily met.
However, when we were working on building the control algorithms, we discovered
that the method of actuating the fork on the model EV3 bike does not work very
well. The friction introduced by adding a motor to the fork significantly
affects the behavior of the bike. Adding a motor in this way is simple, but it
will need to be improved on the "real" bike. This will be described in more
detail in the "results" section.

![System block diagram]({filename}/static/Design_fig1.png)

###Linearized Bike Model
Our controller design is based on a linearized bike model described in the
paper "Linearized dynamics equations for the balance and steer of a bicycle: a
benchmark and review" by Meijaard et al. This model is linearized around the
steady state with the bike straight up and moving forward at a constant velocity
$v$. This model has two major assumptions: that the contact between
the wheels and the ground is an ideal "knife-edge rolling point contact," and
that there is negligible friction on the steering axis. This model divides the
bike into four rigid parts: rear wheel (R frame), rear frame (B frame), front
frame (H frame), and front wheel (F frame) as shown in this diagram taken from
the paper:

![Bike model]({filename}/static/Design_fig2.png)

The bike then can be characterized using the physical parameters of the four
parts as shown in the table below.

![Bike parameter table]({filename}/static/Design_fig3.png)

According to the paper, the linearized equation of bike motion can be summarized as follow:

$$M\begin{bmatrix}\ddot{\theta}\\\ddot{\delta}\end{bmatrix} + vC_1\begin
{bmatrix}\dot{\theta}\\\dot{\delta}\end{bmatrix} + [gK_0 + v^2K_2]\begin
{bmatrix}\theta\\\delta\end{bmatrix} = \begin{bmatrix}T_\theta\\T_\delta\end
{bmatrix}$$

Where $\theta$ is the lean angle and $\delta$ is the steer angle, and $M$,
$C_1$, $K_0$, $K_2$ are constant matrices and can be calculated using the 25
bike parameters as shown in Appendix A of the paper.

For the design, we have chosen to use a linearized dynamics model because linear
models are usually simpler to understand and easier to compute with. Many
real-life control systems also operate with linearized models. However, the
trade-off is that this linear model is only linearized around one point. If the
lean and the steer angle is too big, the linearized equation does not describe
the dynamics of the bike anymore.

###State Space Model
We use the standard technique to convert the equation to a first order state
space model. We choose our state "x" to be the lean/steer angle and their
derivatives and construct a model as follow:

$$x=\begin{bmatrix}\theta\\\delta\\\dot{\theta}\\\dot{\delta}\end{bmatrix} \quad
\dot{x}=\begin{bmatrix}\theta\\\delta\\\ddot{\theta}\\\ddot{\delta}\end{bmatrix} \quad
\dot{x}=Ax+Bu$$

Where "u" is the input we are applying on steering using the steering motor.
Since there is no external torque applied on lean angle axis and the external
torque on steer angle is determined by our input. We can calculate the matrix
A and B using the second order linearized equation:

$$A = \begin{bmatrix}0_{2x2} & I_{2x2} \\ -M^{-1}K & -M^{-1}C\end{bmatrix} \quad
B = \begin{bmatrix}0_{2x2} \\ -M^{-1}\begin{bmatrix}0 \\ 1\end{bmatrix}\end{bmatrix}$$

Next, since the control on a microcontroller is in discrete time, we convert
our state model to discrete time:

$$A_d = e^{A\Delta t} \quad
B_d = \int_0^{\Delta t} e^{A\tau}B d\tau \quad
x[n+1] = A_d x[n] + B_d u[n]$$

Ideally, the sample rate of the system would be chosen to be fast enough so that
the system can respond to all of the dynamics that may exist in the physical
system. However, for our project, we chose to write the software using
Linux and Python. This limited our maximum achievable sample rate.

###Linear Quadratic Regulator (LQR) Control
For this project, we chose to use LQR control. The basic block diagram of a
system with LQR control is shown below.

![LQR diagram]({filename}/static/Design_fig8.png)

LQR is a strategy for designing a state-feedback control system. It results
in a control strategy of the form $$u_k = -Kx_k$$ The algorithm
calculates an ideal proportional constant matrix $K$ that minimizes the
cost function $$J = \sum_{k=0}^{\infty} (x_k^TQx_k + u_k^TRu_k)$$ based on the
$Q$ and $R$ design parameters we choose. As is common, we choose $Q$ to be a
diagonal matrix. The value on the diagonal of $Q$ indicates the weight
of each input and the value of $R$ indicates the weight of the control output.
The figure below shows one set of weights we choose for our system:

![LQR code]({filename}/static/Design_fig9.png)

For this project, we chose to use LQR control because it is a commonly-used
technique. Some alternatives that can be used instead include pole placement
techniques. LQR was chosen because we were most familiar with that technique.
