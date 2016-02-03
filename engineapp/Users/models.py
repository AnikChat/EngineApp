from webapp2_extras.appengine.auth.models import User
from google.appengine.ext import ndb


class User(User):
    """Models a Users entry with an email, password and date."""
    email = ndb.StringProperty()
    password = ndb.TextProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    active = ndb.BooleanProperty()

    @classmethod
    def get_by_email(cls, email):
        """Returns a user object based on an email.

        :param email:
            String representing the user email. Examples:

        :returns:
            A user object.
        """
        return cls.query(cls.email == email).get()

    @classmethod
    def get_Emails(cls):
        """Returns all user objects for Reporting purpose.

        :returns:
            A user object.
        """
        return cls.query()
