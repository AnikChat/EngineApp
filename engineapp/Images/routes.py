# related third party imports
from webapp2_extras.routes import RedirectRoute

# local application/library specific imports
from views import PhotoUploadFormHandler, PhotoUploadHandler
from views import ListPhotoHandler, CommentHandler, LikeHandler, DisLikeHandler, ViewPhotoHandler

_routes = [
     RedirectRoute(
        '/', ListPhotoHandler,
        name='Home', strict_slash=True),
    RedirectRoute(
        '/Home', ListPhotoHandler,
        name='Home', strict_slash=True),
    RedirectRoute(
        '/upload', PhotoUploadFormHandler, name='upload', strict_slash=True),
    RedirectRoute(
        '/upload_photo', PhotoUploadHandler,
        name='upload_photo', strict_slash=True),
    RedirectRoute(
        '/comment', CommentHandler,
        name='comment', strict_slash=True),
    RedirectRoute(
        '/like', LikeHandler,
        name='upload_photo', strict_slash=True),
    RedirectRoute(
        '/dislike', DisLikeHandler,
        name='upload_photo', strict_slash=True),
    RedirectRoute(
        '/view_photo/<photo_key:[^/]+>', ViewPhotoHandler,
        name='view_photo', strict_slash=True),
]


def add_routes(app):
    """Add All Routes To existing applications"""
    for r in _routes:
        app.router.add(r)
