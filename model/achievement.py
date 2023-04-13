class GameStats():
    # keeps track of combat statistics
    # each stat modifier checks for achievement completion

    def __init__(self):
        self.achievements = Achievement_Master(self)
        self.__damage_delt = 0
        self.__damage_taken = 0
        self.__bosses_defeated = 0
        self.__battles_won = 0
        self.__battles_lost = 0

    def set_damage_delt(self, dmg):
        # add amount of damage delt each time player damages enemy
        self.__damage_delt += dmg
        self.achievements.checkAchievements()

    def set_damage_taken(self, dmg):
        # add amount of damage taken each time enemy damages player
        self.__damage_taken += dmg
        self.achievements.checkAchievements()

    def set_bosses_defeated(self):
        # each world has one boss fight, increase each time boss battle is won
        self.__bosses_defeated += 1
        self.achievements.checkAchievements()
        self._reset_battles()

    def set_battles_won(self):
        # increases for every non boss battle won
        self.__battles_won += 1
        self.achievements.checkAchievements()
        self._reset_damage()

    def set_battles_lost(self):
        # increases for every non boss battle lost
        self.__battles_lost += 1
        self.achievements.checkAchievements()
        self._reset_damage()

    def _reset_damage(self):
        # resets damage stats at the end of each battle
        self.__damage_delt = 0
        self.__damage_taken = 0

    def _reset_battles(self):
        # resets battle stats at the end of each world (when boss stat goes up)
        self.__battles_lost = 0
        self.__battles_won = 0

    def resetStatsAndAchievements(self):
        self.__battles_lost = 0
        self.__battles_won = 0
        self.__bosses_defeated = 0
        self.__damage_delt = 0
        self.__damage_taken = 0
        self.achievements._resetAchievements()

    def get_damage_delt(self):
        return self.__damage_delt

    def get_damage_taken(self):
        return self.__damage_taken

    def get_bosses_defeated(self):
        return self.__bosses_defeated

    def get_battles_won(self):
        return self.__battles_won

    def get_battles_lost(self):
        return self.__battles_lost
    
    def get_all_stats(self):
        return (self.__damage_delt, self.__damage_taken, self.__bosses_defeated, self.__battles_won, self.__battles_lost)

class Achievement():
    '''
    Each achievement is initialized with whether it's completed (default false), 
    its display message, and required game statistics to be fulfilled
    stats is an instance of the game information class
    '''

    def __init__(self, message, stats, completed=False):
        self.message = message
        self._stats = stats
        self._completed = completed

    def completeAchievement(self):
        self._completed = True

class Achievement_Master():
    '''
    one instance of achievement master is initilized at beginning of game and should handle all achievements,
    the achievement lists initialization is only permitted to happen once at achivement master initialization
    checkAchievements function should be used to handle achievements throughout game
    '''
    __initialized = False
    _gameplayAchievements = []
    _hiddenAchievements = []

    def __init__(self, stats):
        self.__stats = stats
        self.__initializeGameAchievements()
        self.__initializeHiddenAchievements()
        self.__initialized = True

    def checkAchievements(self):
        ''' Check Achievements
        checks game information to see if any achievements have been fulfilled
        marks them as completed
        '''
        for ach in self._gameplayAchievements:
            if not ach._completed:
                if self.__checkStats(ach._stats):
                    ach.completeAchievement()

        for ach in self._hiddenAchievements:
            if not ach._completed:
                if self.__checkStats(ach._stats):
                    ach.completeAchievement()

    def getCompletedAchievements(self):
        ''' Get Completed Achievements
        yields messages of all completed achievements
        '''
        for ach in self._gameplayAchievements:
            if ach._completed:
                yield ach.message

        for ach in self._hiddenAchievements:
            if ach._completed:
                yield ach.message

    def _resetAchievements(self):
        self.__initialized = False
        self._gameplayAchievements = []
        self._hiddenAchievements = []
        self.__initializeGameAchievements()
        self.__initializeHiddenAchievements()
        self.__initialized = True

    def __checkStats(self, stats):
        cur_stats = self.__stats.get_all_stats()
        for i in range(len(stats)):
            if stats[i] and (stats[i] != cur_stats[i]):
                return False
        return True

    def __updateProfile(self):
        ''' Update Profile
        updates the hidden achievements in the player's profile
        accessed from checkAchievements
        '''
        pass
    
    def __initializeGameAchievements(self):
        ''' Initialize Game Achievements
        creates all gameplay achievements and adds them to gameplayAchievements field
        accessed from init only
        '''
        if not self.__initialized:
            self._gameplayAchievements.append(Achievement("Finished World 1", (None, None, 1, None, None)))
            self._gameplayAchievements.append(Achievement("Finished World 2", (None, None, 2, None, None)))
            self._gameplayAchievements.append(Achievement("Finished World 3", (None, None, 3, None, None)))

    def __initializeHiddenAchievements(self):
        ''' Initialize Hidden Achievements
        if profile has any hidden achievements, initializes hiddenAchievements field to the profile's, 
        otherwise creates all hidden achievements and adds them to hiddenAchievements field
        accessed from init only
        '''
        if not self.__initialized:
            self._gameplayAchievements.append(Achievement("Cheated Death", (None, 99, None, None, 0)))
            self._gameplayAchievements.append(Achievement("Enemy Dodger", (75, 0, None, None, None)))
            self._gameplayAchievements.append(Achievement("Straight A Fighter", (None, None, None, 6, None)))