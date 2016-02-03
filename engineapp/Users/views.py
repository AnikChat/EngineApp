# standard library imports
import logging

# related third party imports
import webapp2
from webapp2_extras import sessions
from webapp2_extras import jinja2


# local application/library specific imports
from forms import UserForm
from config import ERROR_MESSAGES


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, **template_args):
        self.response.write(
            self.jinja2.render_template(filename, **template_args))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


class SignupHandler(BaseHandler):

    """Handler for Signup form
    """

    def get(self):
        """ Returns a simple HTML form for create a new user """
        self.render_template('Signup.html')

    def post(self):
        try:
            form = UserForm()
            form.email = self.request.get('email')
            form.password = self.request.get('password')
            form.Name = self.request.get('name')
            email, Error_Message = form.save()
            self.session['mail'] = email
            self.session['Error_Message'] = ERROR_MESSAGES[Error_Message]
            logging.info(
                "Horray, User Increased in database." +
                self.session.get('mail'))
        except:
            logging.error("Error saving User in datastore")
        finally:
            self.redirect('/Home')


class LoginHandler(BaseHandler):

    def post(self):
        """ Checks Wether the login is Correct Or Not"""
        try:
            form = UserForm()
            form.email = self.request.get('email')
            form.password = self.request.get('password')
            mail, Error_Message = form.find_or_update('GET')
            if Error_Message == 0:
                self.session['mail'] = mail
            self.session['Error_Message'] = ERROR_MESSAGES[Error_Message]
            logging.info("Horray, Login Sucessful.")
        except:
            self.session['Error_Message'] = ERROR_MESSAGES[408]
            logging.error("Error saving User in datastore")
        finally:
            self.redirect('/Home')


class LogoutHandler(BaseHandler):

    def post(self):
        self.session['mail'] = None
        self.session['Error_Message'] = ERROR_MESSAGES[410]
        self.redirect('/Home/')

# Need To Create Forgot Password
