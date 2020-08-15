import sys
import khuauth
# from khuauth import auth

print(khuauth.auth.authenticate(sys.argv[1], sys.argv[2]))