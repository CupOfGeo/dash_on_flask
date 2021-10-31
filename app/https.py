from flask import Blueprint
from flask import redirect

from flask import request


https_bp = Blueprint('https', __name__)

@https_bp.route('/', methods=['GET', 'POST'])
def do():
    # request.get_data()
    return 'TKQ2uV9JSfjoUVDIoms_JAkJda4arCa9VDupwFJZjqg.6x6mzYkOW_Izv2BYmt-XY63QZmksg2QXtjPU65DU_Qk'