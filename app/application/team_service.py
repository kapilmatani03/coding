from app.application.decorators.transaction import session_manager
from app.domain.factories.team_factory import TeamFactory
from app.infrastructure.database.team_repository import TeamRepository
from app.infrastructure.external_clients.notification_client import NotificationClient
from object_registry import register_instance
import random


@register_instance(dependencies=[TeamRepository, NotificationClient])
class TeamService(object):
    def __init__(self, team_repository: TeamRepository, notification_client: NotificationClient):
        self.team_repository = team_repository
        self.notification_client = notification_client

    @session_manager(commit=True)
    def save_team(self, team_aggregate):
        self.team_repository.save_team(team_aggregate)

    @session_manager(commit=True)
    def save_developer(self, team_aggregate):
        self.team_repository.save_developer(team_aggregate)

    def create_new_team(self, team_data):
        team_aggregate = TeamFactory.create_new_team(team_data)
        self.save_team(team_aggregate)
        self.save_developer(team_aggregate)
        return team_aggregate

    def alert_team(self, team_id):
        team_aggreagte = self.team_repository.get_team(team_id)

        developers = team_aggreagte.developers
        if developers:
            developer_id = random.randint(0, len(developers)-1)
            phone_number = developers[developer_id].phone_number
            self.notification_client.send_notification(phone_number=phone_number)
