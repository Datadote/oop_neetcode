""" OOP design of a parking lot """
from typing import List, Dict, Optional
import datetime

class Vehicle:
    def __init__(self, spot_size: int):
        self._spot_size = spot_size

    def get_spot_size(self) -> int:
        return self._spot_size

class Car(Vehicle):
    def __init__(self, spot_size: int = 1):
        super().__init__(spot_size)

class Limo(Vehicle):
    def __init__(self, spot_size: int = 2):
        super().__init__(spot_size)

class Semitruck(Vehicle):
    def __init__(self, spot_size: int = 3):
        super().__init__(spot_size)

class Person:
    def __init__(self, balance: int):
        self._balance = balance

    def get_balance(self):
        return self._balance

    def update_balance(self, amt: int) -> int:
        self._balance += amt
        return self._balance

class ParkingFloor:
    def __init__(self, spots: int):
        self._spots = [0] * spots
        self._vehicle_map: Dict[Vehicle, List[int]] = {}

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        spots_needed = vehicle.get_spot_size()
        left, right = 0, 0
        while right < len(self._spots):
            if self._spots[right] != 0:
                left = right + 1
            if right - left + 1 == spots_needed:
                self.update_spots(left, right, 1)
                self._vehicle_map[vehicle] = [left, right]
                return True
            right += 1
        return False

    def remove_vehicle(self, vehicle: Vehicle) -> bool:
        if vehicle not in self._vehicle_map:
            return False
        start, end = self._vehicle_map[vehicle]
        self.update_spots(start, end, 0)
        del self._vehicle_map[vehicle]
        return True

    def update_spots(self, start: int, end: int, value: int):
        for i in range(start, end + 1):
            self._spots[i] = value

    def get_parking_spots(self):
        return self._spots

    def get_vehicle_spots(self, vehicle: Vehicle) -> Optional[List[int]]:
        return self._vehicle_map.get(vehicle)

class ParkingGarage:
    """ Give a vehicle, search each floor for the vehicle """
    def __init__(self, floors: int, spots_per_floor: int):
        self._floors = [ParkingFloor(spots_per_floor) for _ in range(floors)]

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for floor in self._floors:
            if floor.park_vehicle(vehicle):
                return True
        return False

    def remove_vehicle(self, vehicle: Vehicle) -> bool:
        for floor in self._floors:
            if floor.remove_vehicle(vehicle):
                return True
        return False

class ParkingSystem:
    def __init__(self, parking_garage: ParkingGarage, hourly_rate: int):
        self._parking_garage = parking_garage
        self._hourly_rate = hourly_rate # < 1 hr free, increments of 1 hr
        self._time_parked: Dict[Vehicle, int] = {}

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        if self._parking_garage.park_vehicle(vehicle):
            self._time_parked[vehicle] = datetime.datetime.now().hour
            return True
        return False

    def remove_vehicle(self, person: Person, vehicle: Vehicle) -> bool:
        if self._parking_garage.remove_vehicle(vehicle):
            hrs = datetime.datetime.now().hour - self._time_parked[vehicle]
            person.update_balance(-(hrs * self._hourly_rate))
            del self._time_parked[vehicle]
            return True
        return False
