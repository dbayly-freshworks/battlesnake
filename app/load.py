from game import *
import json
import random
# TensorFlow and tf.kerasi
import tensorflow as keras
import tensorflow as tf

# Helper libraries
import numpy as np
model = tf.keras.models.load_model('saved_model/nextgen_1')
probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])
def pickMove(inputs):
    # direction = random.choice(directions)
    directions = []
    values = probability_model.predict([inputs])
    #print(values)
    index = getMaxIndex(values[0])
    #print(index)
    # print(index)
    if(index >= 8):
        directions.append('right')
        index = index - 8
    if(index >= 4):
        directions.append('left')
        index = index - 4
    if(index >= 2):
        directions.append('down')
        index = index -2
    if(index ==1):
        directions.append('up')

    if(len(directions)==0):
        # print('no moves left, killing self')
        return random.choice(['up','down','left','right'])
    return random.choice(directions)
def getMaxIndex(arr):
    maxValue = arr[0]
    index = 0
    counter = 0
    for x in arr:
        if(maxValue < x):
            maxValue = x
            index = counter
        counter = counter + 1
    return index

if __name__ == "__main__":
    games = 100
    inputList = []
    answers = []
    totalTurns = 0
    totalFood = 0
    while(games>0):
        data = json.loads(open('map.json','r').read())
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
        continueGame = True
        turnCounter = 0
        gameInputs = []
        gameAnswers = []
        foodCount = 0
        while(continueGame):
            # increment turn counter
            turnCounter = turnCounter + 1
            # get a blank map
            listMap = getDefaultMap(data["board"]["height"],data["board"]["width"])
            # fill map with data from the model
            filledMap = fillMap(listMap,data)
            printMap(filledMap)
            print()
            inputs = genInputs(filledMap,data)
            data["you"]["health"] = data["you"]["health"]-1 
            move = pickMove(inputs)
            results  = tick(data,move,filledMap)
            # if(turnCounter>90):
            #     print(data["you"]["health"])
            if(data["you"]["health"]>=100):
                foodCount = foodCount + 1
                totalFood = totalFood +1
            continueGame = results[0]
            totalTurns=totalTurns+1
            if(continueGame):
                if(move == 'up'):
                    gameAnswers.append(1)
                elif(move == 'down'):
                    gameAnswers.append(2)
                elif(move == 'left'):
                    gameAnswers.append(4)
                else:
                    gameAnswers.append(8)
                gameInputs.append(inputs)
        games = games -1
        if(foodCount>=4):
            for x in gameAnswers :
                answers.append(x)
            for x in gameInputs :
                inputList.append(x)

        print("Turns:" + str(turnCounter) )
        print("Food:" + str(foodCount ))
        foodCount = 0
    print(str(totalTurns/100))
    print(str(totalFood/100))
    # model.fit(inputList, 
    #     answers,  
    #     epochs=5)
    # model.save('saved_model/nextgen_6') 