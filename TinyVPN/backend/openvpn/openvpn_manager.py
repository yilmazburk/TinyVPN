import openvpn_api
from datetime import datetime

class OpenVPNManager:
    def __init__(self):
        self.client = openvpn_api.OpenVPNClient()
        self.client.read_config('openvpn/config.ovpn')

    def get_config(self):
        return self.client.config

    def connect_user(self, user_id):
        connection = self.client.connect()
        # Add additional logic to handle user authentication and authorization
        return connection

    def disconnect_user(self, user_id):
        self.client.disconnect()
        # Add additional logic to handle user disconnection