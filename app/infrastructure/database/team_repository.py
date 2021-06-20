from app.domain.aggregates.team_aggregate import TeamAggregate
from app.infrastructure.database.base_entity_repository import BaseEntityRepository
from app.infrastructure.database.developer_adaptor import DeveloperAdaptor
from app.infrastructure.database.models import TeamModel, DeveloperModel
from app.infrastructure.database.team_adaptor import TeamAdaptor
from object_registry import register_instance


@register_instance()
class TeamRepository(BaseEntityRepository):
    team_adaptor = TeamAdaptor()
    developer_adaptor = DeveloperAdaptor()

    def save_team(self, team_aggreagte: TeamAggregate):
        team_model = self.team_adaptor.to_db_model(team_aggreagte.team)
        self._save(team_model)

    def save_developer(self, team_aggreagte: TeamAggregate):
        for developer in team_aggreagte.developers:
            developer_model = self.developer_adaptor.to_db_model(developer, team=team_aggreagte.team.team_id)
            self._save(developer_model)

    def get_team(self, team_id):
        query = self.query(TeamModel)
        query = query.filter(TeamModel.team_id==team_id)
        team_model = query.first()
        if team_model:
            developers = self.query(DeveloperModel).filter(DeveloperModel.team==team_id).all()
            developer_entities = [self.developer_adaptor.to_domain_entity(developer) for developer in developers]
        else:
            raise Exception

        return TeamAggregate(team=TeamAdaptor.to_domain_entity(team_model), developers=developer_entities)