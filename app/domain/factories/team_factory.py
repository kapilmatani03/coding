from app.domain.aggregates.team_aggregate import TeamAggregate
from app.domain.entities.developer import Developer
from app.domain.entities.team import Team
import random

def rand_x_digit_num(x=10, leading_zeroes=False):
    """Return an X digit number, leading_zeroes returns a string, otherwise int"""
    if not leading_zeroes:
        # wrap with str() for uniform results
        return random.randint(10 ** (x - 1), 10 ** x - 1)
    else:
        return '{0:0{x}d}'.format(random.randint(0, 10 ** x - 1), x=x)


def generate_team_id():
    random_number = rand_x_digit_num(6)
    return 'team-{0}'.format(random_number)


def generate_developer_id():
    random_number = rand_x_digit_num(6)
    return 'dev-{0}'.format(random_number)


class TeamFactory(object):
    @staticmethod
    def create_new_team(team_data):
        team = Team(team_id=generate_team_id(), name=team_data.get('team').get('name'))
        developers = []
        for developer in team_data.get('developers'):
            developer_entity = Developer(developer_id=generate_developer_id(), phone_number=developer.get('phone_number'),
                      name=developer.get('name'))
            developers.append(developer_entity)
        return TeamAggregate(team=team, developers=developers)
