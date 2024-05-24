from runner import Runner
from race import ShortRace, MarathonRace
from competition import Competition
from custom_errors import CustomValueError, CustomTypeError


def create_runner(runner_info: str) -> Runner:
    """
    Create a Runner instance from a comma-separated input string.
    """
    try:
        name, age, country, sprint_speed, endurance_speed = runner_info.split(',')
        age = int(age)
        sprint_speed = float(sprint_speed)
        endurance_speed = float(endurance_speed)
        return Runner(name, age, country, sprint_speed, endurance_speed)
    except ValueError:
        raise CustomValueError("Invalid runner information format. Expected format: name,age,country,sprint_speed,endurance_speed")
    except Exception as e:
        raise CustomTypeError(f"Error creating runner: {e}")


def create_competition(runners: list, rounds_info: str, short_distances_info: str, marathon_distances_info: str) -> Competition:
    """
    Create a Competition instance from user inputs.
    """
    try:
        rounds = int(rounds_info)
        distances_short = [float(distance) for distance in short_distances_info.split(',')]
        distances_marathon = [float(distance) for distance in marathon_distances_info.split(',')]
        
        if len(distances_short) != rounds or len(distances_marathon) != rounds:
            raise CustomValueError("Number of distances must match the number of rounds.")
        
        return Competition(runners, rounds, distances_short, distances_marathon)
    except ValueError:
        raise CustomValueError("Invalid competition information format.")
    except Exception as e:
        raise CustomTypeError(f"Error creating competition: {e}")


def main():
    print("Welcome to the Running Competition Organizer!")
    runners = []
    
    while True:
        runner_info = input("Enter runner details (name,age,country,sprint_speed,endurance_speed) or 'done' to finish: ")
        if runner_info.lower() == 'done':
            break
        try:
            runner = create_runner(runner_info)
            runners.append(runner)
            print(f"Runner {runner.name} added successfully!")
        except Exception as e:
            print(e)
    
    if not runners:
        print("No runners were added. Exiting...")
        return
    
    while True:
        try:
            rounds_info = input("Enter the number of rounds: ")
            short_distances_info = input("Enter the distances for short races (comma-separated): ")
            marathon_distances_info = input("Enter the distances for marathon races (comma-separated): ")
            competition = create_competition(runners, rounds_info, short_distances_info, marathon_distances_info)
            break
        except Exception as e:
            print(e)
    
    competition.conduct_competition()
    competition.print_leaderboard()


if __name__ == '__main__':
    main()
