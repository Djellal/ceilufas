from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class CourseType(db.Model):
    __tablename__ = 'CourseTypes'
    id = db.Column('Id', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(250), nullable=False)
    name_ar = db.Column('NameAr', db.String(250), nullable=False)
    description = db.Column('Description', db.Text)

    courses = db.relationship('Course', backref='course_type', lazy=True)

    def __repr__(self):
        return f'<CourseType {self.name}>'


class Course(db.Model):
    __tablename__ = 'Courses'
    id = db.Column('Id', db.Integer, primary_key=True)
    code = db.Column('Code', db.String(30), nullable=False)
    name = db.Column('Name', db.String(250), nullable=False)
    name_ar = db.Column('NameAr', db.String(250), nullable=False)
    is_active = db.Column('IsActive', db.Boolean, nullable=False)
    image = db.Column('Image', db.Text, nullable=False)
    course_type_id = db.Column('CourseTypeId', db.Integer, db.ForeignKey('CourseTypes.Id'), nullable=False)
    order = db.Column('Order', db.Integer, nullable=False)

    components = db.relationship('CourseComponent', backref='course', lazy=True)
    fees = db.relationship('CourseFee', backref='course', lazy=True)
    levels = db.relationship('CourseLevel', backref='course', lazy=True, foreign_keys='CourseLevel.course_id')
    registrations = db.relationship('CourseRegistration', backref='course', lazy=True)
    groupes = db.relationship('Groupe', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.code}>'


class CourseComponent(db.Model):
    __tablename__ = 'CourseComponents'
    id = db.Column('Id', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(250), nullable=False)
    coeff = db.Column('Coeff', db.Float, nullable=False)
    course_id = db.Column('CourseId', db.Integer, db.ForeignKey('Courses.Id'), nullable=False)

    evaluations = db.relationship('Evaluation', backref='course_component', lazy=True)

    def __repr__(self):
        return f'<CourseComponent {self.name}>'


class CourseFee(db.Model):
    __tablename__ = 'CourseFees'
    id = db.Column('Id', db.Integer, primary_key=True)
    profession_id = db.Column('ProfessionId', db.Integer, db.ForeignKey('Professions.Id'), nullable=False)
    course_id = db.Column('CourseId', db.Integer, db.ForeignKey('Courses.Id'), nullable=False)
    fee_value = db.Column('FeeValue', db.Numeric(18, 2), nullable=False)

    def __repr__(self):
        return f'<CourseFee {self.id}>'


class CourseLevel(db.Model):
    __tablename__ = 'CourseLevels'
    id = db.Column('Id', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(250), nullable=False)
    name_ar = db.Column('NameAr', db.String(250), nullable=False)
    duration = db.Column('Duration', db.Integer, nullable=False)
    is_active = db.Column('IsActive', db.Boolean, nullable=False)
    course_id = db.Column('CourseId', db.Integer, db.ForeignKey('Courses.Id'), nullable=False)
    next_level_id = db.Column('NextLevelId', db.Integer, db.ForeignKey('CourseLevels.Id'))
    level_order = db.Column('LevelOrder', db.Integer, nullable=False, default=0)

    next_level = db.relationship('CourseLevel', remote_side=[id], uselist=False)
    registrations = db.relationship('CourseRegistration', backref='course_level', lazy=True)
    groupes = db.relationship('Groupe', backref='course_level', lazy=True)

    def __repr__(self):
        return f'<CourseLevel {self.name}>'


class State(db.Model):
    __tablename__ = 'States'
    id = db.Column('Id', db.String(10), primary_key=True)
    name = db.Column('Name', db.String(250), nullable=False)
    name_ar = db.Column('NameAr', db.String(250), nullable=False)

    municipalities = db.relationship('Municipality', backref='state', lazy=True)

    def __repr__(self):
        return f'<State {self.name}>'


class Municipality(db.Model):
    __tablename__ = 'Municipalities'
    id = db.Column('Id', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(250), nullable=False)
    name_ar = db.Column('NameAr', db.String(250), nullable=False)
    state_id = db.Column('StateId', db.String(10), db.ForeignKey('States.Id'), nullable=False)

    def __repr__(self):
        return f'<Municipality {self.name}>'


class Profession(db.Model):
    __tablename__ = 'Professions'
    id = db.Column('Id', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(300), nullable=False)
    name_ar = db.Column('NameAr', db.String(300), nullable=False)
    fee_value = db.Column('FeeValue', db.Numeric(18, 2), nullable=False)

    course_fees = db.relationship('CourseFee', backref='profession', lazy=True)

    def __repr__(self):
        return f'<Profession {self.name}>'


class Session(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column('Id', db.Integer, primary_key=True)
    session_code = db.Column('SessionCode', db.String(30), nullable=False)
    session_name = db.Column('SessionName', db.String(250), nullable=False)
    session_name_ar = db.Column('SessionNameAr', db.String(250), nullable=False)
    start_date = db.Column('StartDate', db.DateTime(timezone=True), nullable=False)
    end_date = db.Column('EndDate', db.DateTime(timezone=True), nullable=False)

    registrations = db.relationship('CourseRegistration', backref='session', lazy=True)

    def __repr__(self):
        return f'<Session {self.session_code}>'


class CourseRegistration(db.Model):
    __tablename__ = 'CourseRegistrations'
    id = db.Column('Id', db.Integer, primary_key=True)
    user_id = db.Column('UserId', db.Integer, db.ForeignKey('user.id'), nullable=False)
    inscription_code = db.Column('InscriptionCode', db.String(20), nullable=False)
    first_name = db.Column('FirstName', db.String(100), nullable=False)
    last_name = db.Column('LastName', db.String(100), nullable=False)
    first_name_ar = db.Column('FirstNameAr', db.String(100), nullable=False)
    last_name_ar = db.Column('LastNameAr', db.String(100), nullable=False)
    birth_date = db.Column('BirthDate', db.DateTime(timezone=True), nullable=False)
    birth_state_id = db.Column('BirthStateId', db.String(10), db.ForeignKey('States.Id'), nullable=False)
    birth_municipality_id = db.Column('BirthMunicipalityId', db.Integer, db.ForeignKey('Municipalities.Id'), nullable=False)
    address = db.Column('Address', db.String(250), nullable=False)
    tel = db.Column('Tel', db.String(20), nullable=False)
    profession_id = db.Column('ProfessionId', db.Integer, db.ForeignKey('Professions.Id'))
    course_id = db.Column('CourseId', db.Integer, db.ForeignKey('Courses.Id'), nullable=False)
    course_level_id = db.Column('CourseLevelId', db.Integer, db.ForeignKey('CourseLevels.Id'))
    session_id = db.Column('SessionId', db.Integer, db.ForeignKey('Sessions.Id'))
    registration_date = db.Column('RegistrationDate', db.DateTime(timezone=True), nullable=False)
    notes = db.Column('Notes', db.String(250))
    paid_fee_value = db.Column('PaidFeeValue', db.Numeric(18, 2), nullable=False)
    is_reregistration = db.Column('IsReregistration', db.Boolean, nullable=False)
    registration_terms_accepted = db.Column('RegistrationTermsAccepted', db.Boolean, nullable=False)
    registration_validated = db.Column('RegistrationValidated', db.Boolean, nullable=False)
    group_id = db.Column('GroupId', db.Integer, db.ForeignKey('Groupes.Id'))
    fee_value = db.Column('FeeValue', db.Numeric(18, 2), nullable=False, default=0.0)

    birth_state = db.relationship('State', backref='registrations', lazy=True)
    birth_municipality = db.relationship('Municipality', backref='registrations', lazy=True)
    profession = db.relationship('Profession', backref='registrations', lazy=True)
    evaluations = db.relationship('Evaluation', backref='course_registration', lazy=True)

    def __repr__(self):
        return f'<CourseRegistration {self.inscription_code}>'


class Evaluation(db.Model):
    __tablename__ = 'Evaluations'
    id = db.Column('Id', db.Integer, primary_key=True)
    course_registration_id = db.Column('CourseRegistrationId', db.Integer, db.ForeignKey('CourseRegistrations.Id'), nullable=False)
    course_component_id = db.Column('CourseComponentId', db.Integer, db.ForeignKey('CourseComponents.Id'), nullable=False)
    eval = db.Column('Eval', db.Float, nullable=False)

    def __repr__(self):
        return f'<Evaluation {self.id}>'


class Groupe(db.Model):
    __tablename__ = 'Groupes'
    id = db.Column('Id', db.Integer, primary_key=True)
    groupe_name = db.Column('GroupeName', db.String(250), nullable=False)
    teacher_id = db.Column('TeacherId', db.Text, nullable=False)
    course_id = db.Column('CourseId', db.Integer, db.ForeignKey('Courses.Id'), nullable=False)
    course_level_id = db.Column('CourseLevelId', db.Integer, db.ForeignKey('CourseLevels.Id'), nullable=False)
    current_session_id = db.Column('CurrentSessionId', db.Integer, db.ForeignKey('Sessions.Id'))
    nbr_places = db.Column('NbrPlaces', db.Integer, nullable=False)
    description = db.Column('Description', db.Text, nullable=False, default='')

    current_session = db.relationship('Session', backref='groupes', lazy=True)
    registrations = db.relationship('CourseRegistration', backref='groupe', lazy=True)

    def __repr__(self):
        return f'<Groupe {self.groupe_name}>'


class AppParameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<AppParameter {self.key}={self.value}>'

    @staticmethod
    def get(key, default=None):
        param = AppParameter.query.filter_by(key=key).first()
        return param.value if param else default

    @staticmethod
    def set(key, value, description=None):
        param = AppParameter.query.filter_by(key=key).first()
        if param:
            param.value = value
            if description is not None:
                param.description = description
        else:
            param = AppParameter(key=key, value=value, description=description)
            db.session.add(param)
        db.session.commit()
        return param
