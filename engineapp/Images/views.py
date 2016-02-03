# standard library imports
import logging

# related third party imports
import webapp2
from webapp2_extras import jinja2
from webapp2_extras import sessions
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url
from google.appengine.ext.webapp import template

from config import ERROR_MESSAGES

# local application/library specific imports
from models import Image, Comment


image_types = ('image/bmp', 'image/jpeg', 'image/png',
               'image/gif', 'image/tiff', 'image/x-icon')

video_types = ('video/mp4')


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


class PhotoUploadFormHandler(BaseHandler):

    def get(self):
        if not self.session.get('mail'):
            logging.error('In Here :::')
            self.session['Error_Message'] = ERROR_MESSAGES[2]
            self.redirect('/Home')
        upload_url = blobstore.create_upload_url('/upload_photo')
        # To upload files to the blobstore, the request method must be "POST"
        # and enctype must be set to "multipart/form-data".
        self.response.out.write(
            template.render('templates/Upload.html',
                            {'upload': upload_url, 'author': str(self.session.get('mail'))
                             }))


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):
        try:
            logging.error("Before")
            upload = self.get_uploads()[0]
            name = self.request.get('image_name')
            author = self.request.get('author')
            logging.error("Nmae is " + name)
            Photo = Image(
                name=name,
                blob_key=upload.key(),
                author=author)
            logging.error('put is done')
            pic = Photo.put()
            logging.error('Put is not..')
            pic_id = "/Home#" + str(pic.id())
            render = template.render('templates/redirect.html',
                                     {'link': pic_id, 'message': 'Uploaded'})
            self.response.write(render)

        except:
            self.error(500)


class ListPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler,
                       BaseHandler):

    def get(self):
        # Get the all user pics
        pics = Image.get_all_Images()
        logging.error('Value Of Anik Is ::' + str(self.session.get('mail')))
        params = {}
        if self.session.get('Error_Message'):
            params = {
                'Error_Message': str(self.session.get('Error_Message'))
            }
        if self.session.get('mail'):
            mail = self.session.get('mail')
            params.update({
                'log': "", 'logged': "none"
            })
        else:
            mail = ''
            params.update({
                'log': "none", 'logged': ""
            })
        self.session['Error_Message'] = None
        page = template.render('templates/Home_Header.html', params)
        if not pics:
            self.error(404)
        else:
            for pic in pics:
                if not blobstore.get(pic.blob_key):
                    logging.error('oops something went Terribly wrong.')
                else:
                    logging.error("befor key")
                    key = blobstore.get(pic.blob_key)
                    logging.error("after key befor serving"+str(key))
                    blob_info = blobstore.BlobInfo.get(pic.blob_key)
                    # This Code Fails in Production 
                    if blob_info.content_type in image_types:
                        url = get_serving_url(key)
                        logging.error("after serving"+str(url))
                        comments = Comment.get_Detail(pic.key)
                        context = {'id': pic.key.id(), 'Name': pic.name,
                                   'url': url, 'user': pic.author,
                                   'comments': comments, 'nlikes': pic.Like,
                                   'ndislikes': pic.Dislike,
                                   'email': mail
                                   }
                        logging.error('This is where right?')
                        logging.error(
                            'This is where right?' + blob_info.content_type)
                        if blob_info.content_type in image_types:
                            logging.error('This is where right?')
                            page = page + \
                                template.render(
                                    'templates/Home_Form_Image.html', context)
                        elif blob_info.content_type in video_types:
                            page = page + \
                                template.render(
                                    'templates/Home_Form_Video.html', context)
                        else:
                            logging.error("Something is Missed" + str(pic.id))
                    else:
                        logging.error('We got Video Over Here:::::')
            page = page + template.render('templates/Home_footer.html', {})
            self.response.write(page)


class CommentHandler(BaseHandler):

    def post(self):
        logging.error(self.request.get('pid'))
        photo_id = int(self.request.get('pid'))
        Author = self.request.get('comment-name')
        comment = self.request.get('comment')
        photo = Image.get_Detail(photo_id)
        logging.error("Author is" + Author)
        logging.error(comment)
        if Author == '' or comment == '':
            pic_id = "/Home#" + str(photo_id)
            self.redirect(pic_id)
            logging.error("Is it here?")
        else:
            if photo:
                try:
                    comment = Comment(
                        Author=Author,
                        Comment=comment, Image=photo.key)
                    comment.put()
                    logging.info("Horray, a comment is saved.")
                except:
                    logging.error("Error saving User in datastore.")
                finally:
                    pic_id = "/Home#" + str(photo_id)
                    render = template.render('templates/redirect.html',
                                             {'link': pic_id, 'message': 'Commented'})
                    self.response.write(render)


class LikeHandler(BaseHandler):

    def post(self):
        photo_id = int(self.request.get('pid'))
        photo = Image.get_Detail(photo_id)
        if photo:
            try:
                photo.Like = photo.Like + 1
                photo.put()
            except:
                logging.error("Error saving User in datastore.")
            finally:
                pic_id = "/Home#" + str(photo_id)
                render = template.render('templates/redirect.html',
                                         {'link': pic_id, 'message': 'Liked'})
                self.response.write(render)


class DisLikeHandler(BaseHandler):

    def post(self):
        photo_id = int(self.request.get('pid'))
        photo = Image.get_Detail(photo_id)
        if photo:
            try:
                photo.Dislike = photo.Dislike + 1
                photo.put()
            except:
                logging.error("Error saving User in datastore.")
            finally:
                pic_id = "/Home#" + str(photo_id)
                logging.error("after picid before page")
                render = template.render('templates/redirect.html',
                                         {'link': pic_id, 'message': 'Disliked'})
                self.response.write(render)
