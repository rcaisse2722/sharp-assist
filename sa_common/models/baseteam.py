class BaseTeam:

    def __init__(self, teamid, nickname, conference, aliases):
        self.teamid = teamid
        self.aliases = aliases
        self.nickname = nickname
        self.conference = conference
        self.teamname = aliases[0]

    def __str__(self):
        return str(self.teamname)

    def __repr__(self):
        return self.__str__()