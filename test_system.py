from app import create_app
from models import db, User, Follower
from services import FollowingService, TweetService

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
        
        # Test Tweet creation and feed propagation
        print("\n--- Testing Tweet Creation and Feed Propagation ---")
        # Bob creates a tweet
        tweet1 = TweetService.create_tweet(user2.id, "Hello, this is Bob's first tweet!")
        print(f"Bob created a tweet: '{tweet1.content}'")
        
        # Charlie creates a tweet
        tweet2 = TweetService.create_tweet(user3.id, "Hello, this is Charlie's first tweet!")
        print(f"Charlie created a tweet: '{tweet2.content}'")
        
        # Alice gets her feed (Alice follows Bob and Charlie, so should see both)
        alice_feed = TweetService.get_feed(user1.id)
        print(f"Alice's Feed: {[t.content for t in alice_feed]}")
        assert len(alice_feed) == 2, "Alice's feed should have 2 tweets."
        
        # Bob gets his feed (Bob follows Alice, Alice hasn't tweeted, but Bob should see his own tweet)
        bob_feed = TweetService.get_feed(user2.id)
        print(f"Bob's Feed: {[t.content for t in bob_feed]}")
        assert len(bob_feed) == 1, "Bob's feed should have 1 tweet (his own)."
        
        # Test unfollow
        FollowingService.unfollow(user1.id, user2.id)
        print(f"Alice unfollowed Bob. Alice now follows: {[u.username for u in FollowingService.get_following(user1.id)]}")
        
        print("Tests completed successfully.")

if __name__ == '__main__':
    run_tests()
