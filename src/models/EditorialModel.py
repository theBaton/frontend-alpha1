from datetime import datetime
from . import db

class Editorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True, nullable=False)
    cover_image = db.Column(db.String, default='https://picsum.photos/1400/900')
    title = db.Column(db.String)
    sub_title = db.Column(db.String)
    cta_title = db.Column(db.String, default= "Potatorem ipsum dolor sit amet consectetur adipisicing elit. Possimus ratione quo.")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    keywords = db.Column(db.String)
    toc = db.Column(db.String)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key is user.id in main
    

    def __repr__(self):
        return f"Editorial('{self.title}', '{self.date_posted}')"