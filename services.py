from models import db, User, Follower

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
