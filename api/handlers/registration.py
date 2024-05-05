from json import dumps
from logging import info
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine

from .utils import my_encrypt, hash_pass 

from .base import BaseHandler

class RegistrationHandler(BaseHandler):
    @coroutine
    def post(self):
        try:
            body = json_decode(self.request.body)
            emailAddress = body['emailAddress'].lower().strip()
            if not isinstance(emailAddress, str):
                raise Exception()
            password = body['password']
            if not isinstance(password, str):
                raise Exception()
            
            dateOfBirth = body['dateOfBirth']
            if not isinstance(dateOfBirth, str):
                 raise Exception()
            address = body['address']
            if not isinstance(address, str):
                 raise Exception()
            disabilities = body['disabilities']
            if not isinstance(disabilities, str):
                 raise Exception()
            telephone_number = body['telephone_number']
            if not isinstance(telephone_number, str):
                 raise Exception()
            
            display_name = body.get('displayName')
            if display_name is None:
                display_name = emailAddress
            if not isinstance(display_name, str):
                raise Exception()
                
             
            address = body['address']
            if not isinstance(address, str):
                raise Exception()
            
              
            dateOfBirth = body['dateOfBirth']
            if not isinstance(dateOfBirth, str):
                raise Exception()
            
              

        except Exception as e:
            self.send_error(400, message='You must provide an email address, password, display name, address, disability ...!')
            return

        if not emailAddress:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return

        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return
        
        if not address:
             self.send_error(400, message='The address name is invalid!')
             return

        if not telephone_number:
             self.send_error(400, message='Telephone number is invalid!')
             return

        if not disabilities:
             self.send_error(400, message='You must indicate!')
             return

        user = yield self.db.users.find_one({
          'emailAddress': emailAddress
        }, {})

        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return

        
        encrypted_display_name = my_encrypt(display_name)
        encrypted_address = my_encrypt(address)
        encrypted_telephone_number = my_encrypt(telephone_number)
        encrypted_disabilities = my_encrypt(disabilities)
        encrypted_dateOfBirth = my_encrypt(dateOfBirth)
          
        
        
        hashed_password = hash_pass(password)

         
        yield self.db.users.insert_one({
            'emailAddress': emailAddress,
            
            'hashed_password': hashed_password,
            'displayName': encrypted_display_name,
            
             
            'encrypt_address' : encrypted_address,
             
            'dateOfBirth': encrypted_dateOfBirth,
            'telephone_number' : encrypted_telephone_number,
            'disability': encrypted_disabilities
       })
        
         
        self.set_status(200)
        self.response['emailAddress'] = emailAddress
        self.response['displayName'] = display_name
        self.response['address'] = address
        self.response['disabilities'] = disabilities
        self.response['dateOfBirth'] = dateOfBirth
        self.response['telephone_number'] = telephone_number
         

        self.write_json()