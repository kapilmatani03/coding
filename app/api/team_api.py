from flask import Blueprint

from app.api import ApiResponse
from app.api.request_parsers import schema_wrapper_parser, RequestTypes
from app.api.schemas import AlertSchema
from app.api.schemas.request.team import CreateTeamSchema
from app.api.schemas.response.team import TeamResponseSchema
from app.application.team_service import TeamService
from object_registry import inject

team_bp = Blueprint('Teams', __name__, url_prefix="/v1")


@team_bp.route('/teams', methods=['POST'])
@schema_wrapper_parser(CreateTeamSchema, param_type=RequestTypes.JSON)
@inject(team_service=TeamService)
def create_team(team_service: TeamService, parsed_request):

    team_aggregate = team_service.create_new_team(parsed_request)
    response = TeamResponseSchema().dump(team_aggregate)
    return ApiResponse.build(status_code=200, data=response.data)


@team_bp.route('/alert', methods=['POST'])
@schema_wrapper_parser(AlertSchema, param_type=RequestTypes.JSON)
@inject(team_service=TeamService)
def send_alert(team_service: TeamService, parsed_request):

    team_service.alert_team(parsed_request.get('team_id'))
    return ApiResponse.build(status_code=200, data="Successfully notified")