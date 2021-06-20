# coding
Teams and Developers App
Create Teams API:
POST http://127.0.0.1:5000/v1/teams
{
    "data":{
        "team": {
            "name": "kapil"
        },
        "developers": [
            {
                "name": "dev1",
                "phone_number": "9462317503"
            },
            {
                "name": "sdfg",
                "phone_number": "1234567890"
            }
        ]
    }
}

Send Alerts:
POST http://127.0.0.1:5000/v1/alert

{
    "data":{
        "team_id": "team497991"
    }
}
