import com.fhionnghaile.auth.repository.auth_user as auth_user_repo

def save_auth_user(auth_user):
    return to_response(
        auth_user_repo.save_auth_user(
            auth_user_repo.AuthUser(
                auth_user['authUserId'],
                auth_user['email'],
                auth_user['userName']
            )
        )
    )

def get_auth_user_by_user_id(auth_user_id):
    return to_response(
        auth_user_repo.get_auth_user_by_auth_user_id(
            auth_user_id
        )
    )

def get_auth_user_by_name(user_name):
    return to_response(
        auth_user_repo.get_auth_user_by_name(user_name)
    )

def get_auth_user_by_email(email):
    return to_response(
        auth_user_repo.get_auth_user_by_email(email)
    )

def get_all_auth_users():
    users = auth_user_repo.get_all_auth_users()
    return [to_response(user) for user in users]

def update_auth_user(email, user):
    user = auth_user_repo.update_auth_user(
        email, 
        to_auth_user_database(user),
    )
    return to_response(user)

def delete_auth_user(auth_user_id):
    user = auth_user_repo.delete_auth_user(auth_user_id)
    return to_response(user)

def to_response(user):
    if user is None:
        return None
    return {
        "authUserId": user.auth_user_id,
        "email": user.email,
        "userName": user.user_name,
        "createdOn": user.created_on,
        "lastLogin": user.last_login
    }

def to_auth_user_database(auth_user):
    return auth_user_repo.AuthUser(
        auth_user['authUserId'],
        auth_user['email'],
        auth_user['userName'],
        auth_user['createdOn'],
        auth_user['lastLogin']
    )
