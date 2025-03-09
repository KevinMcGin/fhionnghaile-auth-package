from functools import wraps
from flask import request
import requests 
import os
import time

# start: for sqlalchemy db refresh
import fhionnghaile_auth.repository.auth_user
import fhionnghaile_auth.repository.auth_user_role
import fhionnghaile_auth.repository.auth_role
import fhionnghaile_auth.repository.anonymous_user
# end: for sqlalchemy db refresh

def token_required(
    authentication_required=False,
    role_required=None,
):
    def get_current_user(headers, authentication_required):
        AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://localhost:8885')
        auth_uri = AUTH_SERVICE_URL + "/api/auth"
        print("auth uri is:", auth_uri)
        current_user_response = None
        try:
            auth_fail_status = 401
            status_code = 1000
            attempts = 0
            maxAttempts = 3
            sleepPerAttemptSeconds = 1
            while status_code > auth_fail_status and attempts < maxAttempts:
                attempts += 1
                current_user_response = requests.post(
                    auth_uri, 
                    headers={
                        "Authorization": headers.get("Authorization"),
                        "Anonymous-User-Id": headers.get("Anonymous-User-Id"),
                    },
                    timeout=30,
                )
                status_code = current_user_response.status_code
                if status_code > auth_fail_status:
                    print("Retrying authentication due to status code:", status_code)
                    time.sleep(sleepPerAttemptSeconds * attempts)
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
        if authentication_required and not "auth" in current_user:
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
            if "error" in current_user:
                print("Error: current_user has error:", current_user)
                return current_user, 401
            if role_required is not None and \
                "auth" in current_user and \
                role_required not in current_user.get("auth").get("roles"):
                print("Error: current_user has no role:", role_required, "for user:", current_user)
                return current_user, 403
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator