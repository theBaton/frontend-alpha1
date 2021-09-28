from flask import jsonify, request, make_response, Blueprint, flash, redirect, render_template, url_for, render_template_string
from flask_jwt_extended.utils import decode_token
from ..models.UserModel import User
from ..models.BlogpostModel import Blogpost
from ..models.EditorialModel import Editorial
from ..models import db
from sqlalchemy import desc
import os
import uuid

from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from . import jwt
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, get_jwt, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .danger import superadmin_required, staff_required, generate_jwt_access_token

profile_api = Blueprint('profile_api', __name__)

@profile_api.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

@profile_api.context_processor
def handle_context():
    return dict(req_args = request.args, int = int, len = len, datetime=datetime, str = str)

@profile_api.route("/upload")
def upload():
    return render_template('upload_posts.html', title='Upload')

