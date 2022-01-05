from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1,'bob', 'asdf')
]

# by this mapping, we do not have to sort it everytime

username_mapping = {u.username: u for u in users}
# username_mapping_old = {'bob':
#     {
#         'id':1,
#         'username':'bob',
#         'password':'asdf'
#     }
# }

userid_mapping = {u.id: u for u in users}
# userid_mapping_old = { 1:
#     {
#         'id':1,
#         'username':'bob',
#         'password':'asdf'
#     }
# }

def authenticate(username, password):
    user = username_mapping.get(username, None) #By .get(key), we can set a default value in the second argument
    if user and safe_str_cmp(user.password,password): # Safe way to ccompare stirngs under many possible encoding
        return user

def identity(payload): # This function encode the JWT token and identify the user_id
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)        