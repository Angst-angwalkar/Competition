from custom_errors import *
from abc import ABC, abstractmethod
from runner import Runner
import math
from typing import List, Union

class Race(ABC):
    """
    Parent class Race for basic initialization.
    Initializes maximum_participants and energy_per_km vars.
    """
    maximum_participants: int
    energy_per_km = 100

    def __init__(self, distance: float, runners: Union[List[Runner], None] = None):
        self.runners = runners if runners is not None else []
        self.distance = self.distance_validator(distance)


    @staticmethod
    def distance_validator(distance: float) -> float:
        """
        Validates distance for negative values.
        Raises CustomValueError on invalid values for distance.
        """
        if not isinstance(distance, float):
            raise CustomTypeError("Distance must be a float.")
        if distance < 0:
            raise CustomValueError("Invalid Distance {distance}. Value for distance cannot be less than 0.")
        return distance


    def add_runner(self, runner) -> None:
        """
        Adds a new runner to the race.
        Raises RunnerAlreadyExistsError if the runner is already a part of the race.
        Raises RaceIsFullError if the race is full and maximum_participant count is reached.
        """
        if not isinstance(runner, Runner):
            raise CustomTypeError("runner object must be an instance of class Runner.")
        if runner in self.runners:
            raise RunnerAlreadyExistsError(f"Runner with name: {runner.name} already exists in the race.")
        if len(self.runners) > self.maximum_participants:
            raise RaceIsFullError("Race is full. Maximum number of participants reached.")
        self.runners.append(runner)
    
    def remove_runner(self, runner) -> None:
        """
        Adds a new runner to the race.
        Raises RunnerAlreadyExistsError if the runner is already a part of the race.
        Raises RaceIsFullError if the race is full and maximum_participant count is reached.
        """
        if runner not in self.runners:
            raise RunnerDoesntExistError("The runner you're trying to remove does not exist in the race.")
        self.runners.remove(runner)
    

    @abstractmethod
    def conduct_race(self):
        pass

class ShortRace(Race):
    time_multiplier = 1.2

    def __init__(self, distance: float, runners: Union[List[Runner], None] = None):
        self.race_type = "short"
        super().__init__(distance, runners)
        self.maximum_participants = 8
    

    def conduct_race(self) -> list:
        result = []
        for runner in self.runners:
            time_taken = runner.run_race("short", self.distance) * self.time_multiplier
            result.append((runner, round(time_taken, 2)))
        return result


class MarathonRace(Race):

    def __init__(self, distance: float, runners: Union[List[Runner], None] = None):
        self.race_type = "long"
        super().__init__(distance, runners)
        self.maximum_participants = 16

    
    def conduct_race(self) -> list:
        """
        Overrides the conduct_race method from the parent class.
        Conducts the race and prints out the results for the race.
        """
        result = []
        for runner in self.runners:
            time_taken = 0
            finished = True
            for km in range(math.ceil(self.distance)):
                if runner.energy > 0:
                    time_taken += runner.run_race("long", 1)
                    runner.drain_energy(self.energy_per_km)
                else:
                    time_taken = 'DNF'
                    finished = False
                    break
            if finished:
                time_taken = round(time_taken, 2)
            result.append((runner, time_taken))
        return result
        
if __name__ == '__main__':
    short_race = ShortRace(0.5)
    long_race = MarathonRace(5.0)

    # Add a Runner
    eli = Runner('Elijah', 18, 'Australia', 5.8, 4.4)
    rup = Runner('Rupert', 23, 'Australia', 2.3, 1.9)

    long_race.add_runner(eli)
    long_race.add_runner(rup)

    results = long_race.conduct_race()
    for runner, time in results:
        print(runner.name, time) 

