# related third party imports
from webapp2_extras.routes import RedirectRoute

# local application/library specific imports
from views import ReportCornJob
_routes = [
    RedirectRoute('/reports', ReportCornJob, name='Report')]


def add_routes(app):
    """Add All Routes To existing applications"""
    for r in _routes:
        app.router.add(r)

