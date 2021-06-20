from app.infrastructure.database.base_repository import BaseRepository


class BaseEntityRepository(BaseRepository):
    adaptor = None

    def save(self, entity):
        model = self.adaptor.to_db_model(entity)
        self._save(model)

    def update(self, entity):
        model = self.adaptor.to_db_model(entity)
        self._update(model)
