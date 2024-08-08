from bson.objectid import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

client = MongoClient('mongodb://localhost:27017/')
db = client.vpn_db 

class User:
    def __init__(self, username, password_hash, id=None):
        self.username = username
        self.password_hash = password_hash
        self.id = id
        self._active = True

    def save(self):
        users = db.users
        users.insert_one({
            'username': self.username,
            'password_hash': self.password_hash
        })

    @staticmethod
    def find_by_username(username):
        users = db.users
        user_data = users.find_one({'username': username})
        if user_data:
            return User(user_data['username'], user_data['password_hash'])
        return None

    @staticmethod
    def create_user(username, password):
        hashed_password = generate_password_hash(password)
        user = User(username, hashed_password)
        user.save()
        return user

    def get_id(self):
        return self.id

    @staticmethod
    def find_by_id(user_id):
        users = db.users
        user_data = users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data['username'], user_data['password_hash'], user_data.get('_id'))
        return None

    @staticmethod
    def find_all():
        users = db.users
        user_list = []
        for user_data in users.find():
            user_list.append(User(user_data['username'], user_data['password_hash'], str(user_data.get('_id'))))
        return user_list

    @property
    def is_active(self):
        return self._active

    @property
    def is_authenticated(self):
        return True  # Kullanıcılar doğrulanmış olarak kabul edilir

    @property
    def is_anonymous(self):
        return False

class VPNConnection:
    def __init__(self, user_id, start_time, bytes_sent, bytes_received):
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = None
        self.bytes_sent = bytes_sent
        self.bytes_received = bytes_received

    def save(self):
        vpn_connections = db.vpn_connections
        vpn_connections.insert_one({
            'user_id': self.user_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'bytes_sent': self.bytes_sent,
            'bytes_received': self.bytes_received
        })

