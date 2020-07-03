import numpy as np 
from game import *
import json
import random

directions = ['up', 'down', 'left', 'right']
def pickMove(inputs):
    direction = random.choice(directions)
    return direction


if __name__ == "__main__":
    games = 1
    trainingData = []
    answers = []
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
                #printMap(filledMap)
                #generate map based off of 
                
                inputs = genInputs(filledMap,data)
                trainingData.append(inputs)
                data["you"]["health"] = data["you"]["health"]-1 
                roundAnswers= 0
                for z in range(0,4):
                    result = tick(data,directions[z],filledMap)
                    if(result[0]):
                        roundAnswers= roundAnswers + pow(2,z)
                        print(roundAnswers)
                answers.append(roundAnswers)
                move = pickMove(inputs)
                results = tick(data,move,filledMap)
                #tick will increment the game, and return if the game is over and the new board state. ls
                continueGame = results[0]
                data = results[1]
            games = games - 1
            print(turnCounter)
    answersFile = open("testingAnswers.json","w")
    answersFile.write(str(answers))
    trainingDataFile = open("testingData.json","w")
    trainingDataFile.write(str(trainingData))
    answersFile.close()
    trainingDataFile.close()
    
        

