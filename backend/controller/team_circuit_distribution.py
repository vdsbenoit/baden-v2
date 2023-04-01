import math

from pulp import *


def get_nb_circuit(players, teams_per_circuit, min_players_per_team, max_players_per_team):
    if max_players_per_team < 2 * min_players_per_team:
        raise Exception("error")
    nb_circuit = 1
    while True:
        min_players = min_players_per_team * teams_per_circuit * nb_circuit
        max_players = max_players_per_team * teams_per_circuit * nb_circuit
        if players < min_players:
            raise Exception(
                f"The amount of players ({players}) is smaller than the minimum amount of players per circuit ({min_players}). "
                "The minimum amount of players per circuit is computed as follows: min_players_per_team * games_per_circuit * 2. "
                "Tune this parameters to fit your needs."
            )
        if min_players <= players <= max_players:
            if players > max_players:
                raise Exception(
                    f"With {nb_circuit}, there must be minimum {min_players} players and maximum {max_players} players."
                    f"There cannot be {players} players then. There is a bug in the computation algorythm."
                )
            players_per_team = players / (teams_per_circuit * nb_circuit)
            print(f"For {players} players, we need {nb_circuit} circuits with around {players_per_team} players per team")
            return nb_circuit
        nb_circuit += 1


def find_array_values(n: int, array_sum: int, min_values: list, max_values: list, y: list):
    """
    This is a combinatorics problem, and I resolved it using chatCPT.
    Find the values of an array of size 'N'. Let's call this array 'x'
    The sum of the values must be 'array_sum'
    Values of 'x' must be higher or equal to 'min_values'
    Values of 'x' must be smaller or equal to 'max_values'
    The result of y/x must be as close as possible to the average of all Y/x values
    Args:
        n: size of the array x
        array_sum: sum of the array values
        min_values: array of minimum values for each value of the array x
        max_values: array of maximum values for each value of the array x
        y: values that we want to divide by x

    Returns: the array x
    """
    # Initialize problem
    prob = LpProblem("Array Values", LpMinimize)

    # Create decision variables for X values
    X = [LpVariable(f"X_{i}", lowBound=min_values[i], upBound=max_values[i], cat='Integer') for i in range(n)]

    # Define decision variables for positive and negative differences
    D1 = [[LpVariable(f"D1_{i}_{j}", lowBound=0, cat='Continuous') for j in range(i + 1, n)] for i in range(n)]
    D2 = [[LpVariable(f"D2_{i}_{j}", lowBound=0, cat='Continuous') for j in range(i + 1, n)] for i in range(n)]

    # Define objective function
    obj_func = lpSum([D1[i][j - i - 1] + D2[i][j - i - 1] for i in range(n - 1) for j in range(i + 1, n)])
    prob += obj_func

    # Define constraints
    prob += lpSum(X) == array_sum
    for i in range(n):
        # prob += X[i] >= min_values[i]
        # prob += X[i] <= max_values[i]
        for j in range(i + 1, n):
            prob += D1[i][j - i - 1] >= y[i] * X[j] - y[j] * X[i]
            prob += D2[i][j - i - 1] >= y[j] * X[i] - y[i] * X[j]

    # Solve problem
    prob.solve()

    # Return X values
    return [value(X[i]) for i in range(n)]


def distribute_teams(sections: list, games_per_circuit: int, min_players_per_team: int, max_players_per_team: int):
    """
    Define how many circuits are needed and how many teams are needed per section.
    It works for one category at a time.
    Instead of returning the results, it modifies the sections list and adds two keys to every section:
        - nb_teams: the number of teams
        - players_per_team: the number of players per team
    Args:
        sections: list of sections for one category of sections
        games_per_circuit:
        min_players_per_team:
        max_players_per_team:

    Returns:
        the number of circuits

    """
    nb_sections = len(sections)
    nb_players = sum([section["players"] for section in sections])
    nb_teams_per_circuit = 2 * games_per_circuit
    nb_circuits = get_nb_circuit(nb_players, nb_teams_per_circuit, min_players_per_team, max_players_per_team)
    nb_teams = nb_circuits * nb_teams_per_circuit

    min_teams = []
    max_teams = []
    players_per_section = []

    for section in sections:
        min_teams.append(math.ceil(section["players"] / max_players_per_team))
        max_teams.append(min(math.floor(section["players"] / min_players_per_team), section["leaders"]))
        players_per_section.append(section["players"])

    # Find the array values
    nb_teams = find_array_values(nb_sections, nb_teams, min_teams, max_teams, players_per_section)

    # Print the result
    print(f"Total: {sum(nb_teams)}")
    if nb_teams is not None:
        for section in sections:
            section["nb_teams"] = nb_teams.pop(0)
            section["players_per_team"] = math.ceil(section["players"] / section["nb_teams"])
            print(f"{section['name']}: {section['nb_teams']} teams")
    else:
        raise Exception("No feasible solution found.")

    return nb_circuits


GAMES_PER_CIRCUIT = 17
MIN_PLAYERS_PER_TEAM = 4
MAX_PLAYERS_PER_TEAM = 10

if __name__ == '__main__':
    # get_nb_circuit(517, 34, 5, 10)
    sample_loups = [
        {"name": "BR002", "players": 55, "leaders": 10},
        {"name": "BR005", "players": 38, "leaders": 6},
        {"name": "HD003", "players": 37, "leaders": 10},
        {"name": "BR015L1", "players": 36, "leaders": 5},
        {"name": "BR015L2", "players": 35, "leaders": 7},
        {"name": "BR017", "players": 34, "leaders": 6},
        {"name": "BR001", "players": 31, "leaders": 7},
        {"name": "BR18RP", "players": 31, "leaders": 8},
        {"name": "BR001", "players": 30, "leaders": 8},
        {"name": "TO009", "players": 26, "leaders": 4},
        {"name": "NM023", "players": 26, "leaders": 9},
        {"name": "BR006", "players": 24, "leaders": 7},
        {"name": "TO003", "players": 21, "leaders": 5},
        {"name": "BR004", "players": 20, "leaders": 9},
        {"name": "BR007", "players": 17, "leaders": 7},
        {"name": "6To", "players": 16, "leaders": 4}
    ]

    sample_lutins = [
        {"name": "BR002", "players": 53, "leaders": 9},
        {"name": "BR002", "players": 40, "leaders": 8},
        {"name": "BR002", "players": 42, "leaders": 9},
        {"name": "BR002", "players": 41, "leaders": 8},
        {"name": "BR002", "players": 35, "leaders": 6},
        {"name": "BR002", "players": 35, "leaders": 7},
        {"name": "BR002", "players": 8, "leaders": 4},
        {"name": "BR002", "players": 33, "leaders": 8},
    ]
    sample_bala = [
        {"name": "BR002", "players": 20,    "leaders": 4},
        {"name": "BR002", "players": 8,     "leaders": 3},
        {"name": "BR002", "players": 37,    "leaders": 8},
        {"name": "BR002", "players": 7,     "leaders": 3},
        {"name": "BR002", "players": 12,    "leaders": 4},
        {"name": "BR002", "players": 16,    "leaders": 6},
        {"name": "BR002", "players": 32,    "leaders": 7},
        {"name": "BR002", "players": 23,    "leaders": 7},
        {"name": "BR002", "players": 14,    "leaders": 5},
    ]
    distribute_teams(sample_loups, GAMES_PER_CIRCUIT, MIN_PLAYERS_PER_TEAM, MAX_PLAYERS_PER_TEAM)
    distribute_teams(sample_lutins, GAMES_PER_CIRCUIT, MIN_PLAYERS_PER_TEAM, MAX_PLAYERS_PER_TEAM)
    distribute_teams(sample_bala, GAMES_PER_CIRCUIT, MIN_PLAYERS_PER_TEAM, MAX_PLAYERS_PER_TEAM)
