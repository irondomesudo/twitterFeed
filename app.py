import os
from flask import Flask, request, jsonify
from models import db, User
from services import FollowingService

def create_app(database_uri=None):
    flask_app = Flask(__name__)
    
    # Configure Database
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri or os.environ.get(
        'DATABASE_URL', 
        'sqlite:///twitterfeed.db'
    )
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    return flask_app

app = create_app()

@app.route('/follow', methods=['POST'])
def follow():
    data = request.get_json()
    follower_id = data.get('follower_id')
    followed_id = data.get('followed_id')
    
    if not follower_id or not followed_id:
        return jsonify({'error': 'Missing follower_id or followed_id'}), 400
        
    try:
        FollowingService.follow(follower_id, followed_id)
        return jsonify({'message': f'User {follower_id} successfully followed User {followed_id}'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/unfollow', methods=['POST'])
def unfollow():
    data = request.get_json()
    follower_id = data.get('follower_id')
    followed_id = data.get('followed_id')
    
    if not follower_id or not followed_id:
        return jsonify({'error': 'Missing follower_id or followed_id'}), 400
        
    success = FollowingService.unfollow(follower_id, followed_id)
    if success:
        return jsonify({'message': f'User {follower_id} unfollowed User {followed_id}'}), 200
    return jsonify({'error': 'Follow relationship not found'}), 404

@app.route('/followers/<int:user_id>', methods=['GET'])
def get_followers(user_id):
    followers = FollowingService.get_followers(user_id)
    return jsonify({'followers': [{'id': u.id, 'username': u.username} for u in followers]}), 200

@app.route('/following/<int:user_id>', methods=['GET'])
def get_following(user_id):
    following = FollowingService.get_following(user_id)
    return jsonify({'following': [{'id': u.id, 'username': u.username} for u in following]}), 200

if __name__ == '__main__':
    app.run(debug=True)
