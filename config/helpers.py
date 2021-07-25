import os
import re

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def check(email):
    if re.search(regex, email):
        return True
    else:
        return False


file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
