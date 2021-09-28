from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    email_verified = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String, default='https://picsum.photos/400/400')
    profile_cover_picture = db.Column(db.String, default='https://picsum.photos/1400/500')
    password = db.Column(db.String)
    role = db.Column(db.String, default='user')
    bio = db.Column(db.String, default='Hi welcome to my profile!')
    socials_facebook = db.Column(db.String)
    socials_linkedin = db.Column(db.String)
    socials_instagram = db.Column(db.String)
    socials_twitter = db.Column(db.String)
    blogposts = db.relationship('Blogpost', backref='author', lazy=True)
    editorials = db.relationship('Editorial', backref='author', lazy=True)
    


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
