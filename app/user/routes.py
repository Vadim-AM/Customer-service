import time
from datetime import datetime

from flask import url_for, session, flash, request, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import db
from app.models import User, Service
from app.sms import send_sms
from app.user import bp
from app.user.forms import Services, SMSForm, EditProfileForm


@bp.route('/<username>', methods=['GET', 'POST'])
@bp.route('/')
@login_required
def user(username):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.register'))
    form = Services()
    user = User.query.filter_by(username=username).first()
    date = datetime.now().date()  # hide old records
    services = Service.query.filter_by(user_id=user.id)
    profile_form = EditProfileForm(current_user.username, current_user.phone_number)
    if profile_form.validate_on_submit():  # edit profile
        session['username'] = profile_form.username.data
        session['phone_number'] = profile_form.phone_number.data
        session['code'] = send_sms(session['phone_number'])
        flash(f"Your code is {session['code']}")
        return redirect(url_for('user_blueprint.edit_sms'))
    elif request.method == 'GET':
        profile_form.username.data = current_user.username
        profile_form.phone_number.data = current_user.phone_number
    return render_template('user/user.html', user=user, title=username, form=form, profile_form=profile_form,
                           services=services, date=date)


@bp.route('/edit_sms', methods=['GET', 'POST'])
def edit_sms():
    sms_form = SMSForm()
    current_user.username = session['username']
    current_user.phone_number = session['phone_number']
    current_user.set_password(session['phone_number'])
    if request.method == 'POST':
        if request.form['sms'] == 'Register' and sms_form.validate():
            data = sms_form.code_input.data
            if session['code'] == data:
                db.session.commit()
                flash(f'Values has been changed')
                time.sleep(1)
                return redirect(url_for('user_blueprint.user', username=current_user.username))
            flash('Invalid code. Please try again')
            return render_template('sms.html', sms_form=sms_form)
        elif request.form['sms'] == 'Send SMS':  # TODO change SMS timer value and enable service
            session['code'] = send_sms(session['phone_number'])
            flash(f"Your code is {session['code']}")  # TODO don't forget to disable
            return render_template('sms.html', sms_form=sms_form)
    return render_template('sms.html', sms_form=sms_form)


@bp.route('/add_service', methods=['POST'])
@login_required
def add_service():
    form = Services()
    if form.validate_on_submit():
        service_add = Service(service1=form.service1.data, service2=form.service2.data,
                              service3=form.service3.data,
                              service_date=form.service_date.data,
                              service_time=form.service_time.data, user_id=current_user.id)
        db.session.add(service_add)
        db.session.commit()
        flash(f'Congratulations, {current_user.username} you are registered for service at {service_add.service_time}!')
        time.sleep(1)
        return redirect(url_for('user_blueprint.user', username=current_user.username))
    flash('This date or time are already in use. Please choose another date or time.')
    return redirect(url_for('user_blueprint.user', username=current_user.username))


@bp.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id=None):
    if service_id is not None:
        service = Service.query.filter_by(id=service_id).first()
        form = Services()
        if form.validate_on_submit():
            service.service1 = form.service1.data
            service.service2 = form.service2.data
            service.service3 = form.service3.data
            service.service_date = form.service_date.data
            service.service_time = form.service_time.data
            db.session.commit()
            flash(
                f'Ok, {current_user.username} you have changed your service to on {service.service_date} at {service.service_time}!')
            time.sleep(0.5)
            return redirect(url_for('user_blueprint.user', username=current_user.username))
        flash('This date or time are already in use. Please choose another date or time.')
    return redirect(url_for('user_blueprint.user', username=current_user.username))


@bp.route('/user/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    service_del = Service.query.get_or_404(service_id)
    db.session.delete(service_del)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('user_blueprint.user', username=current_user.username))
