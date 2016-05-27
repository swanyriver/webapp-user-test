import webapp2
from google.appengine.ext.ndb import model
from webapp2_extras import auth


class RegHandler(webapp2.RequestHandler):
    def post(self):
        print self.request.POST

        id = self.request.POST.get('id')
        passw = self.request.POST.get('password')

        if not id or not passw:
            self.response.write('Missing Required Field\n')
            self.response.set_status(400, "Missing required field")
            return

        success, user = auth.get_auth().store.user_model.create_user(id, password_raw=passw)

        if not success:
            self.response.write('Unable to create that user:')

            if 'auth_id' in user:
                self.response.write(" Username Already Taken\n")
                self.response.set_status(400)
            else:
                self.response.write(" Server Error\n")
                self.response.set_status(500)
            return

        else:
            print user
            print type(user)
            self.response.write('User Created\n')
            self.response.set_status(202)
            return


class LogHandler(webapp2.RequestHandler):
    def post(self):
        print self.request.POST

        id = self.request.POST.get('id')
        passw = self.request.POST.get('password')

        if not id or not passw:
            self.response.write('Hello world!')
            self.response.set_status(400, "Missing required field")
            return

        print dir(auth.get_store())

        try:
            #user = auth.get_auth().get_user_by_password(id, passw, save_session=False)
            user = auth.get_auth().store.user_model.get_by_auth_password(id, passw)
        except auth.InvalidPasswordError:
            self.response.write("Invalid Password\n")
            self.response.set_status(400)
            return
        except auth.InvalidAuthIdError:
            self.response.write("User Does Not Exist\n")
            self.response.set_status(400)
            return

        if not user:
            self.response.write("Login Failed\n")
            self.response.set_status(500)
            return
        else:
            print user
            self.response.write("user logged in\n")
            self.response.write("Hello %s  id:%s\n"%(user.auth_ids[0],user.key.id()))
            self.response.write("here is your token:\n%s\n"%user.create_auth_token(user.key.id()))
            self.response.set_status(200)
            return


class TokenHandler(webapp2.RequestHandler):
    def post(self):
        print self.request.POST

        id = self.request.POST.get('id')
        token = self.request.POST.get('token')

        if not id or not token:
            self.response.write('Missing Required Field\n')
            self.response.set_status(400, "Missing required field")
            return
        if not id.isdigit():
            self.response.write('Id must be numeric\n')
            self.response.set_status(400, "Missing required field")
            return
        user, timestamp = auth.get_auth().store.user_model.get_by_auth_token(int(id), token)
        print user
        self.response.write("Hello %s\n"%(user.auth_ids[0]))


app = webapp2.WSGIApplication([
    ('/register', RegHandler),
    ("/login", LogHandler),
    ('/token', TokenHandler)
], debug=True)
