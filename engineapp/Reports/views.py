import webapp2
from google.appengine.api import mail

from Users.models import User
from Images.models import Image, Comment
from config import config


class ReportHandler(webapp2.RequestHandler):

    """
    Getting Reports For All Users
    """

    def Send_Mail(self):
        Photos = Image.get_All_Images_by_Users()
        Mail_Content = config['Mail_content_Header']
        Content = 0
        for photo in Photos:
            comments = Comment.get_Detail(photo.key.id())
            Total_Comments = comments.count()
            Total_Likes = photo.Like
            Total_Dislike = photo.Dislike
            Name = photo.Name
            Content = Content + 1
            Mail_Content = Mail_Content + """"
            {0}+ {1}   Likes:{2}   Dislike:{3} Comments:{4}
            """.format(
                Content, Name, Total_Likes, Total_Dislike, Total_Comments)
        if Content == 0:
            Mail_Content = Mail_Content + """
            Oops, It seems you have not uploaded anything till Now."""
        Mail_Content = Mail_Content + config['Mail_content_footer']
        message = mail.EmailMessage()
        message.sender = config['contact_sender']
        message.to = config['receiver']
        message.body = Mail_Content
        message.send()


class ReportCornJob(ReportHandler):

    def get(self):
        if 'X-AppEngine-Corn' not in self.request.headers:
            self.error(403)
        self.Send_Mail()
