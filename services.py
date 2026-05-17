from models import db, User, Follower, Tweet, Feed

class FollowingService:
    @staticmethod
    def follow(follower_id, followed_id):
        """
        Allows a user to follow another user.
        """
        if follower_id == followed_id:
            raise ValueError("A user cannot follow themselves.")
        
        # Check if the follow relationship already exists
        existing_follow = Follower.query.filter_by(
            follower_id=follower_id, 
            followed_id=followed_id
        ).first()
        
        if existing_follow:
            return existing_follow # Already following
            
        new_follow = Follower(follower_id=follower_id, followed_id=followed_id)
        db.session.add(new_follow)
        db.session.commit()
        return new_follow

    @staticmethod
    def unfollow(follower_id, followed_id):
        """
        Allows a user to unfollow another user by deleting the entry.
        """
        follow_record = Follower.query.filter_by(
            follower_id=follower_id, 
            followed_id=followed_id
        ).first()
        
        if follow_record:
            db.session.delete(follow_record)
            db.session.commit()
            return True
        return False
        
    @staticmethod
    def get_followers(user_id):
        """
        Get all users who follow the given user_id.
        """
        followers = db.session.query(User).join(
            Follower, User.id == Follower.follower_id
        ).filter(Follower.followed_id == user_id).all()
        return followers

    @staticmethod
    def get_following(user_id):
        """
        Get all users that the given user_id is following.
        """
        following = db.session.query(User).join(
            Follower, User.id == Follower.followed_id
        ).filter(Follower.follower_id == user_id).all()
        return following


class TweetService:
    @staticmethod
    def create_tweet(user_id, content):
        """
        Creates a new tweet and fan-out on write to all followers' feeds.
        """
        # 1. Create Tweet
        new_tweet = Tweet(user_id=user_id, content=content)
        db.session.add(new_tweet)
        db.session.flush() # Flush to populate new_tweet.id

        # 2. Add to the author's own feed
        own_feed = Feed(user_id=user_id, tweet_id=new_tweet.id)
        db.session.add(own_feed)

        # 3. Get all followers of the author
        followers = FollowingService.get_followers(user_id)
        
        # 4. Insert into feed for each follower
        for follower in followers:
            feed_entry = Feed(user_id=follower.id, tweet_id=new_tweet.id)
            db.session.add(feed_entry)
            
        db.session.commit()
        return new_tweet

    @staticmethod
    def get_feed(user_id):
        """
        Gets the feed for the given user_id, sorted by created_at desc.
        """
        # Join Feed with Tweet to fetch actual tweet content
        tweets = db.session.query(Tweet).join(
            Feed, Tweet.id == Feed.tweet_id
        ).filter(Feed.user_id == user_id).order_by(Feed.created_at.desc()).all()
        return tweets
