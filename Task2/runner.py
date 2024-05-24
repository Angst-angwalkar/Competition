from custom_errors import *
import csv
import os

class Runner:
    max_energy = 1000
    def __init__(self, name, age, country, sprint_speed, endurance_speed):
        """
        Initializes new Runner Instance with the values for:
        name,
        age,
        country,
        sprint_speed,
        endurance_speed        
        """
        self.name = self.name_validator(name)
        self.age = self.age_validator(age)
        self.country = self.country_validator(country)
        self.sprint_speed = self.sprint_speed_validator(sprint_speed)
        self.endurance_speed = self.endurance_speed_validator(endurance_speed)
        self.energy = Runner.max_energy



    
    @staticmethod
    def name_validator(name: str) -> str:
        """
        Validates name for type string and checks if name is alphanumeric.
        """
        if (not isinstance(name, str)):
            raise CustomTypeError(f"Name must be of type string and not {type(name)}")
        if (not name.replace(" ", "").isalnum()):
            raise CustomValueError(f"Name must be alphanumeric and can contain spaces. {name}")
        return name
    

    @staticmethod
    def age_validator(age: int) -> int:
        """
        Validates age for int string and checks if age is integer value.
        """
        if not isinstance(age, int):
            raise CustomTypeError(f"Age must be of type int and not {type(age)}")
        if not (5 <= age <= 120):
            raise CustomValueError(f"Invalid Age: {age}. Age must be less than or equal to 5 and greater than or equal to 120")
        return age
    

    @staticmethod
    def country_validator(country: str) -> str:
        """
        Validates country for type string and checks if country is in the list of valid countries.
        """
        with open(os.getcwd() + "/countries.csv", mode='r', newline="") as country_file:
            reader = csv.DictReader(country_file)
            valid_countries = [row["name"] for row in reader]
            if not isinstance(country, str):
                raise CustomTypeError(f"Country must be of type string and not {type(country)}")
            if country not in valid_countries:
                raise CustomValueError(f"Invalid country. {country} is not in the list of valid countries.")
        return country
    

    @staticmethod
    def sprint_speed_validator(sprint_speed: float) -> float:
        """
        Validates sprint_speed for type float and checks if sprint_speed is in the list of valid countries.
        """
        if not isinstance(sprint_speed, float):
            raise CustomTypeError(f"sprint_speed must be of type float and not {type(sprint_speed)}")
        if not (2.2 <= sprint_speed <= 6.8):
            raise CustomValueError(f"Invalid sprint_speed: {sprint_speed}. sprint_speed must be less than or equal to 2.2 and greater than or equal to 6.8")
        return sprint_speed


    @staticmethod
    def endurance_speed_validator(endurance_speed: float) -> float:
        """
        Validates endurance_speed for type string and checks if endurance_speed is in the list of valid countries.
        """
        if not isinstance(endurance_speed, float):
            raise CustomTypeError(f"endurance_speed must be of type float and not {type(endurance_speed)}")
        if not (1.8 <= endurance_speed <= 5.4):
            raise CustomValueError(f"Invalid endurance_speed: {endurance_speed}. endurance_speed must be less than or equal to 2.2 and greater than or equal to 6.8")
        return endurance_speed
    

    
    def drain_energy(self, drain_points) -> None:
        """
        Drains the energy of the runner by the drain_points provided as argument.
        Resulting energy after deduction cannot be less than 0.
        """
        if not (0 <= drain_points <= Runner.max_energy):
            raise CustomValueError(f"Drain points must be between 0 and {Runner.max_energy}")
        self.energy = max(0, self.energy - drain_points)
    
    def recover_energy(self, recovery_amount):
        """
        Recovers the energy of the runner by the recovery_amount provided as argument.
        Resultant energy after recovery cannot be greater than max_energy.
        """
        if not (0 <= recovery_amount <= Runner.max_energy):
            raise CustomValueError(f"Recovery points must be between 0 and {Runner.max_energy}")
        self.energy = min(Runner.max_energy, self.energy + recovery_amount)
    
    
    def run_race(self, race_type: str, distance: float) -> float:
        """
        Calculate the total time to complete the race based on the type and distance of the race. 
        """
        if race_type not in ["short", "long"]:
            raise ValueError("Race type must be either 'short' or 'long'.")
        
        if distance < 0:
            raise ValueError("Distance must be a non-negative number.")
        
        if race_type == "short":
            time_taken = (distance * 1000) / self.sprint_speed
        else:
            time_taken = (distance * 1000) / self.endurance_speed
        
        return round(time_taken, 2)
    
    def __str__(self):
        return f"Name: {self.name} Age: {self.age} Country: {self.country}"

if __name__ == '__main__':
    runner = Runner('Elijah', 18, 'Australia', 5.8, 4.4)
    
    # running a short race
    time_taken = runner.run_race('short', 2)
    print(f"Runner {runner.name} took {time_taken} seconds to run 2km!")


