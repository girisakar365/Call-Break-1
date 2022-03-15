# This contains the basic code that you will need to view the game on the snadbox.
# You will provide all the moves of all the bots in the sandbox.
# The sandbox is for testing purposes only so, the API data format can change
# when quelifiers begin.
# The sandbox is provided so that you can get familiar with buliding bots before
#  the event actually begings.

# To seutp: `pip install flask, flask_cors`
# To run: python app.py

import json
from Logic import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/bid", methods=["POST"])
def bid():
    """
    Bid is called at the starting phase of the game in callbreak.
    You will be provided with the following data:
    {
        "matchId": "M1",
        "playerId": "P3",
        "cards": ["1S", "TS", "8S", "7S", "6S", "4S", "3S", "9H", "6H", "5H", "1C", "1D", "JD"],
        "context": {
            "round": 1,
            "players": {
            "P3": {
                "totalPoints": 0,
                "bid": 0
            },
            "P0": {
                "totalPoints": 0,
                "bid": 3
            },
            "P2": {
                "totalPoints": 0,
                "bid": 3
            },
            "P1": {
                "totalPoints": 0,
                "bid": 3
            }
            }
        }
    }
    This is all the data that you will require for the bidding phase.
    """

    body = request.get_json()
    # print(json.dumps(body, indent=2))

    ####################################

    cards = body["cards"]
    player = body["playerId"]

    # return should have a single field value which should be an int reprsenting the bid value
    return jsonify({"value": bid_calculator(cards)})


@app.route("/play", methods=["POST"])
def play():
    """
    Play is called at every hand of the game where the user should throw a card.
    Request data format:
    {
        "matchId": "M1",
        "playerId": "P1",
        "cards": [ "QS", "9S", "2S", "KH", "JH", "4H", "JC", "9C", "7C", "6C", "8D", "6D", "3D"],
        "played": [
            "2H/0",
            "8H/0"
        ],
        "history": [
            [1, ["TS/0", "KS/0", "1S/0", "5S/0"], 3],
            [3, ["QS/0", "6S/0", "TH/0", "2S/0"], 3],
        ],
        "players": ["P0", "P1", "P2", "P3"]
    }
    The `played` field contins all the cards played this turn in order.
    'history` field contains an ordered list of cards played from first hand.
    Format: `start idx, [cards in clockwise order of player ids], winner idx`
        `start idx` is index of player that threw card first
        `winner idx` is index of player who won this hand
    `players`: list of ids in clockwise order (always same for a game)
    """
    body = request.get_json()
    # print(json.dumps(body, indent=2))

    ####################################
    cards = body['cards']  # list of cards in hand
    played = body['played']  # list of cards played this turn
    history = body['history']  # list of cards played from first hand
    print('PLAYED: ' + str(played))
    print('CARDS: ' + str(cards))
    print('HISTORY: ' + str(history))
    ####################################
    # return should have a single field value
    # which should be an int representing the index of the card to play
    # e.g> {"value": body.cards.index("QS")}
    # to play the card "QS"
    print(logic(played, cards, history))
    return jsonify({"value": logic(played, cards, history)})


# do not change this port; the sandbox server hits this port on localhost
app.run(port=7000)
