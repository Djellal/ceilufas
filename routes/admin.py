from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from extensions import db
from models import User, Session, AppParameter
from forms import EditUserForm, SessionForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


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
                return render_template('admin/edit_user.html', form=form, user=user)
        if form.email.data != user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash('Email already registered.', 'danger')
                return render_template('admin/edit_user.html', form=form, user=user)
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)


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
    return render_template('admin/parameters.html', parameters=all_params)
