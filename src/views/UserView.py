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

user_api = Blueprint('user_api', __name__)

@user_api.after_request
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

@user_api.context_processor
def handle_context():
    return dict(req_args = request.args, int = int, len = len, datetime=datetime, str = str)

@user_api.route("/")
@user_api.route("/index")
def index():
    featured_editorials = Editorial.query.order_by(desc('date_modified')).limit(4)
    recent_blogs = Blogpost.query.order_by(desc('date_modified')).limit(6)
    return render_template('index.html', recent_blogs = recent_blogs, featured_editorials = featured_editorials)


@user_api.route("/about")
def about():
    return render_template('about.html', title='About')


@user_api.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        user = User(
            public_id = str(uuid.uuid4()),
            name = form.name.data,
            email = form.email.data, 
            password = hashed_password,
            role='user+staff+superadmin'
            )

        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created!', 'success')
        return redirect(url_for('user_api.index'))
    return render_template('register.html', form=form)


@user_api.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):

                response = make_response(redirect(url_for('user_api.index')))
                access_token = generate_jwt_access_token(user)
                set_access_cookies(response, access_token)
                flash('You have been logged in!', 'success')
                
                return response

            flash('Login Unsuccessful. Please check your password', 'danger')

        flash('User does not exist. Please register.', 'danger')

    return render_template('login.html', form=form)


@user_api.route("/logout", methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('user_api.index')))
    unset_jwt_cookies(response)
    flash('You have been logged out!', 'success')
    return response

@user_api.route("/forgot-password", methods=['GET', 'POST'])
def forgot_password():

    return redirect(url_for('user_api.index'))

@user_api.route("/change-password", methods=['GET', 'POST'])
def change_password():

    ##---##

    response = make_response(redirect(url_for('user_api.index')))
    unset_jwt_cookies(response)
    flash('Password changed successfully, please login again!', 'success')
    return response

@user_api.route('/blogs', methods=['GET'])
def blogs():
    blogs_all = Blogpost.query.order_by(desc('date_modified'))
    total_blogs = Blogpost.query.count()
    page_id = request.args.get('page')
    if not page_id:
        page_id = 1
    try:
        page_id = int(page_id)
        blogs = [blogs_all[i] for i in range(9*(page_id - 1), 9*page_id)]
    except ValueError:
        blogs = [blogs_all[i] for i in range(0, 9)]

    except IndexError:
        blogs = [blogs_all[i] for i in range(9*(page_id - 1), total_blogs)]

    return render_template('blogs.html', blogs=blogs)

@user_api.route('/blogs/<public_id>', methods=['GET'])
def blog_post(public_id):

    blogpost = Blogpost.query.filter_by(public_id=public_id).first()

    return render_template_string(source = blogpost.content, blog_post=blogpost)

@user_api.route('/editorials', methods=['GET'])
def editorials():
    editorials_all = Editorial.query.order_by(desc('date_modified'))
    total_editorials = Editorial.query.count()
    page_id = request.args.get('page')
    if not page_id:
        page_id = 1
    #try:
    page_id = int(page_id)
    editorials = [editorials_all[i] for i in range(9*(page_id - 1), total_editorials)]
    #editorials = [editorials_all[i] for i in range(9*(page_id - 1), 9*page_id)]
    #except ValueError:
    #    editorials = [editorials_all[i] for i in range(0, 9)]

    #except IndexError:
    #    editorials = [editorials_all[i] for i in range(9*(page_id - 1), total_editorials)]

    return render_template('editorials.html', editorial_post=editorials)

@user_api.route('/editorials/<public_id>', methods=['GET'])
def editorial_post(public_id):

    editorial_post = Editorial.query.filter_by(public_id=public_id).first()
    toc_string = editorial_post.toc
    toc_list = toc_string.split(',')
    toc = [sections.split('--') for sections in toc_list]
    toc_string_lower = toc_string.lower()
    toc_string_lower_updated = toc_string_lower.replace('--', ',')
    toc_string_lower_updated1 = toc_string_lower_updated.replace(' ', '-')
    toc_id_list = toc_string_lower_updated1.split(',')

    return render_template_string(source = editorial_post.content, editorial_post=editorial_post, toc = toc, toc_id = toc_id_list)

@user_api.route('/podcasts', methods=['GET'])
def podcasts():
    return render_template('podcasts.html')

@user_api.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@user_api.route('/profile-edit', methods=['GET', 'POST', 'PUT'])
@jwt_required()
def profile_edit():
    form = ProfileEditForm()
    claims = get_jwt()

    if form.validate_on_submit():
        user = User.query.filter_by(public_id=claims['public_id']).first()
        user.name = form.name.data
        user.bio = form.bio.data
        user.linkedin = form.linkedin.data
        user.facebook = form.facebook.data
        user.twitter = form.twitter.data
        user.instagram = form.instagram.data
        
        if form.email.data != user.email:
            user.email = form.email.data
            user.email_verified = False
        
        db.session.commit()

        user = User.query.filter_by(public_id=claims['public_id']).first()
        
        access_token = generate_jwt_access_token(user)
        
        response = make_response(redirect(url_for('user_api.index')))
        set_access_cookies(response, access_token)
        flash('Profile updated successfully', 'success')
        return response


    return render_template('editprofile.html', profile=claims)

@user_api.route('/user/<name>', methods=['GET'])
def profile(name):
    name_with_spaces = name.replace("-", " ")
    profile = User.query.filter_by(name=name_with_spaces)
    return render_template('profile.html', profile = profile)

