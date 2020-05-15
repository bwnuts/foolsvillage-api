from shapely import wkb

from models import Issue, Comment, IssueState, PollutionCategory, Role, User
from api.util import to_dict, Singleton


class IssueWrapper(metaclass=Singleton):
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
            issue_fields = [
                'id', 'title', 'description', 'state', 'date',
                'pollution_category', 'pollution_rating', 'budget'
            ]

            d = to_dict(comment, [i for i in fields if i in comment_fields])

            if 'datetime' in d:
                d['datetime'] = str(d['datetime'])
            if 'author' in fields:
                d['author'] = to_dict(comment.author, user_fields)
                d['author']['birthday'] = str(d['author']['birthday'])
                d['author']['role'] = d['author']['role'].role
            if 'origin' in fields:
                d['origin'] = to_dict(comment.issue, issue_fields)
                d['origin']['state'] = d['origin']['state'].state
                d['origin']['date'] = str(d['origin']['date'])
                d['origin']['pollution_category'] = d['origin']['pollution_category'].category
                d['origin']['comments'] = len(comment.issue.comments)
                if d['origin']['budget'] is not None:
                    d['origin']['budget'] = float(d['origin']['budget'])
                if 'location' in fields:
                    point = wkb.loads(bytes(comment.issue.location.data))
                    d['location'] = {'x': point.x, 'y': point.y}

            return d

        comments = session.query(Comment) \
                          .filter(Comment.issue_id == id) \
                          .order_by(Comment.datetime.desc()) \
                          .offset(offset) \
                          .limit(limit) \
                          .all()
        return [process(comment) for comment in comments]

    def info(self, id, fields):
        session = self.session_maker()

        issue_fields = [
            'id', 'title', 'description', 'date', 'pollution_rating', 'budget'
        ]
        user_fields = [
            'id', 'username', 'email', 'name', 'surname', 'gender',
            'phonenumber', 'avatar', 'birthday', 'role'
        ]

        issue = session.query(Issue) \
                       .filter(Issue.id == id) \
                       .one_or_none()
        if issue is None:
            return {}

        issue_dict = to_dict(issue, [i for i in fields if i in issue_fields])

        if 'budget' in issue_dict and issue_dict['budget'] is not None:
            issue_dict['budget'] = float(issue_dict['budget'])
        if 'comments' in fields:
            issue_dict['comments'] = session.query(Comment) \
                                            .filter(Issue.id == id) \
                                            .count()
        if 'state' in fields:
            issue_dict['state'] = issue.state.state
        if 'creator' in fields:
            issue_dict['creator'] = to_dict(issue.creator, user_fields)
            issue_dict['creator']['birthday'] = str(issue_dict['creator']['birthday'])
            issue_dict['creator']['role'] = issue_dict['creator']['role'].role
        if 'approver' in fields and issue.approver:
            issue_dict['approver'] = to_dict(issue.approver, user_fields)
            issue_dict['approver']['birthday'] = str(issue_dict['approver']['birthday'])
            issue_dict['approver']['role'] = issue_dict['approver']['role'].role
        if 'pollution_category' in fields:
            issue_dict['pollution_category'] = issue.pollution_category.category
        if 'location' in fields:
            point = wkb.loads(bytes(issue.location.data))
            issue_dict['location'] = {'x': point.x, 'y': point.y}
        if 'date' in fields:
            issue_dict['date'] = str(issue_dict['date'])

        return issue_dict

    def unapproved_issues(self):
        session = self.session_maker()


        issue_fields = [
            'id', 'title', 'description', 'location','date', 'pollution_rating', 'pollution_category', 'creator'
        ]

        unapproved_issue_id = session.query(IssueState) \
            .filter(IssueState.state=='new').one_or_none().id
        issues = session.query(Issue) \
                       .filter(Issue.state_id == unapproved_issue_id).all()
    
        issues_dict=[]
        for issue in issues:
            item = to_dict(issue, [i for i in issue_fields ])
            point = wkb.loads(bytes(issue.location.data))
            item['location'] = {'x': point.x, 'y': point.y}
            item['pollution_category'] = issue.pollution_category.category
            item['creator']=issue.creator.username
            issues_dict.append(item)

        if issues is None:
            return
        else:
            return issues_dict

    def create_issue(self,data):
        session = self.session_maker()

        try:
            pollution_category_id = session.query(PollutionCategory).filter(PollutionCategory.category == data.get('pollution_category')).one_or_none().id
            data['pollution_category']=pollution_category_id
            unapproved_issue_id = session.query(IssueState).filter(IssueState.state=='new').one_or_none().id
            data['state_id'] = unapproved_issue_id
            
            new_issue = Issue(data)
            session.add(new_issue)
            session.commit()

            issue_fields = [
            'id', 'title', 'description', 'location','date', 'pollution_rating', 'pollution_category', 'creator'
            ]
            result = to_dict(new_issue, [i for i in issue_fields ])
            point = wkb.loads(bytes(new_issue.location.data))
            result['location'] = {'x': point.x, 'y': point.y}
            result['pollution_category'] = new_issue.pollution_category.category
            result['creator']=new_issue.creator.username

            return (result,True)
        except Exception as e:
            return (e.args,False)

    def change_state(self,data):
        session = self.session_maker()

        try:
            approved_issue_id = session.query(IssueState).filter(IssueState.state=='approved').one_or_none().id
            rejected_issue_id = session.query(IssueState).filter(IssueState.state=='rejected').one_or_none().id

            issue = session.query(Issue).filter(Issue.id==data['id']).one_or_none()
            if data['response'] == 'approve':
                issue.state_id=approved_issue_id
                issue.approver_id=data['approver_id']
            elif data['response'] == 'reject':
                issue.state_id = rejected_issue_id
                
            session.commit()
            return True
        except Exception as e:
            return e.args
            

        
