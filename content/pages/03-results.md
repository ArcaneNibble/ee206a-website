Title: Results
Date: 2017-12-08

##Eigenvalues of the system when no control applied
We plot out the real parts of the eigenvalues of the system at different velocity when no control is applied(Figure 1). We can see that, in theory, the bike can actually balance itself without a control when the speed is in range [2.672, 4.647] m/s. However, this speed range is unreachable for our device and is too large for our design criteria. For the velocity we choose to run our system(0.6 m/s), the system is unstable if no control is applied.

![Eigenvalue vs speed graph]({filename}/static/Results_fig1.png)

##Controllabilty Check
We check the controllability by calculating the A and B matrices at different velocity. As the result, in theory, the system is controllable in speed range [0, 5] m/s (Figure 2).

![Controllability vs speed graph]({filename}/static/Results_fig2.png)

##Simulation Result
We simulate the system when the lean angle starts at 10 degrees leaning to the left and the forward velocity is 0.644 m/s. As shown in Figure 3, our LQR control works and lean and steer angle stabilize to 0.

![Simulation graph]({filename}/static/Results_fig3.png)

##Deployment Result
However, our deployment result does not work perfectly, but the bike does tries to balance itself.
youtube link: https://youtu.be/BEyYEvRrz-Q
