# MDPGridWorld

A python program implementing Value Iterations algorithm for 
Markov Decision Process. 

Details:

A grid world of height x width dimension is given as input. 
There is a goal (which has +1.0 reward) and fire pit (which
has -1.0 reward). These values can be set manually. There is 
a living reward (negative) of the robot, so that it doesn't
slack and find the goal as quickly as possible. 

As run on a 3 x 4 grid world with goal at (0, 3) location and
fire at (1, 3) location and obstacle at (1, 1) location it finds
the policy after converging in almost 100 iterations and prints
the policy for the particular map.

Improvements:

As of now it takes only one goal position and one fire pit position
but it can be easily expanded to the situation where there are 
multiple pits and multiple obstacles.
