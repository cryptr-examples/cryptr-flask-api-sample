"""Python Flask Cryptr Resource server integration sample
"""
from flask import Flask, request, jsonify, _request_ctx_stack
import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_cors import cross_origin
from jose import jwt
 
app = Flask(__name__)
 
app.config.from_object('config')

def issuer():
   return app.config["CRYPTR_BASE_URL"] + "/t/" + app.config["CRYPTR_TENANT_DOMAIN"]
 
def jwks_uri():
   return issuer() + "/.well-known"

# Error handler
class AuthError(Exception):
   def __init__(self, error, status_code):
       self.error = error
       self.status_code = status_code
 
@app.errorhandler(AuthError)
def handle_auth_error(ex):
   response = jsonify(ex.error)
   response.status_code = ex.status_code
   return response
 
# Authorization request check
def requires_auth(f):
   """Retrieve token and validate it
   """
   @wraps(f)
   def decorated(*args, **kwargs):
       token = get_token_auth_header()
       rsa_key = get_rsa_key(token)
       validate_token(token, rsa_key)
       return f(*args, **kwargs)
   return decorated
 
def get_token_auth_header():
   """Obtains the Access Token from the Authorization Header
   """
   auth = request.headers.get("Authorization", None)
   if not auth:
       raise AuthError({
           "code": "authorization_header_missing",
           "description": "Authorization header is required"
           }, 401)
 
   parts = auth.split()
   if parts[0].lower() != "bearer" or len(parts) != 2:
       raise AuthError({
           "code": "invalid_header",
           "description": "Wrong Bearer Authorization header syntax"
       })
   return parts[1]
 
def get_rsa_key(token):
   jsonurl = urlopen(jwks_uri())
   jwks = json.loads(jsonurl.read())
   unverified_header = jwt.get_unverified_header(token)
   rsa_key = {}
   for key in jwks["keys"]:
       if key["kid"] == unverified_header["kid"]:
           rsa_key = key
   return rsa_key
 
def validate_token(token, rsa_key):
   if rsa_key:
       try:
           payload = jwt.decode(
               token,
               rsa_key,
               algorithms=["RS256"],
               audience=app.config["CRYPTR_AUDIENCE"],
               issuer=issuer()
           )
       except jwt.ExpiredSignatureError as expiredErr:
           raise AuthError({
               "code": "token_expired",
               "description": "token is expired"}, 401)
       except jwt.JWTClaimsError as expiredErr:
           raise AuthError({
               "code": "invalid_claims",
               "description": "incorrect claims, please check the audience and issuer"}, 401)
       except Exception as err:
           raise AuthError({
               "code": "invalid_header",
               "description": err}, 401)
       _request_ctx_stack.top.current_user = payload
       return
   raise AuthError({
               "code": "no_rsa_key",
               "description": "Unable to find appropriate key"}, 401)

@app.route('/api/v1/courses')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth

def index():
   return jsonify([
       {
           "id": 1,
               "user_id": "eba25511-afce-4c8e-8cab-f82822434648",
               "title": "learn git",
               "tags": ["colaborate", "git" ,"cli", "commit", "versionning"],
               "img": "https://carlchenet.com/wp-content/uploads/2019/04/git-logo.png",
               "desc": "Learn how to create, manage, fork, and collaborate on a project. Git stays a major part of all companies projects. Learning git is learning how to make your project better everyday",
               "date": '5 Nov',
               "timestamp": 1604577600000,
               "teacher": {
                   "name": "Max",
                   "picture": "https://images.unsplash.com/photo-1558531304-a4773b7e3a9c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
               }
       }
   ])
 
if __name__ == "__main__":
 app.run(debug=True)
