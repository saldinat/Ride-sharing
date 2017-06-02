from rider import *


class Container:
    """A container that holds objects.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def add(self, item):
        """Add <item> to this Container.

        @type self: Container
        @type item: Object
        @rtype: None
        """
        raise NotImplementedError("Implemented in a subclass")

    def remove(self):
        """Remove and return a single item from this Container.

        @type self: Container
        @rtype: Object
        """
        raise NotImplementedError("Implemented in a subclass")

    def is_empty(self):
        """Return True iff this Container is empty.

        @type self: Container
        @rtype: bool
        """
        raise NotImplementedError("Implemented in a subclass")


class PriorityQueue(Container):
    """A queue of items that operates in priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first. Ties are resolved in FIFO order,
    meaning the item which was inserted *earlier* is the first one to be
    removed.

    Priority is defined by the rich comparison methods for the objects in the
    container (__lt__, __le__, __gt__, __ge__).

    If x < y, then x has a *HIGHER* priority than y.

    All objects in the container must be of the same type.
    """

    # === Private Attributes ===
    # @type _items: list
    #     The items stored in the priority queue.
    #
    # === Representation Invariants ===
    # _items is a sorted list, where the first item in the queue is the
    # item with the highest priority.

    def __init__(self):
        """Initialize an empty PriorityQueue.

        @type self: PriorityQueue
        @rtype: None
        """
        self._items = []

    def remove(self):
        """Remove and return the next item from this PriorityQueue.

        Precondition: <self> should not be empty.

        @type self: PriorityQueue
        @rtype: object

        >>> pq = PriorityQueue()
        >>> pq.add("red")
        >>> pq.add("blue")
        >>> pq.add("yellow")
        >>> pq.add("green")
        >>> pq.remove()
        'blue'
        >>> pq.remove()
        'green'
        >>> pq.remove()
        'red'
        >>> pq.remove()
        'yellow'
        """
        return self._items.pop(0)

    def is_empty(self):
        """
        Return true iff this PriorityQueue is empty.

        @type self: PriorityQueue
        @rtype: bool

        >>> pq = PriorityQueue()
        >>> pq.is_empty()
        True
        >>> pq.add("thing")
        >>> pq.is_empty()
        False
        """
        return len(self._items) == 0

    def add(self, item):
        """Add <item> to this PriorityQueue.

        @type self: PriorityQueue
        @type item: object
        @rtype: None

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> pq._items
        ['blue', 'green', 'red', 'yellow']
        """
        if item is not None:
            self._items.append(item)
            self._items.sort()

    def __str__(self):
        """Return a string representation of all objects in this PriorityQueue.

        @type self:PriorityQueue
        @rtype: str

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> pq.__str__()
        'Priority queue: blue, green, red, yellow'
        """
        obj_list = []
        for item in self._items:
            obj_list.append(str(item))

        string_list = ', '.join(obj_list)
        return "Priority queue: {}".format(string_list)


class RiderQueue(Container):
    """A first-in, first-out (FIFO) queue.

    Riders are removed from the queue according to rider that was inserted
    *earlier*.
    """

    def __init__(self):
        """Create and initialize new RiderQueue self.

        @type self: RiderQueue
        @rtype: None
        """
        self._riders = []

    def add(self, rider):
        """Add object at the back of RiderQueue self.

        @type self: RiderQueue
        @type rider: Rider
        @rtype: None
        """
        self._riders.append(rider)

    def remove(self):
        """Remove and return front object from RiderQueue self.

        RiderQueue self must not be empty.

        @type self: RiderQueue
        @rtype: Rider

        >>> r = RiderQueue()
        >>> r1 = Rider('Danny', Location(4,4), Location(9,0), 23)
        >>> r.add(r1)
        >>> str(r.remove())
        'RiderID: Danny, Origin: (4, 4), Destination: (9, 0), Status: waiting, Patience: 23'
        """
        return self._riders.pop(0)

    def is_empty(self):
        """Return whether RiderQueue self is empty.

        @type self: RiderQueue
        @rtype: bool

        >>> q = RiderQueue()
        >>> q.add(5)
        >>> q.is_empty()
        False
        >>> q.remove()
        5
        >>> q.is_empty()
        True
        """
        return self._riders == []

    def __str__(self):
        """Return a string representation of all riders in this RiderQueue.

        @type self: RiderQueue
        @rtype: str

        >>> r = RiderQueue()
        >>> r1 = Rider('Danny', Location(4,4), Location(9,0), 23)
        >>> r2 = Rider('Bartholomew', Location(3,3), Location(2,3), 2)
        >>> r.add(r1)
        >>> r.add(r2)
        >>> r.__str__()
        'RiderID: Danny, Origin: (4, 4), Destination: (9, 0), Status: waiting, Patience: 23, RiderID: Bartholomew, Origin: (3, 3), Destination: (2, 3), Status: waiting, Patience: 2'
        """
        rider_list = []
        for rider in self._riders:
            rider_list.append(str(rider))

        string_list = ', '.join(rider_list)
        return "{}".format(string_list)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
