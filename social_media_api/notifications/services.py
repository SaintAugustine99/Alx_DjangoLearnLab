from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None, description=None):
    """
    Create a new notification.
    
    Args:
        recipient: User who receives the notification
        actor: User who triggered the notification
        verb: Action description (e.g., "liked", "commented", "followed")
        target: Object that the action is performed on (e.g., a Post)
        description: Additional text information
    
    Returns:
        Notification object
    """
    if recipient == actor:
        # Don't notify users of their own actions
        return None
        
    if target:
        content_type = ContentType.objects.get_for_model(target)
        object_id = target.id
    else:
        content_type = None
        object_id = None
    
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=object_id,
        description=description
    )
    
    # Here you could implement real-time notifications with WebSockets or similar technology
    
    return notification

def create_like_notification(like):
    """
    Create a notification when a user likes a post.
    """
    return create_notification(
        recipient=like.post.author,
        actor=like.user,
        verb='liked',
        target=like.post,
        description=f"{like.user.username} liked your post: {like.post.title}"
    )

def create_comment_notification(comment):
    """
    Create a notification when a user comments on a post.
    """
    return create_notification(
        recipient=comment.post.author,
        actor=comment.author,
        verb='commented on',
        target=comment.post,
        description=f"{comment.author.username} commented on your post: {comment.post.title}"
    )

def create_follow_notification(follower, followed):
    """
    Create a notification when a user follows another user.
    """
    return create_notification(
        recipient=followed,
        actor=follower,
        verb='followed',
        target=followed,
        description=f"{follower.username} started following you"
    )