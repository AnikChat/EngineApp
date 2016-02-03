"""
author : Anik.Chaturvedi
Use :    All the Business process Goes Here
"""
import logging

# related third party imports
from webapp2_extras import security

from wtforms.fields import PasswordField, TextField
from wtforms import Form


# local application/library specific imports
from models import User
from utils import id_generator, ceaser_cipher


class UserForm(Form):

    """Models a Users entry with an email,
    password and date and Sucess Message
    """
    password = PasswordField("Password")
    email = TextField("Email")
    Name = TextField("Name")

    def save(self):
        """Sign up Services"""
        account = User.get_by_email(self.email)
        if not account:
            account = User(email=self.email, name=self.Name,
                           password=ceaser_cipher(self.password), active=True)
            account.put()
            logging.error('Returning 0 from Here:::', self.email)
            return self.email, 0
        else:
            return account.email, 409

    def find_or_update(self, request):
        """Find  User or update password"""
        account = User.get_by_email(self.email)
        logging.error('Ther You go hiud')
        if request == 'GET':
            if account is not None:
                if account.password == ceaser_cipher(self.password):
                    return account.email, 0
                else:
                    return None, 404
            else:
                return None, 404
        else:
            if account is not None:
                if self.password is None:
                    Password = id_generator()
                    account.password = security.generate_password_hash(
                        Password, length=12)
                    account.active = False
                    return account.email, 406
                else:
                    account.password = security.generate_password_hash(
                        self.Password, length=12)
                    account.active = True
                    return account.email, 407
            else:
                return None, 405
