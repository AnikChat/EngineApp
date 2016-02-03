# related third party imports
from webapp2_extras.routes import RedirectRoute

# local application/library specific imports
from views import SignupHandler, LoginHandler, LogoutHandler

_routes = [
    RedirectRoute('/sign', SignupHandler, name='sign', strict_slash=True),
    RedirectRoute('/Login', LoginHandler, name='Login', strict_slash=True),
    RedirectRoute('/Logout', LogoutHandler, name='Logout', strict_slash=True),
    ]


def add_routes(app):
    """Add All Routes To existing applications"""
    for r in _routes:
        app.router.add(r)
