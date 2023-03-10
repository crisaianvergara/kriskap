from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class ChangePasswordForm(FlaskForm):
    """
    This class is used to change the password of a user.

    Fields:
    - new_password: A password field for the user's new password.
    - confirm_password: A password field for confirming the user's new password.
    - submit: A submit field for submitting the form.
    """

    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Change Password")
