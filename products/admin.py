from flask import g, url_for, redirect, request
from wtforms import TextAreaField

from .models import Product, Category
from flask_admin.contrib.sqla import ModelView

from config.database import db_session
from config.settings import admin


class AdminModelView(ModelView):

    def is_accessible(self):
        if g.user.is_authenticated:
            return g.user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.endpoint))


class ProductView(AdminModelView):
    column_exclude_list = ['description']
    can_create = False
    can_view_details = True

    form_overrides = dict(description=TextAreaField)


admin.add_view(AdminModelView(Category,
                              db_session,
                              name="categories",
                              menu_icon_type="fa",
                              menu_icon_value="fa-list"))
admin.add_view(ProductView(Product, db_session,
                           name="products",
                           menu_icon_type="fa",
                           menu_icon_value="fa-database"))
