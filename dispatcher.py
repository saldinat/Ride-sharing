from location import Location
from driver import *
from rider import Rider
from container import *


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.

    === Attributes ===
    @type driver_list: list
         A list of drivers.
    @type rq: RiderQueue
         A sorted based on a priority queue of riders.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        self.driver_list = []
        self.rq = RiderQueue()

    def __str__(self):
        """Return a string representation of the dispatcher.

        @type self: Dispatcher
        @rtype: str

        >>> d = Dispatcher()
        >>> rider1 = Rider('Mark', Location(4,5), Location(0,4), 10)
        >>> driver1 = Driver('Jum', Location(4,5), 10)
        >>> d.request_rider(driver1)
        >>> str(d)
        "Drivers: ['Driver ID: Jum, Current Location: (4, 5), Speed: 10']\\nAvailable riders: []"
        """
        string_list_driver = []
        for driver in self.driver_list:
            string_list_driver.append(str(driver))
        return "Drivers: {}\nAvailable riders: [{}]".format(
            string_list_driver, str(self.rq))

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None

        Since request_driver returns an object (Driver) or None the output is
        not presentable. Therefore we omit the examples.
        """
        if self.driver_list != []:
            for driver in self.driver_list:
                if driver.is_idle:
                    eta = driver.get_travel_time(rider.origin)
                    fastest_driver = driver
            i = 0

            for i in range(len(self.driver_list)):
                if self.driver_list[i].is_idle == True:
                    new_eta = self.driver_list[i].get_travel_time(rider.origin)
                    if new_eta < eta:
                        eta = new_eta
                        fastest_driver = self.driver_list[i]
            fastest_driver.is_idle = False
            return fastest_driver

        else:
            self.rq.add(rider)

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None

        Since request_rider returns an object (Rider) or None the output is not
        presentable. Therefore we omit the examples.
        """
        if driver not in self.driver_list:
            self.driver_list.append(driver)
            driver.is_idle = True
        if self.rq.is_empty():
            return None
        elif not self.rq.is_empty():
            return self.rq.remove()

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """
        rider.status = CANCELLED


if __name__ == '__main__':
    import doctest
    doctest.testmod()
