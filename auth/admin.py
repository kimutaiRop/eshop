from flask_admin.contrib.sqla import ModelView

from config.database import db_session
from config.settings import admin
from .models import User


admin.add_view(ModelView(User, db_session, name="users", menu_icon_type="fa", menu_icon_value="fa-users"))
