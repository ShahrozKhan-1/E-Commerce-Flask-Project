from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, TextAreaField, FileField, SelectField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional
from flask_wtf.file import FileRequired, FileAllowed



class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=50), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Submit")
    
    
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(max=50), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Submit")  
    
    
def validate_image_count(form, field):
    if len(field.data) > 5:
        raise ValidationError('You can upload maximum 5 images')
    if len(field.data) < 1:
        raise ValidationError('At least one image is required')

class AddProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()],  render_kw={"min": 0})
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()])
    brand = StringField('Product Brand', validators=[DataRequired()])
    images = MultipleFileField(
        'Product Images',
        validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')],
        render_kw={"multiple": True}
    )
    add_product = SubmitField('Add Product')
    
class EditProduct(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()],  render_kw={"min": 0})  
    category = SelectField('Category', coerce=int, validators=[DataRequired()])  # Add coerce=int
    brand = StringField('Brand', validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    images = MultipleFileField('Images', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    edit_product = SubmitField("Update")

class OrderDetail(FlaskForm):
    contact = StringField("Contact Number", validators=[DataRequired()])
    address = StringField("Delivery Address", validators=[DataRequired()])
    message = TextAreaField("Special Instructions (Optional)")
    submit = SubmitField("Place Order")
    
class UpdateAccount(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional()])
    confirm_password = PasswordField('Confirm Password', validators=[Optional()])