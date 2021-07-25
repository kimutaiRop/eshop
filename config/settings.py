from flask import Flask, g, url_for, request, redirect, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_graphql_auth import GraphQLAuth
from flask_login import LoginManager, current_user
from graphene_file_upload.flask import FileUploadGraphQLView

from auth.models import User
from .database import db_session
from .schema import schema

app = Flask(__name__)

secret = "jh876867g66236990990909%16777#ff992n623TG33fg545455"
app.config['JWT_SECRET_KEY'] = secret
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
app.config['SECRET_KEY'] = secret
app.config['REFRESH_EXP_LENGTH'] = 30
app.config["ACCESS_EXP_LENGTH"] = 10
app.config['JWT_SECRET_KEY'] = "Bearer"

auth = GraphQLAuth(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_req():
    g.user = current_user


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


app.add_url_rule("/graphql",
                 view_func=FileUploadGraphQLView.as_view(
                     "graphql",
                     schema=schema,
                     graphiql=True
                 ))

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if g.user.is_authenticated:
            if g.user.is_admin:
                return super(MyAdminIndexView,self).index()
        next_url = request.endpoint
        login_url = '%s?next=%s' % (url_for('login'), next_url)
        flash('Please login as admin  first...', 'error')
        return redirect(login_url)


admin = Admin(app, name='eshop', template_mode='bootstrap4', index_view=MyAdminIndexView(
    name="Dashboard", menu_icon_type="fa", menu_icon_value="fa-dashboard"
))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
