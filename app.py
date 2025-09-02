from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate



db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from models import Category
    @app.context_processor
    def inject_categories():
        categories = Category.query.all()
        return dict(categories=categories)
    
    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    migrate = Migrate(app, db)

    from apps.auth.auth import auth
    from apps.products.products import product
    from models import User
    
    app.register_blueprint(auth)
    app.register_blueprint(product)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        print(current_app.name)
        db.create_all()
    
        
    return app

if __name__ == '__main__':
    create_app().run()