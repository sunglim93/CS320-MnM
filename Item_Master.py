from random import seed,choice

class Item_Master():
    ''' Item Master Class
    type is a dictionary of type name key to an assigned int value
    ability is a dictionary of ability name key to an assigned int value corresponding to the type it falls into
    these values are defined initially and do not change
    '''
    _type = {"Active" : 1, "Passive" : 2, "Consumable" : 3, "Badge" : 4}
    _ability = {"Attack" : 1, "Defense" : 2, "Regeneration" : 3}

    def randomAbility(self, typeStr):
        ''' Random Ability
        returns a random ability name based on type value given
        '''
        seed()
        choices = [key for key,val in self._ability if val == self._type[typeStr]]
        return choice(choices)