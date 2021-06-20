from marshmallow import Schema, fields


class AlertSchema(Schema):
    team_id = fields.String(required=True)