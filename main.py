import webapp2
from webapp2_extras import auth
from webapp2_extras.appengine.auth.models import User


class RegHandler(webapp2.RequestHandler):
    def post(self):
        print self.request.POST

        id = self.request.POST.get('id')
        passw = self.request.POST.get('password')

        if not id or not passw:
            self.response.write('Missing Required Field\n')
            self.response.set_status(400, "Missing required field")
            return

        user = auth.get_auth().store.user_model.create_user(id, password_raw=passw)

        if not user[0]:
            print user[1]
            self.response.write('Unable to create that user:')

            if 'auth_id' in user[1]:
                self.response.write(" Username Already Taken\n")
                self.response.set_status(400)
            else:
                self.response.write(" Server Error\n")
                self.response.set_status(500)
            return

        else:
            print user[1]
            print type(user[1])
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
            #print user
            self.response.write("user logged in\n")
            self.response.write("Hello %s\n"%(user.auth_ids[0]))
            self.response.write("here is your token:\n%s\n"%user.create_auth_token(user.auth_ids[0]))
            self.response.set_status(200)
            return



app = webapp2.WSGIApplication([
    ('/register', RegHandler),
    ("/login", LogHandler)
], debug=True)
