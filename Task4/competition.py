from race import *
from runner import Runner
from typing import Dict, Tuple, Union, List

class Competition:

    """
    Competition class for Conducting race competitions.
    """
    MAX_ROUNDS = 3

    def __get_ordinal(self, n):
        # Helper function to return the ordinal string for a given integer
        # NOTE : You can ignore this method, you don't need to comment
        # or do any checks on it whatsoever
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        if 11 <= n % 100 <= 13:
            suffix = 'th'
        else:
            suffix = suffixes.get(n % 10, 'th')
        return f"{n}{suffix}"

    def __init__(self, runners: List[Runner], rounds: int, distances_short: List[float], distances_marathon: List[float]) -> None:
        """
        Initializer method for Competition.
        :param runners: List of runners participating in the competition
        :param rounds: Number of rounds in the competition
        :param distances_short: List of distances for short races
        :param distances_marathon: List of distances for marathon races

        Validates params: runners, rounds, distances_short, distances_marathon.
        
        """
        if not isinstance(runners, list) or not all(isinstance(runner, Runner) for runner in runners):
            raise CustomTypeError("Runners must be a list of Runner objects.")
        if not isinstance(rounds, int) or rounds <= 0:
            raise CustomTypeError("Rounds must be a positive integer.")
        if rounds > self.MAX_ROUNDS:
            raise CustomValueError(f"Rounds cannot exceed {self.MAX_ROUNDS}.")
        if not isinstance(distances_short, list) or not all(isinstance(distance, float) for distance in distances_short):
            raise CustomTypeError("Distances for short races must be a list of positive floats.")
        if not isinstance(distances_marathon, list) or not all(isinstance(distance, float) for distance in distances_marathon):
            raise CustomTypeError("Distances for marathon races must be a list of positive floats.")
        if len(distances_short) != rounds or len(distances_marathon) != rounds:
            raise CustomValueError("Length of distance lists must be equal to the number of rounds.")

        self.runners = runners
        self.rounds = rounds
        self.distances_short = distances_short
        self.distances_marathon = distances_marathon
        self.leaderboard: Dict[str, Union[None, Tuple[str, int]]] = {}

        for i in range(1, len(self.runners) + 1):
            self.leaderboard[self.__get_ordinal(i)] = None

    def conduct_competition(self) -> Dict[str, Union[None, Tuple[str, int]]]:
        """
        Conducts the competition across the specified number of rounds.
        """
        for current_round in range(self.rounds):
            # Conduct the short race with all runners
            short_race = ShortRace(self.distances_short[current_round], runners=self.runners)
            short_result = self.conduct_race(short_race)

            # Conduct the marathon race with all runners
            marathon = MarathonRace(self.distances_marathon[current_round], runners=self.runners)
            marathon_result = self.conduct_race(marathon)

            # Recover energy for all DNF runners
            for runner in self.runners:
                runner.recover_energy(1000)

            # Update leaderboard
            self.update_leaderboard(short_result)
            self.update_leaderboard(marathon_result)

        return self.leaderboard

    def conduct_race(self, race: Union[ShortRace, MarathonRace]) -> List[Tuple[Runner, Union[float, str]]]:
        """
        Conducts a given race and returns the results.
        """
        return race.conduct_race()

    def update_leaderboard(self, results: List[Tuple[Runner, Union[float, str]]]) -> None:
        """
        Updates the leaderboard based on race results.
        """
        sorted_result = sorted(results, key=lambda x: x[1] if isinstance(x[1], (int, float)) else float('inf'))
        for i, (runner, time) in enumerate(sorted_result):
            position = len(sorted_result) - (i + 1)
            if time == 'DNF':
                points = 0
            else:
                points = position

            # Find runner in leaderboard and update points
            for pos in self.leaderboard:
                if self.leaderboard[pos] and self.leaderboard[pos][0] == runner.name:
                    current_points = self.leaderboard[pos][1]
                    new_points = current_points + points
                    self.leaderboard[pos] = (runner.name, new_points)
                    break
            else:
                self.leaderboard[self.__get_ordinal(i + 1)] = (runner.name, points)

        # Sort leaderboard based on points
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda item: item[1][1] if item[1] else 0, reverse=True)
        self.leaderboard = {self.__get_ordinal(i + 1): item[1] for i, item in enumerate(sorted_leaderboard)}

    def print_leaderboard(self) -> None:
        """
        Prints the leaderboard.
        """
        print("******Leaderboard******")
        for key, value in self.leaderboard.items():
            if value:
                print(f"{key} - {value[0]} ({value[1]})")
            else:
                print(f"{key} - None")

if __name__ == '__main__':
    runners = [
        Runner("Elijah", 19, 'Australia', 6.4, 5.2),
        Runner("Rupert", 67, 'Botswana', 2.2, 1.8),
        Runner("Phoebe", 12, 'France', 3.4, 2.8),
        Runner("Lauren", 13, 'Iceland', 4.4, 5.1),
        Runner("Chloe", 21, 'Timor-Leste', 5.2, 1.9)
    ]

    competition = Competition(runners, 3, [0.5, 0.6, 1.2], [4.0, 11.0, 4.5])
    competition.conduct_competition()
    competition.print_leaderboard()