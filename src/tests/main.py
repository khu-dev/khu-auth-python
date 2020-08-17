import sys
from khuauth.auth import authenticate

print(authenticate(sys.argv[1], sys.argv[2]))