from marshmallow import Schema, fields


class TeamSchema(Schema):
    name = fields.String(required=True)


class DeveloperSchema(Schema):
    name = fields.String(required=True)
    phone_number = fields.String(required=True)


class CreateTeamSchema(Schema):
    team = fields.Nested(TeamSchema)
    developers = fields.Nested(DeveloperSchema, many=True)
