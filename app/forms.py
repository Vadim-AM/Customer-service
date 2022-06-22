from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateField, TelField, RadioField
from wtforms.validators import ValidationError, Length, InputRequired, Regexp

from app.models import User, Service


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(),
        Length(3, 20, message="Please provide a valid name"),
        Regexp("^[A-Za-z][A-Za-z0-9_ .]*$", 0,
               "Usernames must have only letters, " "numbers, "
               "dots or underscores")])
    phone_number = TelField('Phone number', validators=[InputRequired(), Length(10, 12),
                                                        Regexp(r"^\+(?:[0-9]●?){6,14}[0-9]$",
                                                               message="Enter a valid phone number, like +55 555 "
                                                                       "555 555")])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(),
                                       Length(3, 20, message="Please provide a valid name"),
                                       Regexp("^[A-Za-z][A-Za-z0-9_ .]*$", 0,
                                              "Usernames must have only letters, " "numbers, dots or underscores")])
    phone_number = TelField(validators=[InputRequired(), Length(10, 12),
                                        Regexp(r"^\+(?:[0-9]●?){6,14}[0-9]$",
                                               message="Enter a valid phone number, like +55555555555")])
    confirm = SubmitField('Send SMS code')

    @staticmethod
    def validate_username(self, username):  # if already exist
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    @staticmethod
    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user is not None:
            raise ValidationError('Phone number already in use.')


class SMSForm(FlaskForm):
    code_input = StringField(validators=[Length(4, 4)])
    register = SubmitField('Confirm')


class EditProfileForm(FlaskForm):
    username = StringField(validators=[InputRequired(),
                                       Length(3, 20, message="Please provide a valid name"),
                                       Regexp("^[A-Za-z][A-Za-z0-9_ .]*$", 0,
                                              "Usernames must have only letters, " "numbers, "
                                              "dots or underscores")])
    phone_number = TelField(validators=[InputRequired(), Length(10, 12),
                                        Regexp(r"^\+(?:[0-9]●?){6,14}[0-9]$",
                                               message="Enter a valid phone number, like +55"
                                                       "555555555")])
    submit = SubmitField('Confirm')

    def __init__(self, original_username, original_phone_number, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_phone_number = original_phone_number

    def validate_username(self, username):  # if already exist
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_phone_number(self, phone_number):
        if phone_number.data != self.original_phone_number:
            user = User.query.filter_by(phone_number=self.phone_number.data).first()
            if user is not None:
                raise ValidationError('Phone number already in use.')


class Reviews(FlaskForm):
    text = TextAreaField('Enter your text here:', validators=[InputRequired(), Length(min=2, max=300)])
    rating = RadioField('Rating', validators=[InputRequired()],
                        choices=['Terrible!', 'Bad', 'So-so', 'Good', 'Awesome!'])
    send_review = SubmitField('Confirm')


def validate_date_time(form, service_time):
    date_services = Service.query.filter_by(service_date=form.service_date.data).all()
    for service in date_services:
        user = service.client.username
        if service.service_time == service_time.data and user != current_user.username:  # for changing self-services
            raise ValidationError('Please choose a different time.')


class Services(FlaskForm):
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


