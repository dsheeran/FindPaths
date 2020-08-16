import time
class PathSearch:
    """
    Search for and count  different types of paths in plane of integers.
    To start with we look at closed non intersecting  paths of length 2n in first quadrant x>=0, y >=0 , x,y in Z
    """
    UP = (0,1)
    DOWN = (0,-1)
    RIGHT = (1,0)
    LEFT = (-1,0)



    def __init__(self, n):
        """A path consists of a List of Points.
        Admissible Paths start and end at origin.  [ origin , point1,....,origin]
        we include the origin at start and end of List .However in the recorded paths we trim the second origin point to suit the polygon drawing method"""
        self.PATH_LENGTH  = 2*n # the length of the path we are searching for
        self.n = n
        self.deltas = [PathSearch.UP,PathSearch.DOWN,PathSearch.LEFT,PathSearch.RIGHT]  # all possible deltas to next point in path
        self.path = [None] *self.PATH_LENGTH # initialize to empty path
        self.last_index = self.get_last_index_map()
        self.solutions = []  # list of admissible paths found
        self.visited = 0 # number of paths visited
        self.time = 0

    def get_last_index_map(self):
        """ Create 2-d table of size PATH_LENGTH with initial values of None. """
        lim = []
        for i in range(self.PATH_LENGTH):
            lim.append([None]*self.PATH_LENGTH)
        return lim

    def in_path(self, path_length, x,y):
        """
        Check if (x,y) is in self.path with index < path_length.
        This is done in constant time by maintaining a look-up of last index used for x,y
        The advantage of this approach, rather than using something like a set, or a dictionary (Python version >= 3.6) as an ordered set,  to store  points in path is that there is no need to update
        our data when we backtrack and remove a point from the path, i.e. on return from expand().
        The trade off is a slightly more complex condition to check since the last index may be stale.  """

        l_index = self.last_index[x][y]
        r = l_index is not None and  l_index < path_length and self.path[l_index] == (x,y)
        #print( f"in path path_length:{r} {path_length} x:{x} y:{y} l_index:{l_index} path:{self.path}")
        return r

    def search(self):
        # set up starting path. we always start going up from origin
        start_time = time.time()
        self.path[0] = (0,0)
        self.last_index[0][0] = 0
        self.path[1] = (0,1)
        self.last_index[0][1] = 1

        n = 2
        self.expand(n, 0, 1)
        end_time = time.time()
        self.time = end_time - start_time


    def record_solution(self):
        """Save  the current path which contains an admissible path."""
        solution = self.path[:self.PATH_LENGTH]
        self.solutions.append( solution)

    def expand(self, path_length ,x, y):
        """
        Expand the path recursively with all possible successor points. Record any solutions.
        :param path_length: current path length
        :param x the value of x at end of path
        :param y the value of y at end of path

        Note don't really need to have x, y in parameter list since  (x,y) = self.path[path_length-1], but it is convenient.

        """
        #print(f"expand:path length:{path_length} x:{x} y:{y}")
        self.visited += 1
        for delta in self.deltas:
            xp = x + delta[0]
            yp = y + delta[1]
            # check if solution. find solution when we are about to add (0,0) to PATH_LENGTH points.
            if xp == 0 and yp == 0 and path_length == self.PATH_LENGTH:
                self.record_solution()
                continue
            # Check that (xp,yp) is admissible. The last condition checks if we have enough steps left to get back to (0,0)
            if xp >= 0 and yp >= 0  and not self.in_path(path_length,xp,yp) and xp + yp + path_length <= self.PATH_LENGTH:
                # add (xp, yp) to path
                self.path[path_length] = (xp, yp)
                self.last_index[xp][yp] = path_length
                self.expand(path_length + 1, xp, yp)


    def draw_solutions(self):
        """ This is called in Sage Notebook which provides the polygon constructor.
         Draw esch path in a grid of paths """
        width = 6
        dx  = 4
        dy = -4
        d = (0,0)
        col = 0
        index = 0
        chart = None
        for soln in self.solutions:
            if chart is None:
                chart = self.get_polygon(d,soln)
            else:
                chart = chart + self.get_polygon(d,soln)
            index+=1
            if index % width == 0:
                index=0
                d = (0, d[1] + dy)

            else:
                d = (d[0] + dx, d[1] )
        chart.show()


    def get_polygon(self, offset, path ):
        print(f"offset:{offset}")
        points = []
        dx = offset[0]
        dy = offset[1]
        for p in path:
            point = (p[0] + dx, p[1] + dy)
            points.append(point)
        p = polygon(points, axes=False,fill=False)
        p.show()
        return p
