Title: Conclusions
Date: 2017-12-08

##Issues with the current implementation
As can be seen in our [video](https://youtu.be/BEyYEvRrz-Q), our bike does not
remain balanced. Although we pretty much did not achieve any of the tasks we set
out to achieve, this project was still beneficial. We learned about many of the
ways that this project can fail, and we know what we will need to focus on for
future work on the MEng capstone project.

###Mechanical problems
One major problem that we eventually discovered was that the steering axis on
our EV3 bike has a significant amount of friction. We think that this is because
of the following reasons:

* The motor attached to the steering axis has friction and loss. Even if the
  motor is not being actively driven, the friction is noticeable when turning
  the front steering by hand.
* The steering axle is one single LEGO beam that can bend and lose energy.

One factor that supports this hypothesis is that artificially inflating the
$\beta$ damping coefficient in the motor model appeared to improve the
performance (up to a point).

###Major hacks
####Motor model
Because neither of us were familiar with motor models, we copied the motor model
exactly from the design we were referencing. We did not attempt to measure
whether this motor model accurately matched reality. Given additional time (and
continuing into the next semester for the MEng project), we will study motor
models and how to construct a model from a physical motor.

####IMU does not use magnetometer
The magnetometer was causing severe drift in the output of the IMU filter. We
have currently worked around this by faking the data to be a constant. To do
this properly, we should either research how to properly calibrate magnetometers
or remove the magnetometer term from the equations completely.

####Difficulty of retrieving telemetry
The EV3 controller did not have any good mechanisms for retrieving telemetry
data while the bike is running. The processor was slow enough that trying to
save data in the middle of the control loop introduced unacceptable delays. The
code eventually saved telemetry data in memory until it exited, and then all of
the telemetry was saved to a file. This works, but retrieving the file still
required a complicated scheme of connecting various cables and running a slew of
ad-hoc scripts.

####Overall model inaccuracies
We did not validate our theoretical model against the actual behavior of the
bike. This was due to a combination of the annoyance of trying to retrieve
telemetry data as well as due to time constraints.

##Failed experiments
While we were failing to get our LQR controller to stabilize the bike, we also
tried some other control strategies based on machine learning. The idea here was
to choose some machine learning algorithms that could learn "online" while the
bike was running. These algorithms could be bootstrapped in the simulator and
then transferred to the real bike. On the real bike, the algorithms could then
adjust for any inaccuracies and limitation of the simulator.

However nice this sounded in theory, none of these algorithms worked (not even
in the simulator). This was due to a combination of a lack of experience
implementing these algorithms on real systems, time constraints, and overall
trickiness of getting these algorithms to work in the first place.

###SARSA learning
Because we knew that our model in the simulator was not accurate, we tried to
use some form of model-free reinforcement learning. SARSA
(state-action-reward-state-action) learning is one such algorithm. The idea
behind this algorithm is to try and learn a function $Q(s_t, a_t)$ that gives
the expected reward for every pair of possible system states $s_t$ and actions
$a_t$. This $Q$ function can be modeled in arbitrary ways, but we attempted to
model it as a quadratic function of the state and action. Each iteration of the
SARSA learning step could then be used to perform stochastic gradient descent to
improve the guess of the $Q$ function.

We did not have any success getting this algorithm to converge. We know vaguely
that the gradient corresponding to the squared terms appears to be much larger
than expected, but beyond that we ran out of time to investigate what was
happening. Robert Ou discussed this code with his housemate and both could not
find any obvious errors.

###Neural networks
Neural networks can be described as parameterized families of functions that
have a "simple" algorithm for optimizing the parameters using stochastic
gradient descent. We attempted to use a neural network consisting of two
subparts: a part to try and model an optimal controller and a part to try and
model the system dynamics. The intuition for why this might work is that the
existing control strategy and system model assumes that the system is linear,
and the neural net is definitely capable of representing linear functions (and
more complex functions as well, hence why it might work more effectively).

Because the EV3 controller is a resource-constrained system, we manually
implemented a small neural network using only NumPy and manual backpropagation.
However, we also could not get this to converge, even in the simulator. Our best
guess as to the problem is that excessively small networks might not learn
as well as the more common larger networks. Robert Ou's housemate later
reimplemented this network in a widely-used neural network library (PyTorch)
and also did not have any success.
