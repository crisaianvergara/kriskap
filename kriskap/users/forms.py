from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from kriskap.models import User


# WTForms
class RegistrationForm(FlaskForm):
    """
    This class defines the registration form.

    Fields:
    - username: A string field for the user's username.
    - name: A string field for the user's name.
    - email: A string field for the user's email address.
    - password: A password field for the user's password.
    - confirm_password: A password field for confirming the user's password.
    - submit: A submit field for submitting the form.
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=20)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=5)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """
        Validate that the username does not already exist in the database.

        Parameters:
        - username: The username to check.

        Raises:
        - ValidationError: If the username already exists in the database.
        """

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        """
        Validate that the email address does not already exist in the database.

        Parameters:
        - email: The email to check.

        Raises:
        - ValidationError: If the email address already exists in the database.
        """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    """
    This class defines the login form.

    Fields:
    - email: A string field for the user's email address.
    - password: A password field for the user's password.
    - remember: A boolean field for remembering the user's login.
    - submit: A submit field for submitting the form.
    """

    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class UpdateAccountForm(FlaskForm):
    """
    This class defines the update account form.

    Fields:
    - username: A string field for the user's new username.
    - name: A string field for the user's new name.
    - email: A string field for the user's new email address.
    - image_f: A file field for the user's new image.
    - submit: A submit field for submitting the form.
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=20)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=5)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    image_f = FileField(
        "Select Image", validators=[FileAllowed(["jpg", "png", "jpeg", "webp"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        """
        Validate that the username does not already exist in the database, unless it is the same as the current user's username.

        Parameters:
        - username: The username to check.

        Raises:
        - ValidationError: If the username already exists in the database and is not the same as the current user's username.
        """

        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        """
        Validate that the email address does not already exist in the database, unless it is the same as the current user's email address.

        Parameters:
        - email: The email to check.

        Raises:
        - ValidationError: If the email address already exists in the database and is not the same as the current user's email address.
        """
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


class RequestResetForm(FlaskForm):
    """
    This class defines the request reset password form.

    Fields:
    - email: A string field for the user's email address.
    - submit: A submit field for submitting the form.
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """
        Validate that the email address exists in the database.

        Parameters:
        -email: The email to check.

        Raises:
        - ValidationError: If the email address does not exist in the database.
        """

        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email. You must register first."
            )


class ResetPasswordForm(FlaskForm):
    """
    This class defines the reset password form.

    Fields:
    - password: A password field for the user's new password.
    - confirm_password: A password field for confirming the user's new password.
    - submit: A submit field for submitting the form.

    When the form is submitted, the password and confirm_password fields are validated to ensure that the passwords match and meet the minimum requirement. If the fields are valid, the user's password is updated in the database.
    """

    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
