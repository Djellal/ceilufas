import os
from flask import Flask
from extensions import db, login_manager, bcrypt, cache, csrf, toolbar
from models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ceilufas-dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ufaspg2017@127.0.0.1/ceilufas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    csrf.init_app(app)
    toolbar.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(role='admin').first():
            admin = User(
                username='admin',
                email='djellal@univ-setif.dz',
                password=bcrypt.generate_password_hash('dhb571982').decode('utf-8'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
