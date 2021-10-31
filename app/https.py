from flask import Blueprint
from flask import redirect

from flask import request


https_bp = Blueprint('https', __name__)

@https_bp.route('/', methods=['GET', 'POST'])
def do():
    # request.get_data()
    return 'RWBgegO40X1gX7d131JRyYFnmGM2xSeXD3j5Nl2zhw4.6x6mzYkOW_Izv2BYmt-XY63QZmksg2QXtjPU65DU_Qk'