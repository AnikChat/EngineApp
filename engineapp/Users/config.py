
config = {

    # application name
    'app_name': "engineapp",

    # secret Key
    'webapp2_extras.sessions':
    {'secret_key': 'Sercret12key21is12Super21Secret'},

    # jinja2 base layout template
    'base_layout': 'base.html'


}

ERROR_MESSAGES = {
    0: 'Login Sucessful.',
    404: 'UserId or Password is Invalid.',
    405: 'Incorrect UserID.',
    406: 'Password has been Sent to You on email.',
    407: 'Password updated Sucessfully.',
    408: 'OOOPS Something went  Wrong',
    409: 'Email ID Already Entered.',
    410: 'Sucessfully Logged Out.'
}
