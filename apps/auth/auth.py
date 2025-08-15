from flask import Blueprint, render_template, request, url_for, redirect, flash
from models import User
from app import db
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, UpdateAccount




auth = Blueprint("auth", __name__, template_folder="../../templates")

@auth.route("/")
@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('product.dashboard'))
        else:
            flash('Invalid email or password')

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


@auth.route("/user-account", methods=["GET", "POST"])
@login_required
def update_account():
    form = UpdateAccount(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.current_password.data and form.new_password.data and form.confirm_password.data:
            if not check_password_hash(current_user.password, form.current_password.data):
                flash("Current password is incorrect.")
                return render_template("user_account.html", form=form, user=current_user)

            if form.new_password.data != form.confirm_password.data:
                flash("New passwords do not match.")
                return render_template("user_account.html", form=form, user=current_user)

            current_user.password = generate_password_hash(form.new_password.data)

        db.session.commit()
        flash("Account updated successfully!")
        return redirect(url_for("auth.update_account"))

    return render_template("user_account.html", form=form, user=current_user)
