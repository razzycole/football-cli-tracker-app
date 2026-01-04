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
    team=[]
    matches=[]
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

    elif number == 1:
        name = input("What is the player name? ")
        print("\nPlayer Management :")
        print("1 → Add a new player")
        print("2 → View players")
        print("3 → Update player stats")

        num1 = int(input("Input the number: "))
        if num1 == 1:
            players.append({
                "name": name,
                "goals": 0,
                "matches": 0,
                "assists": 0
            })

            print("new player added successfully")

            with open("players.json", "w") as f:
              json.dump(players, f)

        elif num1 == 2:
          found=False
          name = input("What is the player name? ")
          for i in players:
            if i["name"] == name:
                print(name)
                found=True
                break
          if not found:
            print("No such player.")

        elif num1 == 3:
          name = input("Which player do you want to update? ")
          found = False

          for player in players:
            if player["name"] == name:
                found = True

                print("1 → Add goals")
                print("2 → Add matches")
                print("3 → Add assists")

                choice = int(input("Choose stat: "))

                if choice == 1:
                    player["goals"] += int(input("Goals to add: "))
                elif choice == 2:
                    player["matches"] += int(input("Matches to add: "))
                elif choice == 3:
                    player["assists"] += int(input("Assists to add: "))
                else:
                    print("Invalid stat choice.")

                with open("players.json", "w") as f:
                    json.dump(players, f)

                print("Stats updated.")
                break

          if not found:
             print("No such player.")


    elif number == 2:
        print("\nTeam Management")
        print("1 → Create a team")
        print("2 → Add players to a team")
        print("3 → View team info")

        num = int(input("input the number: "))

        if num == 1:
            name = (input("What is the team name? "))
            team.append({
                        "name": name,
                        "players":[]
            })
            print("new team added successfully")
            with open("team.json", "w") as t:
                json.dump(team, t)

        elif num == 2:
            user = input("Which team do you want to add? ")
            found = False

            # Show available teams
            for t in team:
                print(t["name"])

            team_name = input("Enter team name: ")

            selected_team = None
            for t in team:
                if t["name"] == team_name:
                    selected_team = t
                    break

            if not selected_team:
                print("Team not found.")
            else:
                while True:
                    user2 = input("Type player name to add (type 'end' to stop): ").strip()

                    if user2.lower() == "end":
                        break

                    # check player exists
                    player_exists = False
                    for p in players:
                        if p["name"] == user2:
                            player_exists = True
                            break

                    if not player_exists:
                        print("Player does not exist.")
                        continue

                    # check player not already in another team
                    already_in_team = False
                    for t in team:
                        if user2 in t["players"]:
                            already_in_team = True
                            break

                    if already_in_team:
                        print("Player already belongs to a team.")
                        continue

                    # add player
                    selected_team["players"].append(user2)
                    print(f"{user2} added to {selected_team['name']}")

            with open("team.json", "w") as t:
                json.dump(team, t)

        elif num == 3:
            mon = input("Which team do you want to view? ")
            found = False
            for i in team:
                if i["name"] == mon:
                    found = True
                    print("name: ", i["name"], "players: ", i["players"])
            if not found:
                    print("Invalid team choice.")



    # ---------- MATCH MANAGEMENT ----------

    elif number == 3:

        if not team or len(team) < 2:
            print("At least 2 teams are required to start a match.")

            continue

        # --- Select Team A ---

        print("\nAvailable teams:")

        for t in team:
            print("-", t["name"])

        while True:

            team_a_name = input("Enter Team A: ").strip()

            team_a = next((t for t in team if t["name"] == team_a_name), None)

            if team_a:
                break

            print("Invalid team choice. Try again.")

        # --- Select Team B ---

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

        # --- Enter match score ---

        team_a_goals = float(input(f"Goals scored by {team_a_name}: "))

        team_b_goals = float(input(f"Goals scored by {team_b_name}: "))

        # --- Assign goals & assists ---

        match_goals = []  # To store goal events


        # Function to assign goals for a team

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

                # Update player stats

                for player in players:

                    if player["name"] == scorer:
                        player["goals"] += 1

                        player["matches"] += 1

                    if assist and player["name"] == assist:
                        player["assists"] += 1

                events.append({"scorer": scorer, "assist": assist})

            # Add remaining players to matches played

            for player_name in team_dict["players"]:

                if player_name not in [e["scorer"] for e in events]:

                    for player in players:

                        if player["name"] == player_name:
                            player["matches"] += 1

            return events


        # Assign goals for both teams

        team_a_events = assign_goals(team_a, team_a_goals, team_a_name)

        team_b_events = assign_goals(team_b, team_b_goals, team_b_name)

        # --- Save match ---

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


    elif number==4:
        print("stat management \n")
        print(" no 1 for player stats? \n")
        print(" no 2 for team stats? \n")
        print(" no 3 for leaderboard \n")

        user_input=int(input( "enter a number: "))

        if user_input == 1:
          name = input("Enter player name: ")
          for i in players:
              if i["name"] == name:
                  print(i["name"], i ["goals"], i ["matches"], i["assists"])
              else:
               print("Invalid player choice. Try again.")

        if user_input == 2:
            Total_goals=0
            Total_assists=0
            Total_matches=0

            name=input("Enter team name: ")
            for i in team:
                if name == i["name"]:
                    print(i["name"], i ["players"])
                if i["players"]:
                    print(i["name"], i["goals"], i["matches"], i["assists"])
                    Total_goals += i["goals"]
                    Total_assists += i["assists"]
                    Total_matches += i["matches"]
                    print("total goals: ", Total_goals)
                    print("total assists: ", Total_assists)
                    print("total matches: ", Total_matches)
            else:
                print("Invalid team choice. Try again.")

        if user_input == 3:
            highest_goals=0
            highest_matches=0
            highest_assists=0

            top_scorer = None
            most_matches = None
            most_assists = None

            for i in players:
                if i["goals"] > highest_goals:
                    highest_goals=i["goals"]
                    top_scorer=i["name"]

            for i in players:
                if i["matches"] > highest_matches:
                    highest_matches=i["matches"]
                    most_matches = i["name"]


            for i in players:
                if i["assists"] > highest_assists:
                    highest_assists=i["assists"]
                    most_assists = i["name"]


            print(top_scorer, ":" "highest goals:", highest_goals, )
            print(most_matches, ":" "highest matches:", highest_matches, )
            print(most_assists, ":" "highest assists:", highest_assists, )