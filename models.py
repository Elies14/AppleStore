from app import db
import datetime


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.BigInteger)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)
    number_of_rating = db.Column(db.Integer)
    seller = db.Column(db.String)
    size = db.Column(db.String)
    category = db.Column(db.String)
    is_kids_friendly = db.Column(db.Boolean, default=False)
    min_age = db.Column(db.Integer)
    min_iphone_version = db.Column(db.Float)
    min_ipad_version = db.Column(db.Float)
    min_mac_version = db.Column(db.Float)
    is_tv_app = db.Column(db.Boolean, default=False)
    is_photo_app = db.Column(db.Boolean, default=False)
    is_music_app = db.Column(db.Boolean, default=False)
    is_game_app = db.Column(db.Boolean, default=False)
    other = db.Column(db.String)
    weekly_sub = db.Column(db.Float)
    monthly_sub = db.Column(db.Float)
    yearly_sub = db.Column(db.Float)
    languages = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

