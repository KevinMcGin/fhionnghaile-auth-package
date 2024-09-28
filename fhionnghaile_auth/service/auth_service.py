from functools import wraps
from flask import request
import requests 
import os


def token_required(authentication_required=False):
    def get_current_user(headers, authentication_required):
        AUTH_SERVICE_URL =  os.environ.get('AUTH_SERVICE_URL', 'http://localhost:8885')
        current_user_response = requests.post(
            AUTH_SERVICE_URL + "/api/auth", 
            headers=headers,
        )
        current_user = None
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