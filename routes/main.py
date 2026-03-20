from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import Course, CourseLevel, CourseRegistration, State, Municipality, Profession, Session, AppParameter, CourseFee
from forms import CourseRegistrationForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    active_courses = Course.query.filter_by(is_active=True).order_by(Course.order).all()
    registration_opened = AppParameter.get('registration_opened', 'false').lower() == 'true'
    return render_template('home.html', courses=active_courses, registration_opened=registration_opened)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.filter_by(is_active=True).order_by(Course.order).all()
    registration_opened = AppParameter.get('registration_opened', 'false').lower() == 'true'
    return render_template('dashboard.html', courses=courses, registration_opened=registration_opened)


@main_bp.route('/register-course', methods=['GET', 'POST'])
@login_required
def register_course():
    registration_opened = AppParameter.get('registration_opened', 'false').lower() == 'true'
    if not registration_opened:
        flash('Registration is currently closed.', 'warning')
        return redirect(url_for('main.dashboard'))

    form = CourseRegistrationForm()

    # Populate select choices
    active_courses = Course.query.filter_by(is_active=True).order_by(Course.order).all()
    form.course_id.choices = [(0, '— Select Course —')] + [(c.id, c.name) for c in active_courses]
    form.birth_state_id.choices = [('', '— Select State —')] + [(s.id, s.name) for s in State.query.order_by(State.id).all()]
    form.birth_municipality_id.choices = [(0, '— Select Municipality —')]
    form.profession_id.choices = [(0, '— None —')] + [(p.id, p.name) for p in Profession.query.order_by(Profession.name).all()]
    form.course_level_id.choices = [(0, '— Select Level —')]
    form.session_id.choices = [(0, '— None —')]

    # Current session
    current_session_param = AppParameter.get('current_session')
    current_session = None
    if current_session_param:
        current_session = Session.query.get(int(current_session_param))
    if current_session:
        form.session_id.choices = [(current_session.id, current_session.session_name)]
        form.session_id.data = current_session.id

    # Pre-select course from query param
    if request.method == 'GET' and request.args.get('course_id'):
        try:
            course_id_param = int(request.args.get('course_id'))
            form.course_id.data = course_id_param
            levels = CourseLevel.query.filter_by(course_id=course_id_param, is_active=True).order_by(CourseLevel.level_order).all()
            form.course_level_id.choices = [(0, '— Select Level —')] + [(l.id, l.name) for l in levels]
        except (ValueError, TypeError):
            pass

    # Repopulate dependent selects on POST
    if request.method == 'POST':
        if form.birth_state_id.data:
            municipalities = Municipality.query.filter_by(state_id=form.birth_state_id.data).order_by(Municipality.name).all()
            form.birth_municipality_id.choices = [(0, '— Select Municipality —')] + [(m.id, m.name) for m in municipalities]
        if form.course_id.data and int(form.course_id.data) > 0:
            levels = CourseLevel.query.filter_by(course_id=int(form.course_id.data), is_active=True).order_by(CourseLevel.level_order).all()
            form.course_level_id.choices = [(0, '— Select Level —')] + [(l.id, l.name) for l in levels]

    if form.validate_on_submit():
        course_id = form.course_id.data
        if course_id == 0:
            flash('Please select a course.', 'danger')
            return render_template('course_registration_form.html', form=form, title='Course Registration')

        # Determine fee_value from CourseFee or Profession default
        fee_value = 0
        profession_id = form.profession_id.data if form.profession_id.data != 0 else None
        if profession_id:
            course_fee = CourseFee.query.filter_by(course_id=course_id, profession_id=profession_id).first()
            if course_fee:
                fee_value = course_fee.fee_value
            else:
                profession = Profession.query.get(profession_id)
                if profession:
                    fee_value = profession.fee_value

        # Generate inscription code
        year = datetime.utcnow().strftime('%Y')
        last_reg = CourseRegistration.query.filter(
            CourseRegistration.inscription_code.like(f'{year}-%')
        ).order_by(CourseRegistration.id.desc()).first()
        if last_reg:
            last_num = int(last_reg.inscription_code.split('-')[1])
            inscription_code = f'{year}-{last_num + 1:05d}'
        else:
            inscription_code = f'{year}-00001'

        registration = CourseRegistration(
            user_id=current_user.id,
            inscription_code=inscription_code,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            first_name_ar=form.first_name_ar.data,
            last_name_ar=form.last_name_ar.data,
            birth_date=datetime.combine(form.birth_date.data, datetime.min.time()),
            birth_state_id=form.birth_state_id.data,
            birth_municipality_id=form.birth_municipality_id.data,
            address=form.address.data,
            tel=form.tel.data,
            profession_id=profession_id,
            course_id=course_id,
            course_level_id=form.course_level_id.data if form.course_level_id.data != 0 else None,
            session_id=form.session_id.data if form.session_id.data != 0 else None,
            registration_date=datetime.utcnow(),
            notes=None,
            fee_value=fee_value,
            paid_fee_value=0,
            is_reregistration=form.is_reregistration.data,
            registration_terms_accepted=form.registration_terms_accepted.data,
            registration_validated=False,
            group_id=None
        )
        db.session.add(registration)
        db.session.commit()
        flash(f'Registration submitted successfully! Your code is {inscription_code}.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('course_registration_form.html', form=form, title='Course Registration')


@main_bp.route('/api/municipalities/<state_id>')
@login_required
def api_municipalities(state_id):
    municipalities = Municipality.query.filter_by(state_id=state_id).order_by(Municipality.name).all()
    return jsonify([{'id': m.id, 'name': m.name} for m in municipalities])


@main_bp.route('/api/course-levels/<int:course_id>')
@login_required
def api_course_levels(course_id):
    levels = CourseLevel.query.filter_by(course_id=course_id, is_active=True).order_by(CourseLevel.level_order).all()
    return jsonify([{'id': l.id, 'name': l.name} for l in levels])
