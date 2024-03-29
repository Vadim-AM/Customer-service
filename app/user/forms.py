"""Module contains Profile and Service forms"""
from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField, SelectField, DateField
from wtforms.validators import Length, InputRequired, Regexp, ValidationError

from app.models import User, Service


class SMSForm(FlaskForm):
    """Contains an SMS form fields"""
    code_input = StringField(validators=[Length(4, 4)])
    register = SubmitField('Confirm')


class EditProfileForm(FlaskForm):
    """Contains a Profile form fields with validation methods"""
    username = StringField(validators=[InputRequired(),
                                       Length(3, 60, message="Please provide a valid name"),
                                       Regexp("^[A-Za-z][A-Za-z0-9_ .]*$", 0,
                                              "Usernames must have only letters,numbers, dots or underscores")])
    phone_number = TelField(validators=[InputRequired(), Length(10, 12),
                                        Regexp(r"^\+(?:[0-9]●?){10,12}[0-9]$",
                                               message="Enter a valid phone number like +55555555555")])
    submit = SubmitField('Confirm')

    def __init__(self, original_username, original_phone_number, **kwargs):
        super().__init__(**kwargs)
        self.original_username = original_username
        self.original_phone_number = original_phone_number

    def validate_username(self, username):
        """Checks if username already exists in DB"""
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_phone_number(self, phone_number):
        """Checks if Phone number already exists in DB"""
        if phone_number.data != self.original_phone_number:
            user = User.query.filter_by(phone_number=self.phone_number.data).first()
            if user is not None:
                raise ValidationError('Phone number already in use.')


def validate_date_time(form, service_time):
    """Checks if username already exists in DB"""
    date_services = Service.query.filter_by(service_date=form.service_date.data).all()
    for service in date_services:
        user = service.app.username
        if service.service_time == service_time.data and user != current_user.username:
            raise ValidationError('Please choose a different time.')


class Services(FlaskForm):
    """Contains a Services fields with its validators"""
    service1 = SelectField('Choose service:', choices=['Big-mak', 'Chicken Burger', 'Cheeseburger'],
                           render_kw={'placeholder': '12341'})
    service2 = SelectField('Choose additional service:', choices=['', 'Coke-cola', 'Pepsi', 'Fanta'],
                           validate_choice=False)
    service3 = SelectField('Choose another additional service:', choices=['', 'At the place', 'To Go', 'Delivery'],
                           validate_choice=False)
    service_date = DateField('Choose the date', validators=[InputRequired()],
                             format='%Y-%m-%d', render_kw={"min": datetime.now().date()})
    service_time = SelectField('Choose the time', choices=['10:00', '12:00', '14:00', '16:00', '18:00'],
                               validators=[InputRequired(),
                                           validate_date_time])
    submit = SubmitField('Confirm', render_kw={'class': 'btn btn-info'})
