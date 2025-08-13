from flask import Blueprint, render_template, request, url_for, redirect, flash
from models import User
from app import db
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm




auth = Blueprint("auth", __name__, template_folder="../../templates")

@auth.route("/")
@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('product.dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template("login.html", form=form)



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                flash('User already exists')
                return redirect(url_for('auth.register'))
            
            new_user = User(email=form.email.data, username=form.username.data, password=generate_password_hash(form.password.data))
            db.session.add(new_user)
            db.session.commit()       
            flash('Registration successful!')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/update-account", methods=["POST"])
@login_required
def update_account():
    username = request.form.get("username")
    email = request.form.get("email")
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    current_user.username = username
    current_user.email = email

    if current_password and new_password and confirm_password:
        if not check_password_hash(current_user.password, current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("product.update_account"))
        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("product.update_account"))
        current_user.password = generate_password_hash(new_password)

    db.session.commit()
    flash("Account updated successfully!", "success")
    return redirect(url_for("product.user_account", user_id=current_user.id))
