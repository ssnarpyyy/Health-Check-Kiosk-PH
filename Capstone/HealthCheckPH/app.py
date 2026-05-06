from flask import Flask
from flask_login import LoginManager
from routes import main_routes
from auth_routes import auth_routes
from auth import get_admin_by_id
from config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    
    # Set secret key for sessions
    app.secret_key = SECRET_KEY
    
    # Configure login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_routes.login_page'
    
    @login_manager.user_loader
    def load_user(user_id):
        return get_admin_by_id(int(user_id))
    
    # Register blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)
    
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)