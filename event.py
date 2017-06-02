"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import *
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.

    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.=== Attributes ===@type rider: RideThe rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str

        >>> rider1 = Rider('Kelly', Location(4,4), Location(0,8), 10)
        >>> rq1 = RiderRequest(0, rider1)
        >>> str(rq1)
        '0 -- Kelly: Request a driver'
        """
        return "{} -- {}: Request a driver".format(self.timestamp,
                                                   self.rider.rider_id)

    def __eq__(self, other):
        """Return whether two RiderRequest events are equivalent to one another.

        @type self: RiderRequest
        @type other: RiderRequest
        @rtype: Bool

        >>> rider1 = Rider('Michael', Location(4,4), Location(0,8), 10)
        >>> rq1 = RiderRequest(0, rider1)
        >>> rider2 = Rider('Jan', Location(2,2), Location(7,4), 11)
        >>> rq2 = RiderRequest(2, rider2)
        >>> rq3 = RiderRequest(2, rider2)
        >>> rq1 == rq2
        False
        >>> rq2 == rq3
        True
        """
        if type(self) == RiderRequest and type(other) == RiderRequest:
            return (self.rider == other.rider and
                    self.timestamp == other.timestamp)

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        Since testing that method requires a Monitor, Dispatcher (which needs a
        dictionary of activities, riders, and drivers with all their attributes)
        and using notify method, we omit the examples.
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.rider_id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider,
                                 driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    @type timestamp: int
         A timestamp for this event.
         Precondition: must be a non-negative integer.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        Since testing that method requires a Monitor, Dispatcher (which needs a
        dictionary of activities, riders, and drivers with all their attributes)
        and using notify method, we omit the examples.
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        monitor.notify(
            self.timestamp, DRIVER, REQUEST, self.driver.identifier, \
            self.driver.location)

        events = []
        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time, rider,
                                 self.driver))
        return events

    def __eq__(self, other):
        """Return whether two DriverRequest events are equivalent to one another.

        @type self: DriverRequest
        @type other: DriverRequest
        @rtype: Bool

        >>> driver1 = Driver('Phyllis', Location(7,8), 5)
        >>> driver2 = Driver('Roy', Location(2,8), 1)
        >>> driver_request1 = DriverRequest(2, driver1)
        >>> driver_request2 = DriverRequest(3, driver2)
        >>> driver_request3 = DriverRequest(2, driver1)
        >>> driver_request1 == driver_request2
        False
        >>> driver_request1 == driver_request3
        True
        """
        if type(self) == DriverRequest and type(other) == DriverRequest:
            return (self.driver == other.driver and
                    self.timestamp == other.timestamp)

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str

        >>> driver1 = Driver('Phyllis', Location(7,8), 5)
        >>> dr1 = DriverRequest(0,driver1)
        >>> str(dr1)
        '0 -- Phyllis: Request a rider'
        """
        return "{} -- {}: Request a rider".format(self.timestamp,
                                                  self.driver.identifier)


class Cancellation(Event):
    """A rider cancels their requested ride.

    === Attributes ===
    @type driver: the Driver
    @type rider: the rider
    """
    def __init__(self, timestamp, rider):
        """Initialize a cancelation event.

        @type self: Cancellation
        @type rider: Rider
        @rtype: List
        """
        self.rider = rider
        super().__init__(timestamp)

    def do(self, dispatcher, monitor):
        """Cancel the driver, even if they are on route. Change the status of
        the waiting rider. Notify the monitor about the activity.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: List

        Since testing that method requires a Monitor, Dispatcher (which needs a
        dictionary of activities, riders, and drivers with all their attributes)
        and using notify method, we omit the examples.
        """
        if self.rider.status != SATISFIED:
            monitor.notify(
                self.timestamp, RIDER, CANCEL, self.rider.rider_id,
                self.rider.origin)
            self.rider.status = CANCELLED
        return []

    def __eq__(self, other):
        """Return whether two Cancellation events are equivalent to one another.

        @type self: Cancellation
        @type other: Cancellation
        @rtype: Bool

        >>> rider1 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> cancel = Cancellation(0, rider1)
        >>> rider2 = Rider('Dandan', Location(1, 1), Location(2, 3), 4)
        >>> cancel2 = Cancellation(0, rider2)
        >>> cancel == cancel2
        False
        """
        if type(self) == Cancellation and type(other) == Cancellation:
            return (self.timestamp == other.timestamp and
                    self.rider == other.rider)

    def __str__(self):
        """Return a string representation of this event.

        @type self: Cancellation
        @rtype: str

        >>> rider1 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> cancel = Cancellation(0, rider1)
        >>> str(cancel)
        '0 -- Heapster: Cancel request'
        """
        return "{} -- {}: Cancel request".format(self.timestamp,
                                                 self.rider.rider_id)


class Pickup(Event):
    """A driver picks up the rider.

    === Attributes ===
    @type driver: Driver
    @type rider: Rider
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a pickup event.

        @type self: Pickup
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        self.driver = driver
        self.rider = rider
        super().__init__(timestamp)

    def do(self, dispatcher, monitor):
        """Notify the monitor about the activity. Return a list of events.

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: List[Event]

        Since testing that method requires a Monitor, Dispatcher (which needs a
        dictionary of activities, riders, and drivers with all their attributes)
        and using notify method, we omit the examples.
        """

        events = []
        self.driver.end_drive(self.rider)
        monitor.notify(
                                    self.timestamp, DRIVER, PICKUP,
                                    self.driver.identifier,
                                    self.driver.location)
        self.driver.is_idle = False
        if self.rider.status == WAITING:
            self.rider.status = SATISFIED
            travel_time = self.driver.start_ride(self.rider)
            monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.rider_id,
                           self.rider.origin)
            events.append(Dropoff(self.timestamp + travel_time, self.driver,
                                  self.rider))

        elif self.rider.status == CANCELLED:
            self.driver.is_idle = True
            events.append(DriverRequest(self.timestamp, self.driver))

        return events

    def __eq__(self, other):
        """Return whether two Pickup events are equivalent to one another.

        @type self: Pickup
        @type other: Pickup
        @rtype: Bool

        >>> rider1 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> driver1 = Driver('Anu', Location(2, 3), 10)
        >>> pickup1 = Pickup(0, rider1, driver1)
        >>> rider2 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> driver2 = Driver('Anu', Location(2, 3), 10)
        >>> pickup2 = Pickup(0, rider2, driver2)
        >>> pickup1 == pickup2
        True
        """
        if type(self) == Pickup and type(other) == Pickup:
            return (self.timestamp == other.timestamp and self.rider ==
                    other.rider and self.driver == other.driver)

    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str

        >>> rider1 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> driver1 = Driver('Anu', Location(2, 3), 10)
        >>> pickup1 = Pickup(0, rider1, driver1)
        >>> str(pickup1)
        '0 -- Anu: Pickup Heapster'
        """
        return "{} -- {}: Pickup {}".format(self.timestamp,
                                            self.driver.identifier,
                                            self.rider.rider_id)


class Dropoff(Event):
    """A driver drops off the rider.

    === Attributes ===
    @type driver: the Driver
    @type rider: the rider
    """
    def __init__(self, timestamp, driver, rider):
        """Initialize a drop off event.

        @type self: Dropoff
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        self.driver = driver
        self.rider = rider
        super().__init__(timestamp)

    def do(self, dispatcher, monitor):
        """Notify the monitor about the activity.

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        Since testing that method requires a Monitor, Dispatcher (which needs a
        dictionary of activities, riders, and drivers with all their attributes)
        and using notify method, we omit the examples.
        """

        self.rider.status = SATISFIED
        self.driver.end_ride(self.rider)
        monitor.notify(
                    self.timestamp, DRIVER, DROPOFF, self.driver.identifier,
                    self.driver.location)

        return [DriverRequest(self.timestamp, self.driver)]

    def __eq__(self, other):
        """Return whether two Dropoff events are equivalent to one another.

        @type self: Dropoff
        @type other: Dropoff
        @rtype: Bool

        >>> rider1 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> driver1 = Driver('Anu', Location(2, 3), 10)
        >>> dropoff1 = Dropoff(0, driver1, rider1)
        >>> rider2 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> driver2 = Driver('Anu', Location(2, 3), 10)
        >>> dropoff2 = Dropoff(0, driver2, rider2)
        >>> dropoff1 == dropoff2
        True
        """
        if type(self) == Dropoff and type(other) == Dropoff:
            return (self.timestamp == other.timestamp and
                    self.rider == other.rider and self.driver == other.driver)

    def __str__(self):
        """Return a string representation of this event.

        @type self: Dropoff
        @rtype: str

        >>> rider1 = Rider('Heapster', Location(1, 1), Location(2, 3), 4)
        >>> driver1 = Driver('Anu', Location(2, 3), 10)
        >>> dropoff1 = Dropoff(0, driver1, rider1)
        >>> str(dropoff1)
        '0 -- Anu: Dropoff Heapster'
        """
        return "{} -- {}: Dropoff {}".format(self.timestamp,
                                             self.driver.identifier,
                                             self.rider.rider_id)


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                location = deserialize_location(tokens[3])
                driver = Driver(tokens[2], location, int(tokens[4]))
                event = DriverRequest(timestamp, driver)
            elif event_type == "RiderRequest":
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                rider = Rider(tokens[2], origin, destination, int(tokens[5]))
                event = RiderRequest(timestamp, rider)
            events.append(event)
        return events

if __name__ == '__main__':
    import doctest
    doctest.testmod()
