Title: Results
Date: 2017-12-08

##Eigenvalues of the system when no control applied
We plot out the real parts of the eigenvalues of the system at different
velocity when no control is applied. We can see that, in theory, the bike can
actually balance itself without a control when the speed is in range [2.672,
4.647] m/s. However, this speed range is unreachable for our device and is too
large for our design criteria. For the velocity we choose to run our system 
(0.6 m/s), the system is unstable if no control is applied.

![Eigenvalue vs speed graph]({filename}/static/Results_fig1.png)

##Controllabilty Check
We calculated the $A$ and $B$ matrices at various velocities and checked
the controllability of the system by using the controllability rank test. From
this test, we find that, in theory, the system is controllable at all speeds in
the tested speed range of [0, 5] m/s. Note that in theory the system is even
controllable at 0 speed.

![Controllability vs speed graph]({filename}/static/Results_fig2.png)

##Simulation Result
We built a number of simulation tools to test if our controller would work in
theory. The first simulation tool operated in continuous time using SciPy's
numerical integration tools. The second simulator simulates discrete-time
behavior and is implemented as a simple loop with a difference equation.

In the below plot, we simulate the system when the lean angle starts at 0.10
radians leaning to the left and the forward velocity is 0.644 m/s. As shown
below, our LQR control works and lean and steer angle stabilize to 0.

![Simulation graph]({filename}/static/Results_fig3.png)

##Deployment Result
However, our deployment result does not work perfectly, but the bike does tries to balance itself.

<iframe width="800" height="600" src="https://www.youtube.com/embed/BEyYEvRrz-Q"></iframe>
