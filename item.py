from random import seed,gauss

class Item():
    ''' Item Class
    type is a dictionary of type name key to an assigned int value
    ability is a dictionary of int name key assigned to an ability name value
    these values are defined initially and do not change
    an item is defined as a tuple of item name (ability) and number value
    '''
    __type = {}
    __ability = {}

    def __init__(self, difficulty):
        self.__type = {"Active" : 1, "Passive" : 2, "Consumable" : 3, "Badge" : 4}
        self.__ability = {1 : "Attack", 2 : "Defense", 3 : "Regeneration"}

    def __randomAbility(self, type):
        ''' Random Ability
        returns a random ability name based on type value given
        '''
        if type == 1:
            return self.__ability[1]
        if type == 2:
            return self.__ability[2]
        if type == 3:
            return self.__ability[3]

    def getRandomItemRange(self, typeStr, difficulty, min, max):
        ''' Get Random Item spread over range
        returns a tuple of a random ability with a randomly assigned value based on the difficulty
        the random value follows a normal distribution in the range given, higher difficulty gives wider range of values
        top of curve is always the middle of range
        '''
        seed()
        if typeStr in self.__type:
            # get random ability name
            ability = self.__randomAbility(self.__type[typeStr])
            
            # set default gaussean values within range
            mu = (min+max)/2
            sigma = (max-mu)/4

            # shift distribution outwards with higher difficulty
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

            return (ability, randNum)
        return False

    def getRandomItemBetter(self, typeStr, difficulty, min, max):
        ''' Get Random Item favored towards top of range
        returns a tuple of a random ability with a randomly assigned value based on the difficulty
        the random value follows a normal distribution in the range given, higher difficulty gives higher favored values
        top of curve is towards max range with higher difficulty
        '''
        seed()
        if typeStr in self.__type:
            # get random ability name
            ability = self.__randomAbility(self.__type[typeStr])
            
            # set default gaussean values within range
            mu = (min+max)/2
            sigma = (max-mu)/4

            # shift distribution towards higher end of range with higher difficulty
            if difficulty == 0:
                mu = mu*1.25
            elif difficulty == 1:
                mu = mu*1.5
            elif difficulty == 2:
                mu = mu*1.75

            # make sure random value is within range
            randNum = gauss(mu, sigma)
            while randNum > max or randNum < min:
                randNum = gauss(mu, sigma)

            return (ability, randNum)
        return False