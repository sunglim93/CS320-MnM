from random import seed,gauss,choice

# type is like a class of objects and ability would be the name of an object belonging to a type
# the value of an ability corresponds to a specific type
_item_types = {"Attack" : 1, "Defense" : 2, "Consumable" : 3, "Badge" : 4, "Armor" : 5}
_item_abilities = {"Long Sword" : 1, "Sturdy Bone" : 1, "Weak Bow" : 1, "Large Rock" : 1, "Glass Shard" : 1, "Stone Mallet" : 1, "Defense" : 2, "Stale Bread" : 3, "Bone Marrow" : 3, "Some Bugs" : 3, "Raw Meat" : 3, "Good Soup" : 3, "Green Mush" : 3, "Yummy Rock" : 3}

def _randomAbility(typeStr):
    ''' Random Ability
    returns a random ability name based on type value given
    '''
    seed()
    choices = [key for key,val in _item_abilities.items() if val == _item_types[typeStr]]
    return choice(choices)

class Item():
    ''' Item Class
    type is the item type name string that must be a valid Item Master type
    ability is the item's ability name string specified or randomly chosed based on type
    value is a list of numbers specified directly or randomly chosen from given range, 
    the value is meant to be flexible for many types of items

    assortment of random/specific methods for random ability name or values vs specific
    type must be a valid choice from Item Master, ability does not need to be valid

    attack items are allowed to have one value, the attack value
    and defense items are allowed to have one value, the defense modifier
    '''
    def __init__(self):
        self.__type = ""
        self.__ability = ""
        self.__values = []

    def createSpecificItem(self, typeStr, ability, values):
        ''' Create Specific Items
        choose all item values at once and set them directly
        type must be valid
        values can be a list of numerical values or a number
        '''
        if type(values) is list or type(values) is int or type(values) is float:
            if typeStr in _item_types:
                self.__type = typeStr
                self.__ability = ability
                if type(values) is list:
                    if typeStr == "Attack" or typeStr == "Defense":
                        self.__values.append(round(values[0]))
                    else:
                        self.__values.extend(round(values))
                else:
                    self.__values.append(round(values))

    def chooseAbility(self, typeStr, ability):
        ''' Choose Ability
        sets type and ability of choice
        type must be valid
        '''
        if typeStr in _item_types:
            self.__type = typeStr
            self.__ability = ability

    def randomAbility(self, typeStr):
        ''' Random Ability
        sets type and chooses ability randomly based on item type
        type must be valid
        '''
        if typeStr in _item_types:
            # get random ability name
            self.__type = typeStr
            self.__ability = _randomAbility(typeStr)

    def randomValueWideRange(self, min, max, difficulty=None):
        ''' Random Value Wide Range
        chooses random Item value spread over range
        appends Item value list with the randomly chosen number
        can be called multiple times on item with multiple values
        
        the random value follows a normal distribution in the range given, higher difficulty gives wider range of values
        top of curve is always the middle of range
        no difficulty specified follows normal gaussean distibution
        '''
        seed()

        # set default gaussean values within range
        mu = (min+max)/2
        sigma = (max-mu)/4

        # widens distribution with higher difficulty
        if difficulty is not None:
            if difficulty == 0:
                sigma = sigma*1.25
            elif difficulty == 1:
                sigma = sigma*1.5
            elif difficulty == 2:
                sigma = sigma*1.75

        # make sure random value is within range
        randNum = gauss(mu, sigma)
        while randNum > max or randNum < min:
            randNum = gauss(mu, sigma)

        if (self.__type == "Attack" or self.__type == "Defense") and len(self.__values) != 0:
            self.__values[0]=round(randNum)
        else:
            self.__values.append(round(randNum))

    def randomValueTopOfRange(self, min, max, difficulty=None):
        ''' Random Value Top of Range
        chooses random Item value favored towards top of range
        appends Item value list with the randomly chosen number
        can be called multiple times on item with multiple values

        the random value follows a normal distribution in the range given, higher difficulty gives higher favored values
        top of curve shifts towards max range with higher difficulty
        no difficulty specified follows normal gaussean distibution
        '''
        seed()

        # set default gaussean values within range
        mu = (min+max)/2
        sigma = (max-mu)/4

        # shift distribution towards higher end of range with higher difficulty
        if difficulty is not None:
            if difficulty == 0:
                mu = mu*1.1
            elif difficulty == 1:
                mu = mu*1.2
            elif difficulty == 2:
                mu = mu*1.3

        # make sure random value is within range
        randNum = gauss(mu, sigma)
        while randNum > max or randNum < min:
            randNum = gauss(mu, sigma)

        if (self.__type == "Attack" or self.__type == "Defense") and len(self.__values) != 0:
            self.__values[0]=round(randNum)
        else:
            self.__values.append(round(randNum))

    def getItem(self):
        ''' Get Item
        returns a tuple of the item fields
        '''
        return (self.__type, self.__ability, self.__values)

class Armor:
    def __init__(self):
        self.__firstWorldArmor = self.__createFirstWorldArmor()
        self.__secondWorldArmor = self.__createSecondWorldArmor()
        self.__thirdWorldArmor = self.__createThirdWorldArmor()

    def __createFirstWorldArmor(self):
        firstWorldArmor = Item()
        firstWorldArmor.createSpecificItem("Armor", "First", [0.7, 0.75])
        return firstWorldArmor.getItem()

    def __createSecondWorldArmor(self):
        secondWorldArmor = Item()
        secondWorldArmor.createSpecificItem("Armor", "Second", [0.8, 0.85])
        return secondWorldArmor.getItem()

    def __createThirdWorldArmor(self):
        thirdWorldArmor = Item()
        thirdWorldArmor.createSpecificItem("Armor", "Third", [0.9, 0.95])
        return thirdWorldArmor.getItem()
    
    def getArmor(self):
        return (self.__firstWorldArmor, self.__secondWorldArmor, self.__thirdWorldArmor)