import json

def print_menu():
        print("=== Football Tracker ===")
        print("1. Add game")
        print("2. Show all games")
        print("3. Quit")

def add_game():
    try:
        with open("games.json", "r") as f:
            games = json.load(f)

    except(FileNotFoundError, json.JSONDecodeError):
        games = []

    game_dict = {
        "home": input("Home team: "),
        "away": input("Away team: "),
        "date": input("Date: ")
    }
        
    games.append(game_dict)

    with open("games.json", "w") as f:
        json.dump(games, f)

def show_games():
    try:
        with open("games.json", "r") as f:
            games = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        games = []

    if not games:
        print("No games found.")
    else:
        for i, game in enumerate(games):
            print(f"{i+1}. {game['home']} vs {game['away']} - {game['date']}")

user_input = ''

while user_input != '3':
    print_menu()
    user_input = input("what's next? ")
    if user_input == '1':
        add_game()
    elif user_input == '2':
        show_games()
    elif user_input == '3':
        print('Quitting...')
    else:
        print("not a valid option! - try again")
        