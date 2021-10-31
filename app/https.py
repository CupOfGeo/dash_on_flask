from flask import Blueprint
from flask import redirect

from flask import request


https_bp = Blueprint('https', __name__)

@https_bp.route('/', methods=['GET', 'POST'])
def do():
    # request.get_data()
    return 'p6sRGSUYKKN3uUVQmxHhAZXK6VHAVikV2Gy0fgfZHxY.6x6mzYkOW_Izv2BYmt-XY63QZmksg2QXtjPU65DU_Qk'