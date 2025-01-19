import os.path

from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
from models import GiftCard
from ext import app, db
from forms import ProductForm, LoginForm, RegisterForm, CommentForm, TestimonialForm, GiftCardForm, CheckoutForm
from models import Product, User, Comment, Wishlist, Testimonial, Cart
from flask import flash
from utils import admin_required, no_admin_required


@app.route("/")
def home():
    testimonials = Testimonial.query.filter_by(is_approved=True).all()
    return render_template("index.html", testimonials=testimonials)


@app.route('/gift-card', methods=['GET', 'POST'])
@login_required
@no_admin_required
def gift_card():
    gift_card_form = GiftCardForm()
    if request.method == 'POST' and gift_card_form.validate_on_submit():
        amount = gift_card_form.amount.data
        message = gift_card_form.message.data
        recipient_email = gift_card_form.email.data
        gift_card_code = generate_gift_card_code()
        recipient = User.query.filter_by(email=recipient_email).first()
        gift_card = GiftCard(
            user_id=current_user.id,
            amount=amount,
            message=message,
            recipient_email=recipient_email,
            code=gift_card_code
        )
        if recipient:
            gift_card.recipient_user_id = recipient.id
            gift_card.save()
            flash(f'Gift card created for {recipient.firstname}!',
                  'success')
        else:
            gift_card.save()
            flash('Gift card created!', 'success')
        return redirect(url_for('gift_card'))

    return render_template('gift_card.html', gift_card_form=gift_card_form)


def generate_gift_card_code():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@app.route("/catalogue")
def catalogue():
    if current_user.is_authenticated:
        role = current_user.role
        wishlist_items = [item.product_id for item in Wishlist.query.filter_by(user_id=current_user.id).all()]
    else:
        role = "User"
        wishlist_items = []
    search_query = request.args.get('search', '', type=str)
    category = request.args.get('category', '', type=str)
    query = Product.query
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    if category:
        query = query.filter(Product.category == category)
    products = query.all()
    return render_template(
        "catalogue.html",
        products=products,
        search_query=search_query,
        category=category,
        role=role,
        wishlist_items=wishlist_items
    )

@app.route('/admin/create-product', methods=['GET', 'POST'])
@login_required
@admin_required
def create_product():
    create_product_form = ProductForm()
    if create_product_form.validate_on_submit():
        product = Product(
            name=create_product_form.name.data,
            price=create_product_form.price.data,
            description=create_product_form.description.data,
            category=create_product_form.category.data,
            quantity=create_product_form.quantity.data,
            brand=create_product_form.brand.data,
            material=create_product_form.material.data,
            image_url=create_product_form.image_url.data
        )

        image_url = create_product_form.image_url.data
        image_url.save(os.path.join(app.root_path, 'static', 'assets', 'uploads', image_url.filename))
        product.image_url = image_url.filename
        product.save()
        return redirect("/admin/catalogue")
    return render_template("/admin/create_product.html", create_product_form=create_product_form)


@app.route("/admin/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    edit_product_form = ProductForm(name=product.name, price=product.price, description=product.description,
                                    category=product.category, material=product.material, brand=product.brand,
                                    quantity=product.quantity)
    if edit_product_form.validate_on_submit():
        product.name = edit_product_form.name.data
        product.price = edit_product_form.price.data
        product.description = edit_product_form.description.data
        product.category = edit_product_form.category.data
        product.material = edit_product_form.material.data
        product.brand = edit_product_form.brand.data
        product.quantity = edit_product_form.quantity.data
        image_url = edit_product_form.image_url.data
        image_url.save(os.path.join(app.root_path, 'static', 'assets', 'uploads', image_url.filename))
        product.image_url = image_url.filename
        product.update()
        return redirect("/admin/catalogue")
    return render_template("/admin/create_product.html", edit_product_form=edit_product_form)


@app.route("/admin/delete_product/<int:product_id>")
@login_required
@admin_required
def delete_product(product_id):
    Comment.query.filter_by(product_id=product_id).delete()
    Wishlist.query.filter_by(product_id=product_id).delete()
    Cart.query.filter_by(product_id=product_id).delete()
    product = Product.query.get(product_id)
    if product:
        product.delete()
    return redirect("/admin/catalogue")



@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/signup", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        existing_user_email = User.query.filter_by(email=register_form.email.data).first()
        existing_user_phone = User.query.filter_by(phone_number=register_form.phone_number.data).first()
        if existing_user_email:
            error_message = "An account with this email already exists."
            return render_template("signup.html", register_form=register_form, error_message=error_message)
        if existing_user_phone:
            error_message = "An account with this phone number already exists."
            return render_template("signup.html", register_form=register_form, error_message=error_message)
        user = User(firstname=register_form.firstname.data, lastname=register_form.lastname.data,
                    email=register_form.email.data, phone_number=register_form.phone_number.data,
                    gender=register_form.gender.data, country=register_form.country.data,
                    password=register_form.password.data)
        user_image = register_form.user_image.data
        user_image.save(os.path.join(app.root_path, 'static', 'assets', 'uploads', user_image.filename))
        user.user_image = user_image.filename
        user.save()
        return redirect("/signin")
    return render_template("signup.html", register_form=register_form)


@app.route("/signin", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    error_message = None
    if login_form.validate_on_submit():
        user = User.query.filter(User.email == login_form.email.data).first()
        if user is None:
            error_message = "The email address does not exist. Please check your email and try again."
        elif user and not user.check_password(login_form.password.data):
            error_message = "Incorrect password. Please try again."
        else:
            login_user(user)
            return redirect("/")
    print(login_form.errors)
    return render_template("signin.html", login_form=login_form, error_message=error_message)

@app.route("/catalogue/<int:product_id>", methods=["GET", "POST"])
def product_detail(product_id):
    comment_form = CommentForm()
    product = Product.query.get_or_404(product_id)
    comments = Comment.query.filter_by(product_id=product.id).all()
    in_cart = False
    if current_user.is_authenticated:
        in_cart = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first() is not None
    return render_template("product_detail.html", product=product, comments=comments, comment_form=comment_form, in_cart=in_cart)


@app.route("/catalogue/<int:product_id>/comment", methods=["POST"])
@login_required
def comment_on_product(product_id):
    product = Product.query.get_or_404(product_id)
    content = request.form.get("content")
    if content:
        comment = Comment(content=content, user_id=current_user.id, product_id=product.id)
        comment.save()

    return redirect(url_for("product_detail", product_id=product_id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/user/<int:user_id>")
@login_required
def user_page(user_id):
    testimonial_form = TestimonialForm()
    if current_user.id != user_id:
        return redirect("/")
    user = User.query.get(user_id)
    return render_template("user.html", user=user, testimonial_form=testimonial_form)


@app.route("/user/<int:user_id>/gift_cards")
@login_required
def user_gift_cards(user_id):
    user = User.query.get_or_404(user_id)
    created_gift_cards = GiftCard.query.filter_by(user_id=user.id).all()
    received_gift_cards = GiftCard.query.filter_by(recipient_email=current_user.email).all()
    return render_template(
        "user_gift_cards.html",
        created_gift_cards=created_gift_cards,
        received_gift_cards=received_gift_cards
    )

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        address = form.address.data
        city = form.city.data
        zip_code = form.zip_code.data
        card_number = form.card_number.data
        cvv = form.cvv.data
        return redirect("/checkout-success")
    return render_template('checkout.html', form=form)


@app.route('/checkout-success')
@login_required
def checkout_success():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    for item in cart_items:
        product = item.product
        if product.quantity >= item.quantity:
            product.quantity -= item.quantity
        else:
            flash(f"Insufficient stock for {product.name}. Quantity not updated.", 'danger')
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("Purchase completed! All items in your cart have been removed and product quantities have been updated.",
          'success')
    return render_template('success.html')


@app.route('/wishlist/<int:product_id>', methods=['POST'])
@login_required
@no_admin_required
def add_to_wishlist(product_id):
    existing_wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not existing_wishlist_item:
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        wishlist_item.save()
    return redirect(request.referrer)


@app.route('/wishlist')
@login_required
@no_admin_required
def view_wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    products = [item.product for item in wishlist_items]
    return render_template('wishlist.html', products=products)



@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
@login_required
@no_admin_required
def remove_from_wishlist(product_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if wishlist_item:
        wishlist_item.delete()
    return redirect(request.referrer)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
@no_admin_required
def add_to_cart(product_id):
    quantity = request.form.get('quantity', type=int, default=1)
    product = Product.query.get(product_id)
    if not product:
        flash("Product not found!", 'danger')
        return redirect(request.referrer)
    if quantity > product.quantity:
        flash('Not enough stock available!', 'danger')
        return redirect(request.referrer)
    existing_cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if existing_cart_item:
        existing_cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'{quantity} item(s) added to your cart!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
@login_required
@no_admin_required
def update_cart_quantity(product_id):
    new_quantity = request.form.get('quantity', type=int)
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if new_quantity and new_quantity > 0 and cart_item:
        product = cart_item.product
        if new_quantity <= product.quantity:
            cart_item.quantity = new_quantity
            db.session.commit()
    return redirect(url_for('view_cart'))


@app.route('/cart')
@login_required
@no_admin_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.delete()
    return redirect(url_for('view_cart'))


@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != "Admin":
        return redirect('/')
    return render_template('admin/panel.html')


@app.route("/admin/catalogue")
@login_required
@admin_required
def admin_catalogue():
    products = Product.query.all()
    return render_template("/admin/catalogue.html", products=products)

@app.route("/admin/catalogue/<int:product_id>")
@login_required
@admin_required
def admin_product_detail(product_id):
    product = Product.query.get(product_id)
    return render_template("/admin/product_detail.html", product=product)


@app.route('/admin/users')
@login_required
@admin_required
def users_admin():
    users = User.query.filter(User.role != 'Admin').all()
    return render_template('/admin/users.html', users=users)

@app.route("/admin/user/<int:user_id>")
@login_required
@admin_required
def admin_user_page(user_id):
    user = User.query.get(user_id)
    return render_template("/admin/user.html", user=user)


@app.route('/admin/testimonials', endpoint='testimonials')
def testimonials():
    filter_type = request.args.get('filter_type', 'all')
    if filter_type == 'approve':
        testimonials = Testimonial.query.filter_by(is_approved=False).all()
    elif filter_type == 'approved':
        testimonials = Testimonial.query.filter_by(is_approved=True).all()
    else:
        testimonials = Testimonial.query.all()
    return render_template('/admin/testimonials.html', testimonials=testimonials)

@app.route('/approve_testimonial/<int:testimonial_id>')
@login_required
@admin_required
def approve_testimonial(testimonial_id):
    testimonial = Testimonial.query.get(testimonial_id)
    if testimonial:
        testimonial.is_approved = True
        testimonial.save()
    return redirect('/admin/testimonials')

@app.route('/submit_testimonial', methods=['POST'])
@login_required
def submit_testimonial():
    if request.method == 'POST':
        content = request.form['content']
        testimonial = Testimonial(content=content, user_id=current_user.id)
        testimonial.save()
        return redirect(request.referrer)


@app.route('/admin/gift-cards')
@login_required
@admin_required
def admin_gift_cards():
    status = request.args.get('status', 'all')

    if status == 'used':
        gift_cards = GiftCard.query.filter_by(is_sent=True).all()
    elif status == 'unused':
        gift_cards = GiftCard.query.filter_by(is_sent=False).all()
    else:
        gift_cards = GiftCard.query.all()

    return render_template("/admin/gift_card.html", gift_cards=gift_cards, status=status)




@app.route('/admin/gift-card/<int:gift_card_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_gift_card_status(gift_card_id):
    gift_card = GiftCard.query.get_or_404(gift_card_id)
    gift_card.is_sent = not gift_card.is_sent
    db.session.commit()
    status = request.args.get('status', 'all')
    return redirect(url_for('admin_gift_cards', status=status))

@app.route('/admin/analytics')
@login_required
@admin_required
def analytics():
    gender_stats = db.session.query(
        User.gender, func.count(User.id).label('count')
    ).filter(User.role != 'Admin').group_by(User.gender).all()
    total_users = db.session.query(func.count(User.id)).filter(
        User.role != 'Admin').scalar()
    gender_percentages = {
        'Male': 0,
        'Female': 0,
        'Other': 0,
    }
    if total_users > 0:
        for gender, count in gender_stats:
            gender_percentages[gender] = (count / total_users) * 100
    country_stats = db.session.query(
        User.country, func.count(User.id).label('count')
    ).filter(User.role != 'Admin').group_by(User.country).all()
    country_percentages = {}
    for country, count in country_stats:
        country_percentages[country] = (count / total_users) * 100
    return render_template('admin/analytics.html', gender_percentages=gender_percentages,
                           country_percentages=country_percentages)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404