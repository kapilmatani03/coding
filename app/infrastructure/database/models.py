from sqlalchemy.dialects.postgresql import JSON

from app.extensions import db


class TeamModel(db.Model):
    __tablename__ = 'teams'
    team_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)


class DeveloperModel(db.Model):
    __tablename__ = 'developers'
    developer_id = db.Column(db.String, primary_key=True)
    team = db.Column(db.String, db.ForeignKey('teams.team_id'), nullable=False)
    name = db.Column(db.String)
    phone_number = db.Column(db.String)
