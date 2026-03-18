from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from extensions import db, bcrypt
from models import User, Session, AppParameter, State, Municipality, Profession, CourseFee, Course
from forms import CreateUserForm, EditUserForm, SessionForm, StateForm, MunicipalityForm, ProfessionForm, CourseFeeForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/professions')
@admin_required
def professions():
    all_professions = Profession.query.order_by(Profession.name).all()
    return render_template('admin/professions.html', professions=all_professions)


@admin_bp.route('/professions/create', methods=['GET', 'POST'])
@admin_required
def create_profession():
    form = ProfessionForm()
    if form.validate_on_submit():
        profession = Profession(
            name=form.name.data,
            name_ar=form.name_ar.data,
            fee_value=form.fee_value.data
        )
        db.session.add(profession)
        db.session.commit()
        flash('Profession created successfully.', 'success')
        return redirect(url_for('admin.professions'))
    return render_template('admin/profession_form.html', form=form, title='Create Profession')


@admin_bp.route('/professions/<int:profession_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_profession(profession_id):
    profession = Profession.query.get_or_404(profession_id)
    form = ProfessionForm(obj=profession)
    if form.validate_on_submit():
        profession.name = form.name.data
        profession.name_ar = form.name_ar.data
        profession.fee_value = form.fee_value.data
        db.session.commit()
        flash('Profession updated successfully.', 'success')
        return redirect(url_for('admin.professions'))
    return render_template('admin/profession_form.html', form=form, title='Edit Profession')


@admin_bp.route('/professions/<int:profession_id>/delete', methods=['POST'])
@admin_required
def delete_profession(profession_id):
    profession = Profession.query.get_or_404(profession_id)
    # Check if used in registrations or course fees
    if profession.course_fees or profession.registrations:
        flash('Cannot delete profession as it is linked to other records.', 'danger')
        return redirect(url_for('admin.professions'))
    db.session.delete(profession)
    db.session.commit()
    flash('Profession deleted.', 'success')
    return redirect(url_for('admin.professions'))


@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form, title='Create User')


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        # Check uniqueness for username/email if changed
        if form.username.data != user.username:
            existing = User.query.filter_by(username=form.username.data).first()
            if existing:
                flash('Username already taken.', 'danger')
                return render_template('admin/user_form.html', form=form, title='Edit User')
        if form.email.data != user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash('Email already registered.', 'danger')
                return render_template('admin/user_form.html', form=form, title='Edit User')
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form, title='Edit User')


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/sessions')
@admin_required
def sessions():
    all_sessions = Session.query.order_by(Session.start_date.desc()).all()
    return render_template('admin/sessions.html', sessions=all_sessions)


@admin_bp.route('/sessions/create', methods=['GET', 'POST'])
@admin_required
def create_session():
    form = SessionForm()
    if form.validate_on_submit():
        existing = Session.query.filter_by(session_code=form.session_code.data).first()
        if existing:
            flash('Session code already exists.', 'danger')
            return render_template('admin/session_form.html', form=form, title='Create Session')
        session = Session(
            session_code=form.session_code.data,
            session_name=form.session_name.data,
            session_name_ar=form.session_name_ar.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(session)
        db.session.commit()
        flash('Session created successfully.', 'success')
        return redirect(url_for('admin.sessions'))
    return render_template('admin/session_form.html', form=form, title='Create Session')


@admin_bp.route('/sessions/<int:session_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_session(session_id):
    session = Session.query.get_or_404(session_id)
    form = SessionForm(obj=session)
    if form.validate_on_submit():
        if form.session_code.data != session.session_code:
            existing = Session.query.filter_by(session_code=form.session_code.data).first()
            if existing:
                flash('Session code already exists.', 'danger')
                return render_template('admin/session_form.html', form=form, title='Edit Session')
        session.session_code = form.session_code.data
        session.session_name = form.session_name.data
        session.session_name_ar = form.session_name_ar.data
        session.start_date = form.start_date.data
        session.end_date = form.end_date.data
        db.session.commit()
        flash('Session updated successfully.', 'success')
        return redirect(url_for('admin.sessions'))
    return render_template('admin/session_form.html', form=form, title='Edit Session')


@admin_bp.route('/sessions/<int:session_id>/delete', methods=['POST'])
@admin_required
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    db.session.delete(session)
    db.session.commit()
    flash('Session deleted.', 'success')
    return redirect(url_for('admin.sessions'))


@admin_bp.route('/states')
@admin_required
def states():
    all_states = State.query.order_by(State.id).all()
    return render_template('admin/states.html', states=all_states)


@admin_bp.route('/states/create', methods=['GET', 'POST'])
@admin_required
def create_state():
    form = StateForm()
    if form.validate_on_submit():
        existing = State.query.get(form.id.data)
        if existing:
            flash('State code already exists.', 'danger')
            return render_template('admin/state_form.html', form=form, title='Create State', state=None, municipalities=[])
        state = State(id=form.id.data, name=form.name.data, name_ar=form.name_ar.data)
        db.session.add(state)
        db.session.commit()
        flash('State created successfully.', 'success')
        return redirect(url_for('admin.edit_state', state_id=state.id))
    return render_template('admin/state_form.html', form=form, title='Create State', state=None, municipalities=[])


@admin_bp.route('/states/<string:state_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_state(state_id):
    state = State.query.get_or_404(state_id)
    form = StateForm(obj=state)
    if form.validate_on_submit():
        if form.id.data != state.id:
            existing = State.query.get(form.id.data)
            if existing:
                flash('State code already exists.', 'danger')
                return render_template('admin/state_form.html', form=form, title='Edit State', state=state, municipalities=state.municipalities)
            state.id = form.id.data
        state.name = form.name.data
        state.name_ar = form.name_ar.data
        db.session.commit()
        flash('State updated successfully.', 'success')
        return redirect(url_for('admin.edit_state', state_id=state.id))
    municipalities = Municipality.query.filter_by(state_id=state_id).order_by(Municipality.id).all()
    return render_template('admin/state_form.html', form=form, title='Edit State', state=state, municipalities=municipalities)


@admin_bp.route('/states/<string:state_id>/delete', methods=['POST'])
@admin_required
def delete_state(state_id):
    state = State.query.get_or_404(state_id)
    if state.municipalities:
        flash('Cannot delete state with municipalities. Remove them first.', 'danger')
        return redirect(url_for('admin.edit_state', state_id=state_id))
    db.session.delete(state)
    db.session.commit()
    flash('State deleted.', 'success')
    return redirect(url_for('admin.states'))


@admin_bp.route('/states/<string:state_id>/municipalities/create', methods=['GET', 'POST'])
@admin_required
def create_municipality(state_id):
    state = State.query.get_or_404(state_id)
    form = MunicipalityForm()
    if form.validate_on_submit():
        municipality = Municipality(name=form.name.data, name_ar=form.name_ar.data, state_id=state.id)
        db.session.add(municipality)
        db.session.commit()
        flash('Municipality created successfully.', 'success')
        return redirect(url_for('admin.edit_state', state_id=state.id))
    return render_template('admin/municipality_form.html', form=form, title='Create Municipality', state=state)


@admin_bp.route('/states/<string:state_id>/municipalities/<int:municipality_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_municipality(state_id, municipality_id):
    state = State.query.get_or_404(state_id)
    municipality = Municipality.query.get_or_404(municipality_id)
    form = MunicipalityForm(obj=municipality)
    if form.validate_on_submit():
        municipality.name = form.name.data
        municipality.name_ar = form.name_ar.data
        db.session.commit()
        flash('Municipality updated successfully.', 'success')
        return redirect(url_for('admin.edit_state', state_id=state.id))
    return render_template('admin/municipality_form.html', form=form, title='Edit Municipality', state=state)


@admin_bp.route('/states/<string:state_id>/municipalities/<int:municipality_id>/delete', methods=['POST'])
@admin_required
def delete_municipality(state_id, municipality_id):
    State.query.get_or_404(state_id)
    municipality = Municipality.query.get_or_404(municipality_id)
    db.session.delete(municipality)
    db.session.commit()
    flash('Municipality deleted.', 'success')
    return redirect(url_for('admin.edit_state', state_id=state_id))


@admin_bp.route('/course-fees')
@admin_required
def course_fees():
    all_fees = CourseFee.query.all()
    return render_template('admin/course_fees.html', course_fees=all_fees)


@admin_bp.route('/course-fees/create', methods=['GET', 'POST'])
@admin_required
def create_course_fee():
    form = CourseFeeForm()
    form.profession_id.choices = [(p.id, p.name) for p in Profession.query.order_by(Profession.name).all()]
    form.course_id.choices = [(c.id, c.name) for c in Course.query.order_by(Course.name).all()]
    if form.validate_on_submit():
        course_fee = CourseFee(
            profession_id=form.profession_id.data,
            course_id=form.course_id.data,
            fee_value=form.fee_value.data
        )
        db.session.add(course_fee)
        db.session.commit()
        flash('Course fee created successfully.', 'success')
        return redirect(url_for('admin.course_fees'))
    return render_template('admin/course_fee_form.html', form=form, title='Create Course Fee')


@admin_bp.route('/course-fees/<int:course_fee_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course_fee(course_fee_id):
    course_fee = CourseFee.query.get_or_404(course_fee_id)
    form = CourseFeeForm(obj=course_fee)
    form.profession_id.choices = [(p.id, p.name) for p in Profession.query.order_by(Profession.name).all()]
    form.course_id.choices = [(c.id, c.name) for c in Course.query.order_by(Course.name).all()]
    if form.validate_on_submit():
        course_fee.profession_id = form.profession_id.data
        course_fee.course_id = form.course_id.data
        course_fee.fee_value = form.fee_value.data
        db.session.commit()
        flash('Course fee updated successfully.', 'success')
        return redirect(url_for('admin.course_fees'))
    return render_template('admin/course_fee_form.html', form=form, title='Edit Course Fee')


@admin_bp.route('/course-fees/<int:course_fee_id>/delete', methods=['POST'])
@admin_required
def delete_course_fee(course_fee_id):
    course_fee = CourseFee.query.get_or_404(course_fee_id)
    db.session.delete(course_fee)
    db.session.commit()
    flash('Course fee deleted.', 'success')
    return redirect(url_for('admin.course_fees'))


@admin_bp.route('/parameters', methods=['GET', 'POST'])
@admin_required
def parameters():
    if request.method == 'POST':
        params = AppParameter.query.all()
        for param in params:
            new_value = request.form.get(f'param_{param.id}', '')
            param.value = new_value
        db.session.commit()
        flash('Parameters updated successfully.', 'success')
        return redirect(url_for('admin.parameters'))
    all_params = AppParameter.query.order_by(AppParameter.key).all()
    groups = {}
    group_labels = {
        'smtp': ('Email / SMTP', 'bi-envelope'),
        'contact': ('Contact Info', 'bi-info-circle'),
    }
    default_group = ('General', 'bi-gear')
    for param in all_params:
        prefix = param.key.split('_')[0]
        if prefix in group_labels:
            group_key = prefix
        else:
            group_key = '_general'
        groups.setdefault(group_key, []).append(param)
    grouped = []
    if '_general' in groups:
        label, icon = default_group
        grouped.append({'key': '_general', 'label': label, 'icon': icon, 'params': groups.pop('_general')})
    for key, params in groups.items():
        label, icon = group_labels.get(key, default_group)
        grouped.append({'key': key, 'label': label, 'icon': icon, 'params': params})
    all_sessions = Session.query.order_by(Session.start_date.desc()).all()
    return render_template('admin/parameters.html', grouped=grouped, sessions=all_sessions)
