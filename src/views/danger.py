from . import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt, create_access_token
from flask import jsonify
from functools import wraps

def superadmin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "superadmin" in claims['roles']:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


def staff_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "staff" in claims['roles']:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Staff only!"), 403

        return decorator

    return wrapper


def generate_jwt_access_token(user): 
    roles_list = user.role.split("+")

    additional_claims = {
        "name" : user.name,
        "bio" : user.bio,
        "email" : user.email,
        "email_verified" : user.email_verified,
        "profile_picture" : user.profile_picture,
        "profile_cover_picture" : user.profile_cover_picture,
        "public_id" : user.public_id,
        "roles" : roles_list,
        "socials": {"facebook" : user.socials_facebook, "instagram" : user.socials_instagram, "linkedin" : user.socials_linkedin, "twitter" : user.socials_twitter}

    }

    access_token = create_access_token(identity=user.public_id, additional_claims=additional_claims)

    return access_token