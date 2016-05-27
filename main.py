import webapp2
from google.appengine.ext.ndb import model
from webapp2_extras import auth
import json


def jsonMsg(response,msg):
    response.write(json.dumps({"msg": msg}, indent=2) + '\n')


class RegHandler(webapp2.RequestHandler):
    def post(self):
        print self.request.POST

        name = self.request.POST.get('name')
        passw = self.request.POST.get('password')

        if not name or not passw:
            jsonMsg(self.response, 'Missing Required Field')
            self.response.set_status(400, "Missing required field")
            return

        success, user = auth.get_auth().store.user_model.create_user(name, password_raw=passw)

        if not success:
            prefix='Unable to create that user:'

            if 'auth_id' in user:
                jsonMsg(self.response, prefix + " Username Already Taken")
                self.response.set_status(400)
            else:
                jsonMsg(self.response, prefix + " Server Error")
                self.response.set_status(500)
            return

        else:
            print user
            self.response.write(
                json.dumps({"msg": "User Logged In",
                            'userid': user.key.id(),
                            'token': user.create_auth_token(user.key.id())},
                           indent=2
                           ))
            self.response.set_status(200)
            return


class LogHandler(webapp2.RequestHandler):
    def post(self):
        print self.request.POST

        name = self.request.POST.get('name')
        passw = self.request.POST.get('password')

        if not name or not passw:
            jsonMsg(self.response, 'Missing required field')
            self.response.set_status(400, "Missing required field")
            return

        print dir(auth.get_store())

        try:
            #user = auth.get_auth().get_user_by_password(name, passw, save_session=False)
            user = auth.get_auth().store.user_model.get_by_auth_password(name, passw)
        except auth.InvalidPasswordError:
            jsonMsg(self.response, "Invalid Password")
            self.response.set_status(400)
            return
        except auth.InvalidAuthIdError:
            jsonMsg(self.response, "User Does Not Exist")
            self.response.set_status(400)
            return

        if not user:
            jsonMsg(self.response, "Login Failed")
            self.response.set_status(500)
            return
        else:
            print user
            self.response.write(
                json.dumps({"msg": "User Logged In",
                            'userid': user.key.id(),
                            'token': user.create_auth_token(user.key.id())},
                           indent=2
                           ))
            self.response.set_status(200)
            return

#will be changed to function when brought into project
class TokenHandler(webapp2.RequestHandler):
    def post(self):
        print self.request.POST

        id = self.request.POST.get('id')
        token = self.request.POST.get('token')

        if not id or not token:
            jsonMsg(self.response, 'Missing required field')
            self.response.set_status(400, "Missing required field")
            return
        if not id.isdigit():
            jsonMsg(self.response, 'ID must be numeric')
            self.response.set_status(400, "Missing required field")
            return
        user, timestamp = auth.get_auth().store.user_model.get_by_auth_token(int(id), token)
        print user
        self.response.write("Hello %s"%(user.auth_ids[0]))


app = webapp2.WSGIApplication([
    ('/register', RegHandler),
    ("/login", LogHandler),
    ('/token', TokenHandler)
], debug=True)
