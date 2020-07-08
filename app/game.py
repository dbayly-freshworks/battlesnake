import json
import math
import random

def getDefaultMap(x,y):
    listMap = []
    for i in range (y):
        row = []
        for j in range (x):
            row.append(0)
        listMap.append(row)
    return listMap

def fillMap(listMap,data):
    newMap = listMap
    # print(data["board"]["snakes"])
    for x in data["board"]["snakes"]:
        for y in x["body"]:
            newMap[y["y"]][y["x"]]=1
    for food in data["board"]["food"]:
        newMap[food["y"]][food["x"]] = -1
    return newMap

def printMap(listMap):
    for x in listMap:
        print(x)

def calcDist(x1,y1,x2,y2):
    return math.sqrt(pow(abs(x2-x1),2)+pow(abs(y2-y1),2))

def getDiagonal(head,xMod,yMod,filledMap,xMax,yMax):
    res =0
    x = head["x"]
    y = head["y"]
    while(True):
        x=(res+1)*xMod + head["x"]
        y=(res+1)*yMod + head["y"]
        if(x<0 or y<0 or x>=xMax or y>=yMax):
            return res
        if(filledMap[x][y]==1):
            return res
        res = res + 1



def genInputs(listMap,data):
    inputs = []
    height = data["board"]["height"]
    width = data["board"]["width"]
    head = data["you"]["body"][0]
    nearestFood=data["board"]["food"][0]
    distToNearestFood = calcDist(head["x"],head["y"],nearestFood["x"],nearestFood["y"])
    for food in data["board"]["food"]:
        if calcDist(head["x"],head["y"],food["x"],food["y"])<distToNearestFood:
            distToNearestFood = calcDist(head["x"],head["y"],food["x"],food["y"])
            nearestFood = food
    #Add head
    inputs.append(float(head["x"])/width)
    inputs.append(float(head["y"])/height)
    #Add dist to nearest food
    inputs.append(float((head["x"]-food["x"]))/height)
    inputs.append(float((head["y"]-food["y"]))/height)
    #Add diagonals
    inputs.append(float(getDiagonal(head,-1,1,listMap,width,height))/height)
    inputs.append(float(getDiagonal(head,+1,1,listMap,width,height))/height)
    inputs.append(float(getDiagonal(head,-1,-1,listMap,width,height))/height)
    inputs.append(float(getDiagonal(head,1,-1,listMap,width,height))/height)
    #Add Horizontals and veriticals
    inputs.append(float(getDiagonal(head,0, 1,listMap,width,height))/height)
    inputs.append(float(getDiagonal(head,0,-1,listMap,width,height))/height)
    inputs.append(float(getDiagonal(head,-1,0,listMap,width,height))/height)
    inputs.append(float(getDiagonal(head,1,0,listMap,width,height))/height)
    inputs.append(float(data["you"]["health"])/10)
    #Inputs should be a list with head x, head y, the horizontal and vertical distance to the nearest food. followed by the distance to the nearest wall in each direction and hunger
    for x in range(0,len(inputs)):
        inputs[x]=float(inputs[x]+1)/2
    # print(inputs)
    return inputs
# Increments the board state. Returns wether the game is over or not and 
def tick(data,move,filledMap):
    newData = data
    oldTail = {
        "x":data["you"]["body"][len(data["you"]["body"])-1]["x"],
        "y":data["you"]["body"][len(data["you"]["body"])-1]["y"]
    }
    head = {
        "x":data["you"]["body"][0]["x"],
        "y":data["you"]["body"][0]["y"]
    }
    if(move == "up"):
        head['y'] = head["y"]-1
    elif move == "down":
        head['y'] = head["y"]+1
    elif move ==  "left":
        head['x'] = head["x"]-1
    elif move ==  "right":
        head['x'] = head["x"]+1
    if(head['x']<0 
        or head['y']<0
        or head['x']>=data["board"]["width"]
        or head['y']>=data["board"]["height"]):
        return (False,data)
    if(filledMap[head['y']][head['x']]==1):
        return (False,data)
    if(newData["you"]["health"] < 1 ):
        return [False,newData]
    newData["you"]["body"].pop()
    newData["you"]["body"].insert(0,head)
    possibleFoodLocations = getPossibleFoodLocations(newData)
    for food in data["board"]["food"]:
        #snek eatted the food
        if(food["x"]==head["x"]
            and food["y"]==head["y"]):
            choice = random.choice(possibleFoodLocations)
            newData["board"]["food"].remove(food)
            newData["board"]["food"].append(choice)
            possibleFoodLocations.remove(choice)
            newData["you"]["body"].append(oldTail)
            newData["you"]["health"]=100
    for index in range(len(newData["board"]["snakes"])): 
        if newData["board"]["snakes"][index]["id"] == newData["you"]["id"]:
            newData["board"]["snakes"][index] = newData["you"]
    return [True,newData]

def getPossibleFoodLocations(data):
    locationList = []
    for y in range(data["board"]["height"]):
        for x in range(data["board"]["width"]):
            flag = True
            for snake in data["board"]["snakes"]:
                if({'x': x,'y':y} in snake["body"]):
                    flag = False
                    break
            if(flag):
                locationList.append({'x':x,'y':y})
    return locationList

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
# def main():
#     with open('./app/map.json') as map_json:
#         data = json.load(map_json)
#         continueGame = True
#         turnCounter = 0
#         while(continueGame):
#             turnCounter = turnCounter +1
#             #update the map with the current state, then print it. 
#             listMap = getDefaultMap(data["board"]["height"],data["board"]["width"])
#             filledMap = fillMap(listMap,data)
#             printMap(filledMap)
#             #generate map based off of 
#             move = pickMove(genInputs(filledMap,data))
#             results = tick(data,move,filledMap)
#             #tick will increment the game, and return if the game is over and the new board state. ls
#             continueGame = results[0]
#             data = results[1]
        
# if __name__ == '__main__':
#     main()