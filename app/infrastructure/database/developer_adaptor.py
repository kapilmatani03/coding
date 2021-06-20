from app.domain.entities.developer import Developer
from app.infrastructure.database.models import DeveloperModel


class DeveloperAdaptor(object):
    @staticmethod
    def to_db_model(developer: Developer, team):
        return DeveloperModel(team=team, name=developer.name, phone_number=developer.phone_number,
                              developer_id=developer.developer_id)

    @staticmethod
    def to_domain_entity(developer_model: DeveloperModel):
        return Developer(name=developer_model.name, phone_number=developer_model.phone_number,
                         developer_id=developer_model.developer_id)
