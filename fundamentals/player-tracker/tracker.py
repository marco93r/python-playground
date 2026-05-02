import json

def print_menu():
        print("=== Player Tracker ===")
        print("1. Add player")
        print("2. Show all players")
        print("3. Quit")

def add_player():
    try:
        with open("players.json", "r") as f:
            players = json.load(f)

    except(FileNotFoundError, json.JSONDecodeError):
        players = []

    while True:
        try:
            name = input("Player name: ")
            team = input("Player team: ")
            goals = int(input("Goals scored: "))
            break
        except ValueError:
            print("Has to be a number, try again...")


    player_dict = {
        "name": name,
        "team": team,
        "goals": goals
    }

        
    players.append(player_dict)

    with open("players.json", "w") as f:
        json.dump(players, f)

def show_players():
    try:
        with open("players.json", "r") as f:
            players = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        players = []

    if not players:
        print("No players found.")
    else:
        for i, player in enumerate(players):
            print(f"{i+1}. {player['name']}, {player['team']} - {player['goals']} goals scored")

user_input = ''

while user_input != '3':
    print_menu()
    user_input = input("what's next? ")
    if user_input == '1':
        add_player()
    elif user_input == '2':
        show_players()
    elif user_input == '3':
        print('Quitting...')
    else:
        print("not a valid option! - try again")