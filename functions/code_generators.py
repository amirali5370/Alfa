import random
from models.user import User
def invite_generator():
    string = "abcdefghijklmnopqrstuvwxyz0123456789"
    while True:
        code = ''.join(random.choice(string) for x in range(6))
        x = User.query.filter(User.invite_code==code).first()
        y = User.query.filter(User.sub_invite_code==code).first()
        if x == None and y == None:
            break
    return code


def auth_generator():
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        code = ''.join(random.choice(string) for x in range(36))
        x = User.query.filter(User.invite_auth==code).first()
        if x == None:
            break
    return code