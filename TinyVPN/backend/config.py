import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    MONGODB_SETTINGS = {
        'db': 'vpn_db',
        'host': 'mongodb://localhost:27017/vpn_db'
    }