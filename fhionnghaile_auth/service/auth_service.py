from functools import wraps
from flask import request
import requests 
import os


def token_required(authentication_required=False):
    def get_current_user(headers, authentication_required):
        AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://localhost:8885')
        auth_uri = AUTH_SERVICE_URL + "/api/auth"
        print("auth uri is:", auth_uri)
        current_user_response = None
        try:
            current_user_response = requests.post(
                auth_uri, 
                # headers=headers,
                timeout=30,
            )
        except Exception as e:
            print("Error occurred while authenticating user:", e)
            return {
                "message": "Authentication failed",
                "data": None,
                "error": "Unauthorized"
            }
        current_user = None
        print("current_user_response is:", current_user_response)
        print("response is:", current_user_response.text)
        if current_user_response.status_code == 200:
            current_user = current_user_response.json()
        else:
            return {
                "message": "Authentication failed",
                "data": None,
                "error": "Unauthorized"
            } 
        print("current_user is this:", current_user)
        if authentication_required and not current_user["auth"]:
            return {
                "message": "Authentication Token failed!",
                "data": None,
                "error": "Unauthorized"
            }
        return current_user
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            current_user=get_current_user(request.headers, authentication_required)
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator