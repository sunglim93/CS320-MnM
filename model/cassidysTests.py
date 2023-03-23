import unittest
from model import item

class ItemTestMethods(unittest.TestCase):
    ''' Unit testing of item module and class
    White Box testing function/statement/branch coverage
    Tests all methods for statement and branch coverage except the random value methods, 
    which uses random gaussean and was tested at creation by hand and graphed (without automated methods)
    '''

    # Testing of item class object creation
    '''
    _item_types = {"Active" : 1, "Passive" : 2, "Consumable" : 3, "Badge" : 4}
    _item_abilities = {"Attack" : 1, "Defense" : 2, "Regeneration" : 3}
    class Item():
    def __init__(self):
        self.__type = ""
        self.__ability = ""
        self.__values = []

    def getItem(self):
        return (self.type, self.ability, self.values)'''
    def testEmptyItemClass(self):
        # white box function coverage
        newItem = item.Item()
        itemTuple = newItem.getItem()
        self.assertEqual(("","",[]),itemTuple)

    # Testing of specific item method
    '''
    def createSpecificItem(self, typeStr, ability, values):
        if type(values) is list or type(values) is int or type(values) is float:
            if typeStr in _item_types:
                self.__type = typeStr
                self.__ability = ability
                if type(values) is list:
                    self.__values.extend(values)
                else:
                    self.__values.append(values)'''
    def testSpecificItemIncorrectType(self):
        # white box branch coverage, 100% with all testSpecificItem tests
        newItem = item.Item()
        newItem.createSpecificItem("Incorrect", "Any", 10)
        itemTuple = newItem.getItem()
        self.assertEqual(("","",[]),itemTuple)
    
    def testSpecificItemIncorrectValueType(self):
        # white box branch coverage, 100% with all testSpecificItem tests
        newItem = item.Item()
        newItem.createSpecificItem("Incorrect", "Any", "Bang")
        itemTuple = newItem.getItem()
        self.assertEqual(("","",[]),itemTuple)

    def testSpecificItemNumber(self):
        # white box branch coverage, 100% with all testSpecificItem tests
        newItem = item.Item()
        newItem.createSpecificItem("Active", "Spear", 10)
        itemTuple = newItem.getItem()
        self.assertEqual(("Active", "Spear", [10]), itemTuple)

    def testSpecificItemList(self):
        # white box branch coverage, 100% with all testSpecificItem tests
        newItem = item.Item()
        newItem.createSpecificItem("Active", "Spear", [10])
        itemTuple = newItem.getItem()
        self.assertEqual(("Active", "Spear", [10]), itemTuple)

    def testSpecificItemMultipleValues(self):
        # white box branch coverage, 100% with all testSpecificItem tests
        newItem = item.Item()
        newItem.createSpecificItem("Active", "Spear", [10, 20, 30])
        itemTuple = newItem.getItem()
        self.assertEqual(("Active", "Spear", [10, 20, 30]), itemTuple)

    # Testing of choose ability method
    '''
    def chooseAbility(self, typeStr, ability):
        if typeStr in _item_types:
            self.__type = typeStr
            self.__ability = ability'''
    def testChooseAbilityIncorrectType(self):
        # white box branch coverage, 100% with testChooseAbility
        newItem = item.Item()
        newItem.chooseAbility("Incorrect", "Any")
        itemTuple = newItem.getItem()
        self.assertEqual(("","",[]),itemTuple)

    def testChooseAbility(self):
        # white box branch coverage, 100% with testChooseAbilityIncorrectType
        newItem = item.Item()
        newItem.chooseAbility("Passive", "Defense")
        itemTuple = newItem.getItem()
        self.assertEqual(("Passive","Defense",[]),itemTuple)

    # Testing of random ability method
    '''
    def _randomAbility(typeStr):
        seed()
        choices = [key for key,val in _item_abilities.items() if val == _item_types[typeStr]]
        return choice(choices)

    def randomAbility(self, typeStr):
        if typeStr in _item_types:
            self.__type = typeStr
            self.__ability = _randomAbility(typeStr)'''
    def testRandomAbilityIncorrectType(self):
        # white box branch coverage, 100% with testRandomAbility
        newItem = item.Item()
        newItem.randomAbility("Incorrect")
        itemTuple = newItem.getItem()
        self.assertEqual(("","",[]),itemTuple)

    def testRandomAbility(self):
        # white box branch coverage, 100% with testRandomAbilityIncorrectType
        newItem = item.Item()
        newItem.randomAbility("Active")
        itemTuple = newItem.getItem()
        self.assertEqual(("Active","Attack",[]),itemTuple)

    # Testing rondom value spread over range
    '''
    def randomValueWideRange(self, min, max, difficulty=None):
        seed()
        mu = (min+max)/2
        sigma = (max-mu)/4
        if difficulty is not None:
            if difficulty == 0:
                sigma = sigma*1.25
            elif difficulty == 1:
                sigma = sigma*1.5
            elif difficulty == 2:
                sigma = sigma*1.75
        randNum = gauss(mu, sigma)
        while randNum > max or randNum < min:
            randNum = gauss(mu, sigma)
        self.__values.append(round(randNum, 2))'''
    def testRandomValueWideRange(self):
        # white box function coverage
        newItem = item.Item()
        newItem.randomValueWideRange(20, 40, 1)
        itemTuple = newItem.getItem()
        self.assertTrue(itemTuple[2][0] >= 20 and itemTuple[2][0] <= 40)

    # Testing random value favored towards top of range
    '''
    def randomValueTopOfRange(self, min, max, difficulty=None):
        seed()
        mu = (min+max)/2
        sigma = (max-mu)/4
        if difficulty is not None:
            if difficulty == 0:
                mu = mu*1.1
            elif difficulty == 1:
                mu = mu*1.2
            elif difficulty == 2:
                mu = mu*1.3
        randNum = gauss(mu, sigma)
        while randNum > max or randNum < min:
            randNum = gauss(mu, sigma)
        self.__values.append(round(randNum, 2))'''
    def testRandomValueTopOfRange(self):
        # white box function coverage
        newItem = item.Item()
        newItem.randomValueTopOfRange(20, 40, 1)
        itemTuple = newItem.getItem()
        self.assertTrue(itemTuple[2][0] >= 20 and itemTuple[2][0] <= 40)

class ArmorTestMethods(unittest.TestCase):
    '''Integration tests the item creation via Item class in the Armor class
        and black box acceptance tests armor requirement'''
    '''
    # Testing of armor class creation
    class Armor:
        def __init__(self):
            self.firstWorldArmor = self.__createFirstWorldArmor()
            self.secondWorldArmor = self.__createSecondWorldArmor()
            self.thirdWorldArmor = self.__createThirdWorldArmor()

        def __createFirstWorldArmor(self):
            firstWorldArmor = Item()
            firstWorldArmor.createSpecificItem("Armor", "First", [0.7, 0.75])
            return firstWorldArmor.getItem()

        def __createSecondWorldArmor(self):
            secondWorldArmor = Item()
            secondWorldArmor.createSpecificItem("Armor", "First", [0.8, 0.85])
            return secondWorldArmor.getItem()

        def __createThirdWorldArmor(self):
            thirdWorldArmor = Item()
            thirdWorldArmor.createSpecificItem("Armor", "First", [0.9, 0.95])
            return thirdWorldArmor.getItem()
    
        def getArmor(self):
            return (self.firstWorldArmor, self.secondWorldArmor, self.thirdWorldArmor)'''
    
    def testArmor(self):
        # acceptance test verifies requirement that there will be 3 armors, one for each world
        armor = item.Armor()
        armorTuple = armor.getArmor()
        self.assertEqual(3, len(armorTuple))

    def testArmorContents(self):
        # acceptance test verifies requirement that the three armors will be unique
        armor = item.Armor()
        armorTuple = armor.getArmor()
        self.assertEqual((("Armor", "First", [0.7, 0.75]),("Armor", "Second", [0.8, 0.85]),("Armor", "Third", [0.9, 0.95])),armorTuple)
