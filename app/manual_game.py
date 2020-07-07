import numpy as np 
from game import *
import json
import random

directions = ['up', 'down', 'left', 'right']
def pickMove():
    move = input("Pick a move, use wasd.")
    if(move == 'w'):
        return ['up',1]
    if(move == 's'):
        return ['down',2]
    if(move == 'a'):
        return ['left',4]
    if(move == 'd'):
        return ['right',8]
    return pickMove()
    


if __name__ == "__main__":
    games = 1 
    trainingData = json.loads(open("trainingData.json","r").read())
    answers = json.loads(open("trainingAnswers.json","r").read())
    while(games>0):
        with open('./map.json') as map_json:
            data = json.load(map_json)
            width = data["board"]["width"]
            height = data["board"]["height"]
            startlocal = {
                "x":np.random.randint(0,width-1),
                "y":np.random.randint(0,height-1)
            }
            data["board"]["snakes"][0]["body"].append(startlocal)
            data["you"]["body"].append(startlocal)
            data["board"]["food"].append({
                "x": (np.random.randint(1,width-1)+startlocal["x"])%width,
                "y": np.random.randint(0,height-1)
            })
            print(data["board"]["food"])
            
            continueGame = True
            turnCounter = 0
            while(continueGame):
                turnCounter = turnCounter +1
                #update the map with the current state, then print it. 
                listMap = getDefaultMap(data["board"]["height"],data["board"]["width"])
                filledMap = fillMap(listMap,data)
                printMap(filledMap)
                #generate map based off of 
                inputs = genInputs(filledMap,data)
                trainingData.append(inputs)
                data["you"]["health"] = data["you"]["health"]-1 
                move = pickMove()
                answers.append(move[1])
                results = tick(data,move[0],filledMap)
                #tick will increment the game, and return if the game is over and the new board state. ls
                continueGame = results[0]
                data = results[1]
            games = games - 1
            print(turnCounter)
    print(str(answers))
    # print(str(trainingData))
    answersFile = open("trainingAnswers.json","w")
    answersFile.write(str(answers))
    trainingDataFile = open("trainingData.json","w")
    trainingDataFile.write(str(trainingData))
    answersFile.close()
    trainingDataFile.close()
    