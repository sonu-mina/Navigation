class Point:
    '''
        A point object that contains x & y co-ordinates
        and connections with other points
    '''

    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = set()

    def __str__(self):
        return '('+str(round(self.x, 2))+','+str(round(self.y, 2))+')'

    def distance(self, point):
        return ((self.x-point.x)**2 + (self.y-point.y)**2)**(1/2)
        # return max(abs(self.x-point.x), abs(self.y-point.y))

    def isValid(self, point, max_distance):
        return self.distance(point)<max_distance and self.distance(point)>0