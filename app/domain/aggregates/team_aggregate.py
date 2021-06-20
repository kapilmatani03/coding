from app.domain.entities.developer import Developer
from app.domain.entities.team import Team


class TeamAggregate(object):

    def __init__(self, team: Team, developers: [Developer]):
        self.team = team
        self.developers = developers