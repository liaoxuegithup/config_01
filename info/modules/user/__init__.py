from flask import Blueprint

user_blue = Blueprint("user",__name__,url_prefix="/user")

from . import views
# passport_blue = Blueprint("passport",__name__,url_prefix="/passport")
#
# from . import views