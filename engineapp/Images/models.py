from google.appengine.ext import ndb


class Image(ndb.Model):

    """Models a Images/Videos entry with an email, password and date."""
    # name of Image Uploaded
    name = ndb.StringProperty()
    # user uploading images
    author = ndb.StringProperty()
    # like by Guest as well as User
    Like = ndb.IntegerProperty(default=0)
    # Actual key Join by Blob value Of Image/Video
    blob_key = ndb.BlobKeyProperty()
    # Number of dislike by Guest as well as user
    Dislike = ndb.IntegerProperty(default=0)
    # Date Modified For Ordering
    date = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get_All_Images_by_Users(cls, Author):
        """Returns all images added by users
        """
        return cls.query(cls.author == Author).order(-cls.date)

    @classmethod
    def get_all_Images(cls):
        """
        Getting all Images Randomly
        """
        return cls.query().order(-cls.date)

    @classmethod
    def get_Detail(cls, id):
        """
        Getting Details Of Individual Images
        """
        return cls.get_by_id(id)


class Comment(ndb.Model):

    """Models For Comment
    Here Comments are entered by either login user or Guest"""
    Comment = ndb.TextProperty()
    Author = ndb.TextProperty()
    Image = ndb.KeyProperty(kind='Image')
    Date = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get_Detail(cls, key):
        """
        Getting Details Of Individual Images
        """
        return cls.query(cls.Image==key).order(-cls.Date).fetch(3)

    @classmethod
    def get_report_Detail(cls, key):
        """
        Getting Details Of Individual Images
        """
        return cls.query(cls.Image==key)
