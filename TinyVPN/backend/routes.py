from flask import Blueprint, jsonify, request, g
from models import User, VPNConnection
from openvpn.openvpn_manager import OpenVPNManager
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash
import jwt
import datetime

api_bp = Blueprint('api', __name__)
openvpn_manager = OpenVPNManager()

SECRET_KEY = '1234'

@api_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    # Kullanıcının zaten var olup olmadığını kontrol et
    if User.find_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400
    
    # Yeni kullanıcı oluştur ve veritabanına kaydet
    user = User.create_user(username, password)
    if user:
        return jsonify({'message': 'Registration successful'}), 201
    else:
        return jsonify({'error': 'Registration failed'}), 500

@api_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.find_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        login_user(user)

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'message': 'Login successful', 'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.find_all()
    return jsonify([user.username for user in users])

@api_bp.route('/vpn/connect', methods=['POST'])
@login_required
def connect_vpn():
    server_config = openvpn_manager.get_config()
    # Connect user to VPN using OpenVPN API
    connection = openvpn_manager.connect_user(current_user.id)
    # Save connection details to database
    vpn_connection = VPNConnection(user_id=current_user.id,
                                   start_time=connection.start_time,
                                   bytes_sent=connection.bytes_sent,
                                   bytes_received=connection.bytes_received)
    vpn_connection.save()
    return jsonify(connection.to_dict())