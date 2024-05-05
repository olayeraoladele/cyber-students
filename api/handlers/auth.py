from datetime import datetime
from time import mktime
from tornado.gen import coroutine
from .utils import myDecrypt  

from .base import BaseHandler

class AuthHandler(BaseHandler):

    @coroutine
    def prepare(self):
        super(AuthHandler, self).prepare()

        if self.request.method == 'OPTIONS':
            return

        try:
            token = self.request.headers.get('X-Token')
            if not token:
              raise Exception()
        except:
            self.current_user = None
            self.send_error(400, message='You must provide a token!')
            return

        # the field names need to match the field names in registration.py
        user = yield self.db.users.find_one({
            'token': token
        }, {

            'emailAddress': 1,
            'address': 1,
            'displayName': 1,
            'telephone_number': 1,
            'disability': 1,
            'expiresIn': 1,
            'encrypt_emailAddress':1,
            'encrypt_telephone_number': 1,
            'encrypt_disability' : 1,
            'encrypt_address' : 1,
            'encrypt_dateOfBirth' : 1
            
        })

        if user is None:
            self.current_user = None
            self.send_error(403, message='Your token is invalid!')
            return

        current_time = mktime(datetime.now().utctimetuple())
        if current_time > user['expiresIn']:
            self.current_user = None
            self.send_error(403, message='Your token has expired!')
            return
                
        self.current_user = {
            'emailAddress': user['emailAddress'],
            'display_name': myDecrypt(user['displayName']),
             'telephone_number' : myDecrypt (user['encrypt_telephone_number']),
             'encrypt_disability':myDecrypt(user['encrypt_disability']),
             'encrypt_address':myDecrypt(user['encrypt_address']),
             'encrypt_dateOfBirth':myDecrypt(user['encrypt_dateOfBirth'])
            
        }
       
        return user
