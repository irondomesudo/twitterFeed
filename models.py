from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class Follower(db.Model):
    __tablename__ = 'followers'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure a user cannot follow the same person multiple times
    __table_args__ = (
        db.UniqueConstraint('follower_id', 'followed_id', name='unique_followers'),
    )

    def __repr__(self):
        return f'<Follower follower_id={self.follower_id} followed_id={self.followed_id}>'

class Tweet(db.Model):
    __tablename__ = 'tweets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet id={self.id} user_id={self.user_id} content={self.content[:20]}...>'

class Feed(db.Model):
    __tablename__ = 'feeds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Owner of the feed
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('feed_entries', lazy=True))
    tweet = db.relationship('Tweet', backref=db.backref('feed_entries', lazy=True))

    def __repr__(self):
        return f'<Feed user_id={self.user_id} tweet_id={self.tweet_id}>'
