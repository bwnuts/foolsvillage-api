from sqlalchemy import Column, Integer, String, \
                       ForeignKey, Numeric, Date, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geography

import datetime

__all__ = [
    'Base', 'Role', 'User', 'PollutionCategory', 'IssueState', 'Issue',
    'Event', 'Comment', 'Donation', 'TechnicalIssue', 'AdminRequests'
]

Base = declarative_base()

event_participant_table = Table(
    'event_participant', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('user_id', Integer, ForeignKey('users.id')))

class AdminRequest(Base):
    __tablename__ = 'admin_requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable = False)
    about = Column(String, nullable = False)
    additional_info = Column(String)
    
    state = Column(String, nullable = False)
    comment = Column(String)

    user = relationship('User', back_populates='admin_request')

class Role(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)

    users = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    email = Column(String, nullable=False)

    name = Column(String)
    surname = Column(String)
    gender = Column(Integer)
    birthday = Column(Date)
    phonenumber = Column(String)
    avatar = Column(String)

    password_hash = Column(String, nullable=False)
    password_salt = Column(String, nullable=False)

    admin_request = relationship('AdminRequest', back_populates='user')
    role = relationship('Role', back_populates='users')
    created_issues = relationship('Issue',
                                  back_populates='creator',
                                  foreign_keys='Issue.creator_id')
    approved_issues = relationship('Issue',
                                   back_populates='approver',
                                   foreign_keys='Issue.approver_id')
    created_events = relationship('Event',
                                  back_populates='creator',
                                  foreign_keys='Event.creator_id')
    events = relationship('Event',
                          secondary=event_participant_table,
                          back_populates='participants')
    comments = relationship('Comment',
                            back_populates='author',
                            foreign_keys='Comment.author_id')


class PollutionCategory(Base):
    __tablename__ = 'pollution_categories'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)

    issues = relationship('Issue', back_populates='pollution_category')


class IssueState(Base):
    __tablename__ = 'issue_states'

    id = Column(Integer, primary_key=True)
    state = Column(String, nullable=False)

    issues = relationship('Issue', back_populates='state')


class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    state_id = Column(Integer, ForeignKey('issue_states.id'), nullable=False)

    date = Column(Date, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    approver_id = Column(Integer, ForeignKey('users.id'))

    pollution_category_id = Column(Integer,
                                   ForeignKey('pollution_categories.id'),
                                   nullable=False)
    pollution_rating = Column(Integer, nullable=False)

    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    budget = Column(Numeric)

    state = relationship('IssueState', back_populates='issues')
    creator = relationship('User',
                           back_populates='created_issues',
                           foreign_keys='Issue.creator_id')
    approver = relationship('User',
                            back_populates='approved_issues',
                            foreign_keys='Issue.approver_id')
    pollution_category = relationship('PollutionCategory',
                                      back_populates='issues')
    events = relationship('Event',
                          back_populates='issue',
                          foreign_keys='Event.issue_id')
    comments = relationship('Comment', back_populates='issue')

    def __init__(self, data):
        self.title = data.get('title')
        self.description = data.get('description')
        self.state_id = data.get('state_id')
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.creator_id = data.get('creator_id')
        self.pollution_category_id = data.get('pollution_category')
        self.pollution_rating = data.get('pollution_rating')
        self.location = data.get('location')

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

    issue_id = Column(Integer, ForeignKey('issues.id'), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    datetime = Column(DateTime, nullable=False)

    issue = relationship('Issue', back_populates='events')
    creator = relationship('User', back_populates='events')
    comments = relationship('Comment', back_populates='event')
    participants = relationship('User',
                                secondary=event_participant_table,
                                back_populates='events')

    def __init__(self,data):
        self.title = data.get('title')
        self.description = data.get('description')
        self.issue_id = data.get('issue_id')
        self.creator_id = data.get('creator_id')
        self.datetime = data.get('datetime')



class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    rating = Column(Integer, nullable=False)

    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'))
    issue_id = Column(Integer, ForeignKey('issues.id'))

    author = relationship('User', back_populates='comments')
    event = relationship('Event', back_populates='comments')
    issue = relationship('Issue', back_populates='comments')


class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True)

    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    city = Column(String)
    date = Column(Date, nullable=False)

    amount = Column(Numeric, nullable=False)


class TechnicalIssue(Base):
    __tablename__ = 'tech_issues'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    text = Column(String, nullable=False)
    media = Column(String)
