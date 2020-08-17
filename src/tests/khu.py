import sys
from khuauth.auth import authenticate
import logging

logging.basicConfig(level=logging.DEBUG)
print(authenticate(sys.argv[1], sys.argv[2]))
