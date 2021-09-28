from datetime import datetime
from . import db

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True, nullable=False)
    cover_image = db.Column(db.String, default='static/images/default_cover.jpg')
    title = db.Column(db.String, nullable=False)
    sub_title = db.Column(db.String)
    cta_title = db.Column(db.String, default= "Lorem ipsum dolor sit amet consectetur adipisicing elit. Possimus ratione quo.")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    keywords = db.Column(db.String)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Blogpost('{self.title}', '{self.date_posted}')"