from app.domain.entities.team import Team
from app.infrastructure.database.models import TeamModel


class TeamAdaptor(object):
    @staticmethod
    def to_db_model(team: Team):
        return TeamModel(team_id=team.team_id, name=team.name)

    @staticmethod
    def to_domain_entity(team_model: TeamModel):
        return Team(team_id=team_model.team_id, name=team_model.name)
