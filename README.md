# khu-auth-python

# Installation

on python 3.x environment

```bash
$ pip install khuauth
```

# Quickstart

Let's try khu-auth-python with some simple codes.

```python
# simple.py
from khuauth.auth import authenticate

ID = {{YOUR_INFO_21_ID}}
PW = {{YOUR_INFO_21_PW}}

print(authenticate(ID, PW))
```

```bash
# An example of output
$ python simple.py

INFO:root:Start khu authentication
INFO:root:Finish khu authentication
{'user_id': 'your_id', 'verified': True, 'student_number': '123123123'}
```

