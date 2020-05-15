from models import Event, Comment
from api.util import to_dict, Singleton

import datetime

class EventWrapper(metaclass=Singleton):
    def __init__(self, session_maker):
        self.session_maker = session_maker

    def comments(self, id, fields, offset=0, limit=25):
        session = self.session_maker()

        comment_fields = ['id', 'text', 'datetime', 'rating']

        def process(comment):
            user_fields = [
                'id', 'username', 'email', 'name', 'surname', 'gender',
                'phonenumber', 'avatar', 'birthday', 'role'
            ]
            event_fields = ['id', 'datetime', 'comments', 'participants']
            d = to_dict(comment, [i for i in fields if i in comment_fields])

            if 'datetime' in d:
                d['datetime'] = str(d['datetime'])
            if 'author' in fields:
                d['author'] = to_dict(comment.author, user_fields)
                d['author']['birthday'] = str(d['author']['birthday'])
                d['author']['role'] = d['author']['role'].role
            if 'origin' in fields:
                d['origin'] = to_dict(comment.event, event_fields)
                d['origin']['datetime'] = str(d['origin']['datetime'])
                d['origin']['comments'] = len(d['origin']['comments'])
                d['origin']['participants'] = len(d['origin']['participants'])

            return d

        comments = session.query(Comment) \
                          .filter(Comment.event_id == id) \
                          .order_by(Comment.datetime.desc()) \
                          .offset(offset) \
                          .limit(limit) \
                          .all()
        return [process(comment) for comment in comments]

    def info(self, id, fields):
        session = self.session_maker()
        event_fields = ['id', 'datetime']
        issue_fields = [
            'id', 'title', 'description', 'state', 'date',
            'pollution_category', 'pollution_rating', 'budget', 'comments'
        ]
        user_fields = [
            'id', 'username', 'email', 'name', 'surname', 'gender',
            'phonenumber', 'avatar', 'birthday', 'role'
        ]

        event = session.query(Event) \
                       .filter(Event.id == id) \
                       .one_or_none()
        if event is None:
            return {}

        event_dict = to_dict(event, [i for i in fields if i in event_fields])

        if 'datetime' in event_dict:
            event_dict['datetime'] = str(event_dict['datetime'])
        if 'comments' in fields:
            event_dict['comments'] = len(event.comments)
        if 'participants' in fields:
            event_dict['participants'] = len(event.participants)
        if 'issue' in fields:
            event_dict['issue'] = to_dict(event.issue, issue_fields)
            event_dict['issue']['state'] = event_dict['issue']['state'].state
            event_dict['issue']['date'] = str(event_dict['issue']['date'])
            event_dict['issue']['pollution_category'] = event_dict['issue']['pollution_category'].category
            event_dict['issue']['comments'] = len(event_dict['issue']['comments'])
            if event_dict['issue']['budget'] is not None:
                event_dict['issue']['budget'] = float(event_dict['issue']['budget'])
        if 'creator' in fields:
            event_dict['creator'] = to_dict(event.creator, user_fields)
            event_dict['creator']['birthday'] = str(event_dict['creator']['birthday'])
            event_dict['creator']['role'] = event_dict['creator']['role'].role

        return event_dict

    def create_event(self,data):
        session = self.session_maker()
        
        try:
            if datetime.datetime.strptime(data['datetime'],"%Y-%m-%d %H:%M") < datetime.datetime.now():
                return 'Invalid date'
                
            new_event = Event(data)
            session.add(new_event)
            session.commit()
            
            event_fields = ['id','title','description','issue_id','creator_id','datetime']

            result = to_dict(new_event, [i for i in event_fields])

            return (result,True)
        except Exception as e:
            return (e.args,False)

    def change_datetime(self,data):
        session = self.session_maker()

        try:
            event = session.query(Event).filter(Event.id==data['id']).one_or_none()
            
            if datetime.datetime.strptime(data['datetime'],"%Y-%m-%d %H:%M") < datetime.datetime.now():
                return 'Invalid date'

            event.datetime = data['datetime']
            session.commit()
            return True
        except Exception as e:
            return e.args
