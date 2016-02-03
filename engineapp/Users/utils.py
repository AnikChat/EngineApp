import string
import random
from google.appengine.api import mail


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generating Passwords for user name"""
    return ''.join(random.choice(chars) for _ in range(size))


def Send_Mail(Password, To_mail):
    message = mail.EmailMessage(sender="Example.com Support <support@example.com>",
                                subject="Change Password")

    message.to = To_mail
    message.body = """
	Hi,

	Your Temporaty password is """ + str(Password) + """
	Please let us know if you have any questions.

	Thanks,
	Anik Chaturvedi
	"""

    message.send()


def ceaser_cipher(mess):
    cipher = ''
    for character in mess:
        encrypt = ord(character) + 3
        cipher = cipher + str(unichr(encrypt))
    return cipher
