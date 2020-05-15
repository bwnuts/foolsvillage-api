from models import User, Role, AdminRequest
from api.util import to_dict, Singleton

class UserWrapper(metaclass=Singleton):
    def __init__(self,session_maker):
        self.session_maker= session_maker

    def admin_request_response(self,data):
        session = self.session_maker()

        try:
            admin_request = session.query(AdminRequest).filter(AdminRequest.id==data['admin_request_id']).one_or_none()
            if admin_request.state != 'opened':
                return "The request is not opened"

            user = session.query(User).filter(User.id==admin_request.user_id).one_or_none()
            admin_role_id = session.query(Role).filter(Role.role=='admin').one_or_none().id

            if data['response'] == 'approve':
                user.role_id = admin_role_id
                admin_request.state = 'approved'
            elif data['response'] == 'reject':
                admin_request.state = 'rejected'
                admin_request.comment = data['comment']
            
            session.commit()
            return
        except Exception as e:
            return e.args


    def edit_avatar(self,user_id,new_avatar):
        session = self.session_maker()

        try:
            session.query(User).get(user_id).avatar = new_avatar
            session.commit()
            return
        except Exception as e:
            return e.args

    def edit_profile(self,data):
        session = self.session_maker()

        try:
            user = session.query(User).get(data['user_id'])
            user.name = data['name']
            user.surname = data['surname']
            user.username = data['username']
            user.phone = data['phone']
            user.birthday = data['birthday']
            user.gender = data['gender']
            session.commit()
            return
        except Exception as e:
            return e.args
    
    def admin_requests(self):
        session = self.session_maker()

        admin_requests_fields = [
            'id', 'message', 'about', 'additional_info'
            ]

        admin_requests = session.query(AdminRequest).filter(AdminRequest.state=='opened').all()
        admin_requests_dict=[]
        for admin_request in admin_requests:
            item = to_dict(admin_request, [i for i in admin_requests_fields])
            user = session.query(User).filter(User.id==admin_request.user_id).one_or_none()
            item['name'] = user.name
            item['email'] = user.email
            admin_requests_dict.append(item)
        if admin_requests is None:
            return
        else:
            return admin_requests_dict




