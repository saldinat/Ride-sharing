from location import Location, manhattan_distance
from rider import *


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        self.identifier = identifier
        self.location = location
        self.speed = speed
        self.destination = None
        self.is_idle = True

    def __str__(self):
        """Return a string representation of the Driver.

        @type self: Driver
        @rtype: str

        >>> point1 = Location(4, 5)
        >>> d1 = Driver('Mark', point1, 10)
        >>> str(d1)
        'Driver ID: Mark, Current Location: (4, 5), Speed: 10'
        """
        return 'Driver ID: {}, Current Location: {}, Speed: {}'.format(
            self.identifier, self.location, self.speed)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool

        >>> point1 = Location(5, 6)
        >>> point2 = Location(8, 5)
        >>> d1 = Driver('Kelly', point1, 10)
        >>> d2 = Driver('Michael', point2, 5)
        >>> d3 = Driver('Kelly', point1, 10)
        >>> d1 == d2
        False
        >>> d1 == d3
        True
        """
        return type(self) == type(other) and (self.identifier, self.location,
                                              self.speed) == (other.identifier,
                                                              other.location,
                                                              other.speed)

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int

        >>> point1 = Location(1,1)
        >>> driver1 = Driver('Mark', point1, 3)
        >>> point2 = Location(4,4)
        >>> point3 = Location(4, 0)
        >>> driver1.get_travel_time(point2)
        2
        >>> driver1.get_travel_time(point3)
        1
        """
        distance = manhattan_distance(self.location, destination)
        return distance // self.speed

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int

        >>> point1 = Location(1,1)
        >>> point2 = Location(6,6)
        >>> driver1 = Driver('Mark', point1, 5)
        >>> driver1.start_drive(point2)
        2
        """
        self.is_idle = False
        self.destination = location
        distance = manhattan_distance(self.location, self.destination)
        return round(distance / self.speed)

    def end_drive(self, rider):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @type rider: Rider
        @rtype: None
        """
        self.location = rider.origin
        self.destination = None
        self.is_idle = True

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> driver = Driver('Jim', Location(2, 2), 10)
        >>> rider = Rider('Mark', Location(0, 0), Location(3, 3), 2)
        >>> driver.start_ride(rider)
        0
        """
        #Pick up the rider only if they are still waiting
        self.destination = rider.destination
        rider.status = SATISFIED
        return self.get_travel_time(self.destination)

    def end_ride(self, rider):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @type rider: Rider
        @rtype: None
        """
        self.location = rider.destination
        self.destination = None
        self.is_idle = True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
