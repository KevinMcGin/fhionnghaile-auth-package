import fhionnghaile_auth.repository.anonymous_user as anonymous_user_repo

def save_anonymous_user(anonymous_user):
    return to_response(
        anonymous_user_repo.save_anonymous_user(
            anonymous_user_repo.AnonymousUser(
                anonymous_user['anonymousUserId'],
                anonymous_user['userName']
            )
        )
    )

def get_anonymous_user_by_uuid(anonymous_user_id):
    return to_response(
        anonymous_user_repo.get_anonymous_user_by_anonymous_user_id(
            anonymous_user_id
        )
    )

def get_anonymous_user_by_name(user_name):
    return to_response(
        anonymous_user_repo.get_anonymous_user_by_name(user_name)
    )

def get_all_anonymous_users():
    users = anonymous_user_repo.get_all_anonymous_users()
    return [to_response(user) for user in users]

def update_anonymous_user(anonymous_user_id, user):
    user = anonymous_user_repo.update_anonymous_user(
        anonymous_user_id, 
        to_anonymous_user_database(user)
    )
    return to_response(user)

def delete_anonymous_user(anonymous_user_id):
    user = anonymous_user_repo.delete_anonymous_user(anonymous_user_id)
    return to_response(user)

def to_response(user):
    if user is None:
        return None
    return {
        "anonymousUserId": user.anonymous_user_id,
        "userName": user.user_name,
        "createdOn": user.created_on,
        "lastLogin": user.last_login
    }

def to_anonymous_user_database(anonymous_user):
    return anonymous_user_repo.AnonymousUser(
        anonymous_user['anonymousUserId'],
        anonymous_user['userName'],
        anonymous_user['createdOn'],
        anonymous_user['lastLogin']
    )
