from flask import request, json, Response, Blueprint
from models import Issue, IssueState
from ..issues import IssueWrapper

def custom_response(result,status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(result),
        status=status_code
    )

issue_api = Blueprint('issue',__name__)

@issue_api.route('/unapproved_issues', methods=['GET'])
def unapproved_issues():
    issues = IssueWrapper().unapproved_issues()

    if issues is not None:
        return custom_response(issues,200)
    else:
        return custom_response({'Error': 'Bad request'},400)

@issue_api.route('/', methods=['POST'])
def create_issue():
    request_data = request.get_json()

    result = IssueWrapper().create_issue(request_data)

    if result[1] is True:
        return custom_response(result[0],200)
    else:
        return custom_response({'Error': result[0]},400)

@issue_api.route('/change_state', methods=['PUT'])
def change_state():
    request_data = request.get_json()

    result = IssueWrapper().change_state(request_data)

    if result is True:
        return custom_response({'Success':'State has been updated'},200)
    else:
       return custom_response({'Error': result},400)
