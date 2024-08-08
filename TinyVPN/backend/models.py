from flask_mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)

class VPNConnection(db.Document):
    user = db.ReferenceField(User, required=True)
    start_time = db.DateTimeField(required=True)
    end_time = db.DateTimeField()
    bytes_sent = db.LongField(required=True)
    bytes_received = db.LongField(required=True)