from location import Location

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """

    A rider object within the simulation.

    === Attributes ===

    @type string rider_id: the identifying name of the associated rider
    @type Location origin: the current coordinate location of the rider
    @type Location destination: the coordinate destination of the rider
    @type string status: the current status of the rider: waiting, cancelled
    or satisfied
    @type string patience: the amount of time units a rider is willing to wait
    before they cancel their pickup request
    """

    def __init__(self, rider_id, origin, destination, patience):
        """
        Initialize a new rider object.

        @type rider_id: string
            The identifying name of the associated rider
        @type origin: tuple
            The current coordinate location of the rider
        @type destination: tuple
            The coordinate destination of the rider
        @type patience: string
            The amount of time units a rider is willing
        to wait before they cancel their pickup request
        @rtype: None
        """
        self.rider_id = rider_id
        self.origin = origin
        self.destination = destination
        self.status = WAITING
        self.patience = patience

    def __str__(self):
        """
        A string representation of a rider object.

        @type self: Rider
        @rtype: string

        >>> rider1 = Rider('Almond', Location(1,1), Location(2,2), 4)
        >>> str(rider1)
        'RiderID: Almond, Origin: (1, 1), Destination: (2, 2), Status: waiting,
         Patience: 4'
        """
        return(
            'RiderID: {}, Origin: {}, Destination: {}, Status: {}, '
            'Patience: {}'.format(
                self.rider_id, self.origin, self.destination,
                self.status, self.patience))

    def __eq__(self, other):
        """
        Return whether Rider self is equivalent to other.

        @type self: Rider
        @type other: Rider
        @rtype: Bool

        >>> r1 = Rider(43, Location(4,4), Location(9,0), 23)
        >>> r2 = Rider(44, Location(4,4), Location(9,0), 23)
        >>> r1 == r2
        False
        """
        return (type(self) == type(other) and
                self.rider_id == other.rider_id and
                self.origin == other.origin and
                self.destination == other.destination and
                self.status == other.status and
                self.patience == other.patience)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
