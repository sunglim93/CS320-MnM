class Achievement():
    name = ""
    message = ""

    def __init__(self, name, message, stats, completed=False):
        '''
        Each achievement is initialized with whether it's completed (default false), 
        its name, display message, and required game statistics to be fulfilled
        stats will be an instance of the game information class
        '''
        self.name = name
        self.message = message
        self.stats = stats
        self.completed = completed

    def getAchievement(self):
        ''' Get Achievement
        returns tuple of achievement fields
        '''
        return (self.name, self.message, self.stats, self.completed)