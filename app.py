import os
from datetime import datetime
from flask import Flask
from extensions import db, login_manager, bcrypt, cache, csrf, toolbar
from models import User, AppParameter, Session

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

    app.jinja_env.globals['now'] = datetime.utcnow

    @app.context_processor
    def inject_current_session():
        current_session_param = AppParameter.query.filter_by(key='current_session').first()
        current_session = None
        if current_session_param and current_session_param.value:
            current_session = Session.query.get(int(current_session_param.value))
        
        contact_keys = ['contact_address', 'contact_website', 'contact_phone', 'contact_email', 
                        'contact_facebook', 'contact_linkedin', 'contact_youtube', 
                        'contact_instagram', 'contact_twitter']
        contact_info = {}
        for key in contact_keys:
            param = AppParameter.query.filter_by(key=key).first()
            if param and param.value:
                contact_info[key] = param.value
        
        return dict(current_session=current_session, contact_info=contact_info)

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

        # Seed default application parameters
        defaults = [
            ('current_session', None, 'Current active session ID'),
            ('registration_opened', 'true', 'Whether user registration is open'),
            ('max_registrations_per_user', '3', 'Maximum number of registrations allowed per user'),
            ('app_name', 'Ceilufas', 'Application display name'),
            ('maintenance_mode', 'false', 'Enable maintenance mode'),
            ('contact_address', '', 'Physical address'),
            ('contact_website', '', 'Website URL'),
            ('contact_phone', '', 'Phone number'),
            ('contact_email', '', 'Contact email'),
            ('contact_facebook', '', 'Facebook page URL'),
            ('contact_linkedin', '', 'LinkedIn page URL'),
            ('contact_youtube', '', 'YouTube channel URL'),
            ('contact_instagram', '', 'Instagram page URL'),
            ('contact_twitter', '', 'Twitter/X page URL'),
            ('smtp_host', 'smtp.gmail.com', 'SMTP server hostname'),
            ('smtp_port', '587', 'SMTP server port'),
            ('smtp_username', '', 'SMTP authentication username'),
            ('smtp_password', '', 'SMTP authentication password'),
            ('smtp_use_tls', 'true', 'Use TLS for SMTP connection'),
            ('smtp_sender_name', 'Ceilufas', 'Email sender display name'),
            ('smtp_sender_email', '', 'Email sender address'),
        ]
        for key, value, description in defaults:
            if not AppParameter.query.filter_by(key=key).first():
                db.session.add(AppParameter(key=key, value=value, description=description))
        db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
