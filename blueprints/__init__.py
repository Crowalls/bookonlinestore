# __init__.py

from flask import Blueprint

# 初始化各个蓝图
register_bp = Blueprint('register', __name__)
login_bp = Blueprint('login', __name__)
book_bp = Blueprint('book', __name__)
cart_bp = Blueprint('cart', __name__)
profile_bp = Blueprint('profile', __name__)
order_bp = Blueprint('order', __name__)
admin_bp = Blueprint('admin', __name__)

# 导入各个蓝图的路由模块
from . import register_bp_routes
from . import login_bp_routes
from . import book_bp_routes
from . import cart_bp_routes
from . import profile_bp_routes
from . import order_bp_routes
from . import admin_bp_routes
