import requests
import time

# === CONFIG ===
LEAGUE_ID = "12557"  # your FPL Draft league ID

TEAM_OWNERS = {
    51777: "Andy",
    51792: "Ali",
    51771: "Jim",
    51755: "Sam",
    51778: "Rhys",
    51773: "Roz",
    51753: "Steve",
    51760: "Jord",
    51690: "Joe",
    51757: "Liam"
}

def get_standings_message(league_id=LEAGUE_ID):
    # Get team names
    details_url = f"https://draft.premierleague.com/api/league/{league_id}/details"
    details = requests.get(details_url).json()
    teams = {entry["id"]: entry["entry_name"] for entry in details["league_entries"]}

    # Get standings
    standings = details["standings"]

    print(details)

    # Build formatted message
    message_lines = ["📊 *Current League Standings* 📊\n"]
    for row in standings:
        id = row["league_entry"]
        team_name = teams.get(id, f"Team {id}")
        rank = row["rank"]
        pts = row["total"]
        # played = row["matches_played"]

        # Add emojis for fun
        if rank == 1:
            medal = "🥇"
        elif rank == 2:
            medal = "🥈"
        elif rank == 3:
            medal = "🥉"
        else:
            medal = "⚽"

        message_lines.append(f"{medal} {rank}. *{TEAM_OWNERS[id]}* {team_name} — {pts} pts")

    return "\n".join(message_lines)
    
def get_and_process_queue_message():
	queue__consume_url = "http://localhost:5001/consume/fpl"
	queue_publish_base_url = "http://localhost:5001/publish"
	
	message = requests.get(queue__consume_url).json()
	
	if("status" in message and message["status"] == "empty"):
		return
	
	action = message["action"]
	reply_to = message["reply_to"]
	
	if(action.startswith("!standings")):
		print("Getting standings")
		standings = get_standings_message()
		queue_publish_url = queue_publish_base_url + "/" + reply_to
		print("Sending standings to queue: " + queue_publish_url)
		response = requests.post(queue_publish_url, json={"message": standings})
		print(response.text)
	else:
		print("Unsupported: " + action)
    
while(True):
	time.sleep(100/1000)
	
	get_and_process_queue_message()
 
