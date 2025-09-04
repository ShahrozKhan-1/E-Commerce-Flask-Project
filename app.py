from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from models import Category, User

    @app.context_processor
    def inject_categories():
        try:
            categories = Category.query.all()
        except Exception:
            categories = []
        return dict(categories=categories)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    Migrate(app, db)

    from apps.auth.auth import auth
    from apps.products.products import product
    app.register_blueprint(auth)
    app.register_blueprint(product)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
