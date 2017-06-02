class Location:
    """A location based on two coordinates(m,n) on a two-dimensional grid.
    
    ===Attributes===
    @type m: int 
        The number of blocks the location is from the bottom edge of the grid
        A non-negative integer
    @type n: int
        The number of blocks the location is from the left of the grid
        A non-negative integer
    """
    
    def __init__(self, m, n):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        self.coordinate = (m, n)

    def __str__(self):
        """Return a string representation.
        
        @type self: Location
        @rtype: str
        
        >>> loc = Location(2, 3)
        >>> print(loc.__str__())
        (2, 3)
        """
        return str(self.coordinate)
        
    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.
        
        @type self: Location
        @rtype: bool
        
        >>> loc1 = Location(2,2)
        >>> loc2 = Location(2,3)
        >>> loc3 = Location(2,2)
        >>> loc1 == loc2 
        False
        >>> loc1 == loc3 
        True
        >>> loc2 == loc3
        False
        """
        return type(self) == type(other) and self.coordinate == other.coordinate


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    
    >>> point1= Location(1, 1)
    >>> point2 = Location (4, 4)
    >>> manhattan_distance(point1, point2)
    6
    """
    return (
        abs(
            origin.coordinate[0] - destination.coordinate[0]) + abs(
                origin.coordinate[1] - destination.coordinate[1]))


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'm,n'
    @rtype: Location
    
    >>> point1 = deserialize_location('1,2')
    >>> print(point1)
    (1, 2)
    """
    location_list = location_str.split(',')
    return Location(int(location_list[0]), int(location_list[1]))

if __name__ == '__main__':
    import doctest
    doctest.testmod()