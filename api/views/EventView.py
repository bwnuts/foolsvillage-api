from flask import request, json, Response, Blueprint
from models import Event
from ..events import EventWrapper

def custom_response(result,status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(result),
        status=status_code
    )

event_api = Blueprint('event',__name__)

@event_api.route('/', methods=['POST'])
def create_event():
    request_data = request.get_json()

    result = EventWrapper().create_event(request_data)

    if result[1] is True:
        return custom_response(result[0],200)
    else:
        return custom_response({'Error': result[0]},400)

@event_api.route('/change_datetime', methods=['PUT'])
def change_datetime():
    request_data = request.get_json()

    result = EventWrapper().change_datetime(request_data)

    if result is True:
        return custom_response({'Success': 'Datetime has been updated'},200)
    else:
        return custom_response({'Error': result},400)