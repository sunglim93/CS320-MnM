class Achievement_List():
    '''
    return lists of the name, message, and game stats of all achievements, predetermined
    '''

    def _gameplayAchievements(self):
        ''' Gameplay Achievements
        yields each achievement
        '''
        pass

    def _hiddenAchievements(self):
        ''' Hidden Achievements
        yields each achievement
        '''
        pass

class Achievement():
    '''
    Each achievement is initialized with whether it's completed (default false), 
    its name, display message, and required game statistics to be fulfilled
    stats is an instance of the game information class
    '''
    name = ""
    message = ""

    def __init__(self, name, message, stats, completed=False):
        self.name = name
        self.message = message
        self._stats = stats
        self._completed = completed

    def _completeAchievement(self):
        self.completed = True
    
    def getAchievement(self):
        ''' Get Achievement
        returns tuple of achievement fields
        '''
        return (self.name, self.message, self._stats, self._completed)

    def getStats(self):
        return self._stats

    def getCompleted(self):
        return self._completed

class Achievement_Master():
    '''
    one instance of achievement master is initilized at beginning of game and should handle all achievements,
    the achievement lists initialization is only permitted to happen once at achivement master initialization
    checkAchievements function should be used to handle achievements throughout game
    '''
    _gameplayAchievements = []
    _hiddenAchievements = []
    __initialized = False

    def __init__(self):
        ''''''
        achievement_list = Achievement_List()
        self.__initializeGameAchievements(achievement_list)
        self.__initializeHiddenAchievements(achievement_list)
        self.__initialized = True

    def checkAchievements(self):
        ''' Check Achievements
        checks game information to see if any achievements have been fulfilled
        and marks them as completed
        '''
        pass

    def __displayMessage(self):
        ''' Display Message
        displays message on screen indicating achievement has been met
        accessed from checkAchievements
        '''
        pass

    def __updateProfile(self):
        ''' Update Profile
        updates the hidden achievements in the player's profile
        accessed from checkAchievements
        '''
        pass
    
    def __initializeGameAchievements(self, achievement_list):
        ''' Initialize Game Achievements
        creates all gameplay achievements and adds them to gameplayAchievements field
        accessed from init only
        '''
        if not self.__initialized:
            for newAch in achievement_list._gameplayAchievements():
                achievement = Achievement(newAch[0], newAch[1], newAch[2])
                self._gameplayAchievements.append(achievement)
            

    def __initializeHiddenAchievements(self, achievement_list):
        ''' Initialize Hidden Achievements
        if profile has any hidden achievements, initializes hiddenAchievements field to the profile's, 
        otherwise creates all hidden achievements and adds them to hiddenAchievements field
        accessed from init only
        '''
        if not self.__initialized:
            for newAch in achievement_list._hiddenAchievements():
                achievement = Achievement(newAch[0], newAch[1], newAch[2])
                self._hiddenAchievements.append(achievement)