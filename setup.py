import json
import os

from flask import Flask, request
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from models import Base
from api.issues import IssueWrapper
from api.events import EventWrapper
from api.users import UserWrapper

from api.views.UserView import user_api as user_blueprint
from api.views.IssueView import issue_api as issue_blueprint
from api.views.EventView import event_api as event_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix='/api/user/')
app.register_blueprint(issue_blueprint,url_prefix='/api/issue/')
app.register_blueprint(event_blueprint,url_prefix='/api/event/')

@app.route('/api/event/<int:id>', methods=['GET'])
def event_info(id):
    valid_fields = [
        'id', 'issue', 'creator', 'datetime', 'comments', 'participants'
    ]

    fields = request.args.get('fields', None)
    if fields:
        fields = [i for i in fields.split(',') if i in valid_fields]
    else:
        fields = valid_fields

    event = EventWrapper().info(id, fields)
    response = json.dumps(event)

    return response


@app.route('/api/event/<int:id>/comments', methods=['GET'])
def event_get_comments(id):
    valid_fields = ['id', 'text', 'datetime', 'author', 'origin', 'rating']

    offset = int(request.args.get('offset', 0))
    offset = max(offset, 0)
    limit = int(request.args.get('limit', 25))
    limit = min(25, limit)

    fields = request.args.get('fields', None)
    if fields:
        fields = [i for i in fields.split(',') if i in valid_fields]
    else:
        fields = valid_fields

    comments = EventWrapper().comments(id, fields, offset, limit)

    response = json.dumps(comments)
    return response


@app.route('/api/issue/<int:id>', methods=['GET'])
def issue_info(id):
    valid_fields = [
        'id', 'title', 'description', 'state', 'date', 'creator',
        'approver', 'pollution_category', 'pollution_rating', 'budget',
        'comments', 'location'
    ]

    fields = request.args.get('fields', None)
    if fields:
        fields = [i for i in fields.split(',') if i in valid_fields]
    else:
        fields = valid_fields

    issue = IssueWrapper().info(id, fields)
    response = json.dumps(issue)

    return response


@app.route('/api/issue/<int:id>/comments', methods=['GET'])
def issue_get_comments(id):
    valid_fields = ['id', 'text', 'datetime', 'author', 'origin', 'rating']

    offset = int(request.args.get('offset', 0))
    offset = max(offset, 0)
    limit = int(request.args.get('limit', 25))
    limit = min(25, limit)

    fields = request.args.get('fields', None)
    if fields:
        fields = [i for i in fields.split(',') if i in valid_fields]
    else:
        fields = valid_fields

    comments = IssueWrapper().comments(id, fields, offset, limit)

    response = json.dumps(comments)
    return response

class Development(object):
    DEBUG=True

if __name__ == '__main__':
    connstring = os.environ('DATABASE_URL')
    if connstring is None:
        print('Setup the DATABASE_URL variable')
        exit(1)

    db = sa.create_engine(connstring, echo=True)
    Session = sessionmaker(bind=db)
    Base.metadata.create_all(db)

    IssueWrapper(Session)
    EventWrapper(Session)
    UserWrapper(Session)
    
    app.config.from_object(Development)

    app.run()
