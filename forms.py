from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, IntegerField, RadioField, SelectField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, length, equal_to
from flask_wtf.file import FileField


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(message="Product name is required")])
    price = IntegerField('Price', validators=[DataRequired(message="Product price is required")])
    description = TextAreaField('Description', validators=[DataRequired(message="Product description is required")])
    image_url = FileField('Product Image', validators=[DataRequired(message="Product image is required")])
    quantity = IntegerField('Product Quantity', validators=[DataRequired(message="Product quantity is required")])
    brand = SelectField('Product Brand', choices=[
    ('tiffany', 'Tiffany & Co.'),
    ('cartier', 'Cartier'),
    ('bulgari', 'Bvlgari'),
    ('van_cleef', 'Van Cleef & Arpels'),
    ('chopard', 'Chopard'),
    ('harry_winston', 'Harry Winston'),
    ('graff', 'Graff'),
    ('boucheron', 'Boucheron'),
    ('piaget', 'Piaget'),
    ('damiani', 'Damiani'),
    ('mikimoto', 'Mikimoto'),
    ('de_beers', 'De Beers'),
    ('swarovski', 'Swarovski'),
    ('chaumet', 'Chaumet'),
    ('blue_nile', 'Blue Nile'),
    ('antonini', 'Antonini'),
    ('messika', 'Messika'),
    ('ileana_iscovici', 'Ileana Iscovici'),
    ('louis_vuitton', 'Louis Vuitton Jewelry'),
    ('gucci', 'Gucci Jewelry'),
    ('prada', 'Prada Jewelry'),
    ('monica_viner', 'Monica Vinader'),
    ('tacori', 'Tacori'),
    ('pandora', 'Pandora')],
                        validators=[DataRequired(message="Product brand is required")])
    material = SelectField('Product Material',choices = [
    ('Gold', 'Gold'),
    ('Silver', 'Silver'),
    ('Platinum', 'Platinum'),
    ('Copper', 'Copper'),
    ('Iron', 'Iron'),
    ('Aluminum', 'Aluminum'),
    ('Bronze', 'Bronze'),
    ('Titanium', 'Titanium'),
    ('Steel', 'Steel'),
    ('Nickel', 'Nickel'),
    ('Lead', 'Lead'),
    ('Zinc', 'Zinc'),
    ('Brass', 'Brass'),
    ('Palladium', 'Palladium'),
    ('Rhodium', 'Rhodium'),
    ('Diamond', 'Diamond'),
    ('Quartz', 'Quartz'),
    ('Wood', 'Wood'),
    ('Plastic', 'Plastic'),
    ('Glass', 'Glass'),
    ('Carbon Fiber', 'Carbon Fiber')
],
                           validators=[DataRequired(message="Product material is required")])
    category = SelectField('Category', choices=[('Earrings', 'Earrings'),
                                                ('Rings', 'Rings'),
                                                ('Bracelets', 'Bracelets'),
                                                ('Watches', 'Watches'),
                                                ('Brooches', 'Brooches'),
                                                ('Gift', 'Gift')],
                           validators=[DataRequired(message="Product category is required")])
    submit = SubmitField("Create")



class RegisterForm(FlaskForm):
    user_image = FileField("Your Image", validators=[DataRequired(message="User image is required")])
    firstname = StringField("First Name", validators=[DataRequired(message="First name is required")])
    lastname = StringField("Last Name", validators=[DataRequired(message="Last name is required")])
    email = EmailField("Email", validators=[DataRequired(message="Email is required")])
    phone_number = IntegerField("Phone Number", validators=[DataRequired(message="Phone number is required")])
    gender = RadioField("Gender", choices=["Male", "Female", "Other"],
                        validators=[DataRequired(message="Gender is required")])
    country = SelectField("Country", choices=[
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('GB', 'United Kingdom'),
        ('IN', 'India'),
        ('AU', 'Australia'),
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('BR', 'Brazil'),
        ('MX', 'Mexico'),
        ('JP', 'Japan'),
        ('CN', 'China'),
        ('IT', 'Italy'),
        ('ES', 'Spain'),
        ('RU', 'Russia'),
        ('KR', 'South Korea'),
        ('ZA', 'South Africa'),
        ('NG', 'Nigeria'),
        ('AR', 'Argentina'),
        ('SE', 'Sweden'),
        ('NO', 'Norway'),
        ('FI', 'Finland'),
        ('SG', 'Singapore')
    ], validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=8, max=20,
                                                                            message="Password must be between 8 and 20 characters")])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), length(min=8, max=20,
                                                                                          message="Password must be between 8 and 20 characters"),
                                                                   equal_to("password",
                                                                            message="Passwords must match")])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message="Email is required")])
    password = PasswordField("Password", validators=[DataRequired(message="Password is required"), length(min=8, max=20,
                                                                                                          message="Password must be between 8 and 20 characters")])
    submit = SubmitField("Sign In")

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField("Add Comment")

class TestimonialForm(FlaskForm):
    content = TextAreaField('Testimonial Content', validators=[DataRequired()])
    submit = SubmitField('Add Testimonial')


class GiftCardForm(FlaskForm):
    amount = SelectField(
        'Choose Amount:',
        choices=[
            ('10', '$10'),
            ('25', '$25'),
            ('50', '$50'),
            ('100', '$100'),
            ('200', '$200'),
            ('500', '$500'),
            ('1000', '$1000'),
            ('5000', '$5000')
        ],
    validators=[DataRequired(message="Please select a gift card amount.")]
    )
    message = TextAreaField(
        'Personalized Message:',
        validators=[DataRequired(message="Please enter a message for the recipient.")]
    )
    email = EmailField(
        'Recipient\'s Email:',
        validators=[DataRequired(message="Please provide a recipient's email address.")]
    )
    submit = SubmitField('Create Gift Card')

class CheckoutForm(FlaskForm):
    address = StringField('Shipping Address', validators=[DataRequired(message="Please provide your address.")])
    city = StringField('City', validators=[DataRequired(message="Please provide your city.")])
    zip_code = StringField('Zip Code', validators=[DataRequired(message="Enter zip-code.")])
    card_number = StringField('Card Number', validators=[DataRequired(message="Card number is required"), length(min=11, max=16, message="Card number must be between 11 and 16 characters")])
    cvv = StringField('CVV', validators=[DataRequired()])
    submit = SubmitField('Complete Purchase')