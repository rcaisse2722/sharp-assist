class BaseTeam:

    def __init__(self, teamid, nickname, conference, aliases):
        self.teamid = teamid
        self.aliases = aliases
        self.nickname = nickname
        self.conference = conference
        self.teamname = aliases[0]