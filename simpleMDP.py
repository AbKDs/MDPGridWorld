# Possible set of actions
NORTH = 0 # Location(-1, 0)
EAST  = 1 # Location( 0, 1)
SOUTH = 2 # Location( 1, 0)
WEST  = 3 # Location(0, -1)
OBSTACLE = None

class Location(object):
    """
    Location represents a two dimensional location on a grid.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __add__(self, loc):
        x = self.getX() + loc.getX()
        y = self.getY() + loc.getY()
        return Location(x, y)

    def __str__(self):
        return '<' + self.x + ', ' + self.y + '>'

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) 
  
Actions = {NORTH:Location(-1, 0), EAST:Location( 0, 1), 
            SOUTH:Location( 1, 0) , WEST:Location(0, -1)}

class Robot(object):
    """
    Represents a robot in a grid world.

    Contains specific transition probabilities and 
    reward functions for it's movements.
    """
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid
        self.livingReward = -0.01

    def __str__(self):
        return 'Robot name is ' + str(self.name)
    
    def T(self, s, a, sdash):
        aL = Location(0*Actions[a].getX() + (-1)*Actions[a].getY(), 
                    1*Actions[a].getX() + 0*Actions[a].getY())
        aR = Location(0*Actions[a].getX() + 1*Actions[a].getY(), 
                    (-1)*Actions[a].getX() + 0*Actions[a].getY())

        sA = s + Actions[a]
        sAR = s + aR
        sAL  = s + aL

        if (not grid.isLocInGrid(sA)) \
            or grid.isLocObstacle(sA):
            sA = s

        if (not grid.isLocInGrid(sAR)) \
            or grid.isLocObstacle(sAR):
            sAR = s

        if (not grid.isLocInGrid(sAL)) \
            or grid.isLocObstacle(sAL):
            sAL = s

        if sA == sdash:
            return 0.8
        elif sAR == sdash:
            return 0.1
        elif sAL == sdash:
            return 0.1
        else:
            return 0.0

    def R(self, s, a, sdash):
        """
        Returns reward for transitioning from a current state 
        to a new state. 

        Note: In this simple example, only the final state 
        determines the value of reward. Can be easily 
        modified for a more complicated function.
        """
        return self.livingReward

class GridWorld(object):
    """ 
    GridWorld represents a rectangular world with a reward and
    a pit. 

    A world contains height * width states and at any point the
    grid values represent the maximum reward that can be 
    achieved from that state.
    """
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.V = [[0.0 for _ in range(self.width)] \
                for _ in range(self.height)]
        self.Q = [[[0.0 for _ in Actions] for _ in range(self.width)]\
                for _ in range(self.height)]
        self.goal = None        
        self.pit = None
        self.goalValue = 1.0
        self.pitValue = -1.0
        self.obstacle = None
        self.directions = [[NORTH for _ in range(self.width)]
                            for _ in range(self.height)]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setGoalLocation(self, loc):
        """
        Takes a location to set the goal on the grid.
        """
        self.goal = loc
        x = loc.getX()
        y = loc.getY()
        self.Q[x][y] = 0.0

    def getGoalLoc(self):
        return self.goal

    def getPitLoc(self):
        return self.pit

    def setPitLocation(self, loc):
        """
        Takes a location to set the goal on the grid.
        """
        self.pit = loc
        x = loc.getX()
        y = loc.getY()
        self.Q[x][y] = 0.0
    
    def getPolicy(self):
        return self.directions
    
    def setDirection(self, direction):
        self.direction = direction
    
    def getQ(self):
        """
        Return Q states of the grid.
        """
        return self.Q

    def setQ(self, Q):
        self.Q = Q

    def setV(self, V):
        self.V = V

    def getV(self):
        """
        Return V values of the grid.
        """
        return self.V

    def printQ(self):
        """
        Prints the Q values of a state, in order of 
        north, east, south, west.
        """
        for _ in self.Q:
            print _

    def printV(self):
        """
        Prints the V values of a state.
        """
        for x in range(len(self.V)):
            for y in range(len(self.V[0])):
                if self.V[x][y] == None:
                    print("Nil  "),
                else:
                    print("%0.2f " %self.V[x][y]), 
            print '\n'
    def printDirections(self):
        dirStrings = ['North', 'East', 'South', 'West']
        
        for x in range(len(self.V)):
            for y in range(len(self.V[0])):
                if self.V[x][y] == None:
                    print("---  "),
                else:
                    print("%s " %dirStrings[self.direction[x][y]]), 
            print '\n'
    
    def getObstacleLoc(self):
        return self.obstacle

    def isLocInGrid(self, loc):
        x = loc.getX()
        y = loc.getY()
        return (x >= 0) and (x < self.height) \
            and (y >= 0) and (y < self.width)

    def isLocObstacle(self, loc):
        return loc == self.obstacle

    def setObstacleLocation(self, loc):
        """
        Places an obstacle in a grid position. The 
        robot can't reach this position.        
        """
        x = loc.getX()
        y = loc.getY()
        self.obstacle = loc
        self.V[x][y] = OBSTACLE
        self.Q[x][y] = OBSTACLE

    def getGoalValue(self):
        return self.goalValue

    def getPitValue(self):
        return self.pitValue

class ValueIteration(object):
    """
    ValueIteration represents a class which manipulates a 
    GridWorld using value iteration.

    Value Iteration is a reinforcement learning algorithm
    to find the optimal V values of a state and the policy.
    """
    def __init__(self, gridWorld, robot, gamma):
        self.gridWorld = gridWorld
        self.robot = robot
        self.gamma = gamma
        
    def updateUtility(self):
        """
        A single iteration update over all the state values.
        """
        height = self.gridWorld.getHeight()
        width  = self.gridWorld.getWidth()

        Q = self.gridWorld.getQ()

        oldV = self.gridWorld.getV()
        newV = self.gridWorld.getV()
        direction = self.gridWorld.getPolicy()
        
        T = robot.T
        R = robot.R

        for x in range(height):
            for y in range(width):
                s = Location(x, y)
                if self.notExitNorObstacle(s):
                    for action in Actions.keys():
                        total = 0
                        for xdash in range(height):
                            for ydash in range(width):
                                sdash = Location(xdash, ydash)
                                if not self.gridWorld.isLocObstacle(sdash):
                                    total += T(s, action, sdash)*(R(s, action
                                    , sdash) + self.gamma*oldV[xdash][ydash])
                        Q[x][y][action] = total

        for x in range(height):
            for y in range(width):
                s = Location(x, y)
                if self.notExitNorObstacle(s):
                    (newV[x][y], direction[x][y]) = max((v, i) for i,v in 
                                                enumerate(Q[x][y]))
        
        self.gridWorld.setV(newV)
        self.gridWorld.setDirection(direction)
        self.gridWorld.setQ(Q)
    
    def updateStates(self, iter):
        """
        Updates the value of Q states for the grid positions
        for a given number of iterations.
        """

        # The first iteration updates the value of the 
        # exit states.
        goal = self.gridWorld.getGoalLoc()
        goalX = goal.getX()
        goalY = goal.getY()

        pit = self.gridWorld.getPitLoc()
        pitX = pit.getX()
        pitY = pit.getY()

        Q = self.gridWorld.getQ()
        Q[goalX][goalY] = self.gridWorld.getGoalValue()
        Q[pitX][pitY] = self.gridWorld.getPitValue()

        V = self.gridWorld.getV()
        V[goalX][goalY] = self.gridWorld.getGoalValue()
        V[pitX][pitY] = self.gridWorld.getPitValue()

        self.gridWorld.setQ(Q)
        self.gridWorld.setV(V)

        # Updating all states except obstacle state and 
        # the exit states.

        for i in range(1, iter):
            self.updateUtility()

    def notExitNorObstacle(self, loc):
        """
        Checks whether the current state is not a
        obstacle nor any of the exit states.
        """
        goal = self.gridWorld.getGoalLoc()
        pit = self.gridWorld.getPitLoc()
        obstacle = self.gridWorld.getObstacleLoc()

        return not ((loc == goal) or (loc == pit) or (loc == obstacle))


if __name__ == '__main__':
    grid = GridWorld(3, 4)
    grid.setGoalLocation(Location(0, 3))
    grid.setPitLocation(Location(1, 3))
    grid.setObstacleLocation(Location(1, 1))
    robot = Robot('R2D2', grid)

    vi = ValueIteration(grid, robot, gamma = 0.9)
    
    print 'Initial Values:'
    print '------------------------------------'
    grid.printV()
    #grid.printQ()
    iter = 100
    vi.updateStates(iter)
    
    print 'Values after ' + str(iter) + ' iterations.'
    print '------------------------------------'
    grid.printV()
    
    print '\n'
    print 'The policy on this map.'
    print '------------------------------------'
    grid.printDirections()
    #grid.printQ()
