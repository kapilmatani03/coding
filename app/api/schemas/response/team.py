from marshmallow import Schema, fields


class TeamSchema(Schema):
    name = fields.String()
    team_id = fields.String()


class DeveloperSchema(Schema):
    name = fields.String()
    phone_number = fields.String()
    developer_id = fields.String()


class TeamResponseSchema(Schema):
    team = fields.Nested(TeamSchema)
    developers = fields.Nested(DeveloperSchema, many=True)
