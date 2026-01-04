import json

# ---------- LOAD DATA ----------
try:
    with open("players.json", "r") as p:
        players = json.load(p)
    with open("team.json", "r") as t:
        team = json.load(t)
    with open("matches.json", "r") as m:
        matches = json.load(m)
except FileNotFoundError:
    players = []
    team = []
    matches = []

# ---------- MAIN LOOP ----------
while True:
    print("\nHello! What do you want to do?")
    print("1 → Player management")
    print("2 → Team management")
    print("3 → Match management")
    print("4 → View stats / leaderboards")
    print("5 → Exit")

    number = int(input("Input the number: "))

    if number == 5:
        print("Exiting program...")
        break

    # ---------- PLAYER MANAGEMENT ----------
    elif number == 1:
        print("\nPlayer Management :")
        print("1 → Add a new player")
        print("2 → View player stats")
        print("3 → Update player stats")

        num1 = int(input("Input the number: "))

        if num1 == 1:
            name = input("What is the player name? ")
            players.append({
                "name": name,
                "goals": 0,
                "matches": 0,
                "assists": 0
            })
            print("New player added successfully")
            with open("players.json", "w") as f:
                json.dump(players, f, indent=4)

        elif num1 == 2:
            name = input("Enter player name: ")
            found = False
            for player in players:
                if player["name"] == name:
                    print(f"{player['name']} → Goals: {player['goals']}, Matches: {player['matches']}, Assists: {player['assists']}")
                    found = True
                    break
            if not found:
                print("Player not found.")

        elif num1 == 3:
            name = input("Which player do you want to update? ")
            found = False
            for player in players:
                if player["name"] == name:
                    found = True
                    print("1 → Add goals")
                    print("2 → Add assists")
                    choice = int(input("Choose stat: "))
                    if choice == 1:
                        player["goals"] += int(input("Goals to add: "))
                    elif choice == 2:
                        player["assists"] += int(input("Assists to add: "))
                    else:
                        print("Invalid stat choice.")
                    with open("players.json", "w") as f:
                        json.dump(players, f, indent=4)
                    print("Stats updated.")
                    break
            if not found:
                print("Player not found.")

    # ---------- TEAM MANAGEMENT ----------
    elif number == 2:
        print("\nTeam Management")
        print("1 → Create a team")
        print("2 → Add players to a team")
        print("3 → View team info")

        num = int(input("Input the number: "))

        if num == 1:
            name = input("What is the team name? ")
            team.append({"name": name, "players": []})
            print("New team added successfully")
            with open("team.json", "w") as t_file:
                json.dump(team, t_file, indent=4)

        elif num == 2:
            # Show teams
            print("Available teams:")
            for t in team:
                print("-", t["name"])

            team_name = input("Enter team name to add players: ")
            selected_team = next((t for t in team if t["name"] == team_name), None)
            if not selected_team:
                print("Team not found.")
            else:
                while True:
                    player_name = input("Type player name to add (type 'end' to stop): ").strip()
                    if player_name.lower() == "end":
                        break
                    # Check player exists
                    if not any(p["name"] == player_name for p in players):
                        print("Player does not exist.")
                        continue
                    # Check not already in another team
                    if any(player_name in t["players"] for t in team):
                        print("Player already belongs to a team.")
                        continue
                    # Add player
                    selected_team["players"].append(player_name)
                    print(f"{player_name} added to {selected_team['name']}")

                with open("team.json", "w") as t_file:
                    json.dump(team, t_file, indent=4)

        elif num == 3:
            team_name = input("Which team do you want to view? ")
            selected_team = next((t for t in team if t["name"] == team_name), None)
            if not selected_team:
                print("Invalid team choice.")
            else:
                print(f"\nTeam: {selected_team['name']}")
                print("Players:", selected_team["players"])

    # ---------- MATCH MANAGEMENT ----------
    elif number == 3:
        if len(team) < 2:
            print("At least 2 teams are required to start a match.")
            continue

        # Select Team A
        print("\nAvailable teams:")
        for t in team:
            print("-", t["name"])
        while True:
            team_a_name = input("Enter Team A: ").strip()
            team_a = next((t for t in team if t["name"] == team_a_name), None)
            if team_a:
                break
            print("Invalid team choice. Try again.")

        # Select Team B
        print("\nAvailable teams:")
        for t in team:
            print("-", t["name"])
        while True:
            team_b_name = input("Enter Team B: ").strip()
            if team_b_name == team_a_name:
                print("Team B cannot be the same as Team A. Try again.")
                continue
            team_b = next((t for t in team if t["name"] == team_b_name), None)
            if team_b:
                break
            print("Invalid team choice. Try again.")

        print(f"\nMatch: {team_a_name} vs {team_b_name}")

        # Enter match score
        team_a_goals = int(input(f"Goals scored by {team_a_name}: "))
        team_b_goals = int(input(f"Goals scored by {team_b_name}: "))

        # Assign goals & assists
        def assign_goals(team_dict, goals, team_label):
            events = []
            if goals > 0:
                print(f"\nAssigning {goals} goals for {team_label}:")
            for g in range(1, goals + 1):
                while True:
                    scorer = input(f"Goal {g} scorer: ").strip()
                    if scorer in team_dict["players"]:
                        break
                    print("Player not in team. Try again.")
                assist = input("Assist by (leave blank if none): ").strip()
                if assist and assist not in team_dict["players"]:
                    print("Assist player not in team, ignoring assist.")
                    assist = ""
                for player in players:
                    if player["name"] == scorer:
                        player["goals"] += 1
                    if assist and player["name"] == assist:
                        player["assists"] += 1
                events.append({"scorer": scorer, "assist": assist})
            # Increment matches for all players
            for player_name in team_dict["players"]:
                for player in players:
                    if player["name"] == player_name:
                        player["matches"] += 1
            return events

        team_a_events = assign_goals(team_a, team_a_goals, team_a_name)
        team_b_events = assign_goals(team_b, team_b_goals, team_b_name)

        # Save match
        match = {
            "team_a": team_a_name,
            "team_b": team_b_name,
            "team_a_goals": team_a_goals,
            "team_b_goals": team_b_goals,
            "team_a_events": team_a_events,
            "team_b_events": team_b_events
        }
        matches.append(match)

        # Save updated data
        with open("matches.json", "w") as m_file:
            json.dump(matches, m_file, indent=4)
        with open("players.json", "w") as p_file:
            json.dump(players, p_file, indent=4)

        print("\nMatch saved successfully!")

    # ---------- VIEW STATS / LEADERBOARDS ----------
    elif number == 4:
        print("\n1 → Player stats")
        print("2 → Team stats")
        print("3 → Leaderboard")

        user_input = int(input("Enter a number: "))

        # Player stats
        if user_input == 1:
            name = input("Enter player name: ")
            found = False
            for player in players:
                if player["name"] == name:
                    print(f"{player['name']} → Goals: {player['goals']}, Matches: {player['matches']}, Assists: {player['assists']}")
                    found = True
                    break
            if not found:
                print("Player not found.")

        # Team stats
        elif user_input == 2:
            team_name = input("Enter team name: ")
            selected_team = next((t for t in team if t["name"] == team_name), None)
            if not selected_team:
                print("Invalid team choice.")
            else:
                total_goals = total_assists = total_matches = 0
                print(f"\nTeam: {selected_team['name']}")
                print("Players and individual stats:")
                for player_name in selected_team["players"]:
                    for player in players:
                        if player["name"] == player_name:
                            print(f"{player['name']} → Goals: {player['goals']}, Matches: {player['matches']}, Assists: {player['assists']}")
                            total_goals += player["goals"]
                            total_assists += player["assists"]
                            total_matches += player["matches"]
                print("\nCumulative team stats:")
                print(f"Total Goals: {total_goals}")
                print(f"Total Assists: {total_assists}")
                print(f"Total Matches: {total_matches}")

        # Leaderboard
        elif user_input == 3:
            highest_goals = highest_matches = highest_assists = 0
            top_scorer = most_matches = most_assists = None
            for player in players:
                if player["goals"] > highest_goals:
                    highest_goals = player["goals"]
                    top_scorer = player["name"]
                if player["matches"] > highest_matches:
                    highest_matches = player["matches"]
                    most_matches = player["name"]
                if player["assists"] > highest_assists:
                    highest_assists = player["assists"]
                    most_assists = player["name"]
            print(f"Top Scorer → {top_scorer}: {highest_goals} goals")
            print(f"Most Matches → {most_matches}: {highest_matches} matches")
            print(f"Most Assists → {most_assists}: {highest_assists} assists")
