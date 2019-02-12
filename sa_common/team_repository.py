import abc
import csv
from sa_common.models.baseteam import BaseTeam

# Base interface
class ITeamRepository(abc.ABC):

    @abc.abstractmethod
    def __init__(self, connection_string):
        pass

    @abc.abstractmethod
    def get_team(self, team_name):
        pass


# File implementation of ITeamProvider (CSV file)
class FileTeamRepository(ITeamRepository):

    team_map = {}

    def __init__(self, connection_string):
        with open(connection_string, 'r', errors="surrogateescape") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if(len(row) < 4):
                    print(f"Invalid row in team DB: {row}")
                    continue
                elif "#" in row[0]: # Comment row
                    continue
                teamid = int(row[0])
                conference = row[1]
                nickname = row[2]
                aliases = row[3:len(row)]
                self.team_map[teamid] = BaseTeam(teamid, nickname, conference, aliases)


    def get_team(self, team_name):
        team = None
        for value in self.team_map.values():
            matches = [s for s in value.aliases if team_name.lower() == s.lower()]
            if(len(matches) > 0):
                team = value
                break

        return team
        