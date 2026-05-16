from app import create_app
from models import db, User, Follower
from services import FollowingService

def run_tests():
    app = create_app('sqlite:///:memory:') # Use in-memory DB for tests
    
    with app.app_context():
        # Create users
        user1 = User(username='alice', email='alice@example.com')
        user2 = User(username='bob', email='bob@example.com')
        user3 = User(username='charlie', email='charlie@example.com')
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        
        print("Users created.")
        
        # Test follow
        FollowingService.follow(user1.id, user2.id)
        FollowingService.follow(user1.id, user3.id)
        FollowingService.follow(user2.id, user1.id)
        
        print(f"Alice follows: {[u.username for u in FollowingService.get_following(user1.id)]}")
        print(f"Bob's followers: {[u.username for u in FollowingService.get_followers(user2.id)]}")
        
        # Test unfollow
        FollowingService.unfollow(user1.id, user2.id)
        print(f"Alice unfollowed Bob. Alice now follows: {[u.username for u in FollowingService.get_following(user1.id)]}")
        
        print("Tests completed successfully.")

if __name__ == '__main__':
    run_tests()
