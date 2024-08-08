from flask import Blueprint, jsonify, request, g
from models import User, VPNConnection
from openvpn.openvpn_manager import OpenVPNManager
from flask_login import login_required, current_user

api_bp = Blueprint('api', __name__)
openvpn_manager = OpenVPNManager()

@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.objects.all()
    return jsonify([user.username for user in users])

@api_bp.route('/vpn/connect', methods=['POST'])
@login_required
def connect_vpn():
    server_config = openvpn_manager.get_config()
    # Connect user to VPN using OpenVPN API
    connection = openvpn_manager.connect_user(current_user.id)
    # Save connection details to database
    vpn_connection = VPNConnection(user=current_user, 
                                   start_time=connection.start_time, 
                                   bytes_sent=connection.bytes_sent, 
                                   bytes_received=connection.bytes_received)
    vpn_connection.save()
    return jsonify(connection.to_dict())

# Add more API endpoints as needed