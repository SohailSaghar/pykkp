import json
from pymongo import MongoClient
import requests
import time


def save_and_get_game_id(player, collection):
    url_for_skyline = f"https://jstris.jezevec10.com/u/{player}/stats?mode=1"
    response_for_skyline = requests.get(url_for_skyline)
    # a bit of scraping magic but basically what it does is that it finds line 287 in the source code
    # which is the line where all coordinates of the graph that the site makes are located.
    skyline = response_for_skyline.text.split("\n")[286].split(" = ")[1]
    list_of_points = json.loads(skyline[1:len(skyline) - 2])["skyline"]
    for games in list_of_points:
        if int(games["id"]) > 55000000 and int(games["y"]) < 21:
            time.sleep(0.2)
            url_for_replay = f"https://jstris.jezevec10.com/replay/data?id={games['id']}&type=0"
            response_for_replay = requests.get(url_for_replay)
            if len(response_for_replay.text) > 2:
                print(f"inserting for {player}")
                json_formatted_response_for_replay = json.loads(response_for_replay.text)
                collection.insert_one(json_formatted_response_for_replay)


def main():
    client = MongoClient("localhost", 27017)
    db = client["jstris"]
    games = db["games"]
    players = db["playernames"]
    player_names = list(players.find())
    for player_name in player_names:
        save_and_get_game_id(player_name, games)


if __name__ == '__main__':
    main()
    
