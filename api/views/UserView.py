from flask import request, json, Response, Blueprint
from models import User, Role
from ..users import UserWrapper

def custom_response(result,status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(result),
        status=status_code
    )

user_api = Blueprint('user',__name__)

@user_api.route('/edit_avatar', methods=["PUT"])
def edit_avatar():
    request_data = request.get_json()
    
    result = UserWrapper().edit_avatar(request_data['user_id'],request_data['new_avatar'])
    
    if result is None:
        return custom_response({'Success':'Avatar has been updated'},200)
    else:
        return custom_response({'Error': result},400)

@user_api.route('/edit_profile', methods=["PUT"])
def edit_profile():
    request_data = request.get_json()

    result = UserWrapper().edit_profile(request_data)
    
    if result is None:
        return custom_response({'Success':'Profile has been updated'},200)
    else:
        return custom_response({'Error': result},400)

@user_api.route('/admin_requests', methods=["GET"])
def admin_requests():
    result = UserWrapper().admin_requests()

    return custom_response(result,200)

@user_api.route('/admin_request', methods=["PUT"])
def admin_request_response():
    request_data = request.get_json()

    result = UserWrapper().admin_request_response(request_data)

    if result is None:
        return custom_response({'Success':'Role has been updated'},200)
    else:
        return custom_response({'Error': result},400)
        