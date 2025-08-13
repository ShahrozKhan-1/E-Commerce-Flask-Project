from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from forms import AddProduct, EditProduct
from models import Category, Cart, Checkout, Product, User, ProductImage
from app import db
from flask import jsonify
import cloudinary.uploader


product = Blueprint("product", __name__, template_folder="../../templates")


@product.route("/dashboard")
@login_required
def dashboard():
    categories = Category.query.all()
    category_products = []
    for category in categories:
        products = Product.query.filter_by(category_id=category.id).limit(4) 
        if products:
            category_products.append({
                "category": category,
                "products": products
            })
    return render_template("dashboard.html", category_products=category_products)
    

@product.route("/delete-product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id == current_user.id or current_user.is_admin:
        Cart.query.filter_by(product_id=product.id).delete()
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully")
    else:
        flash("You are not authorized to delete this product.")
        return redirect(url_for("product.dashboard"))
    return redirect(url_for("product.dashboard"))


@product.route("/add-product", methods=["POST", "GET"])
@login_required
def add_product():
    form = AddProduct()
    categories = [(c.id, c.name) for c in Category.query.all()]
    categories.append((-1, "Add New Category"))
    form.category.choices = categories
    if form.validate_on_submit():
        if form.category.data == -1:
            flash("Please add a category first before saving the product.")
            return render_template("add_product.html", form=form)
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            user_id=current_user.id,
            brand=form.brand.data,
            category_id=form.category.data
        )    
        db.session.add(new_product)
        db.session.flush()
        for image_file in form.images.data:
            if image_file:
                try:
                    upload_result = cloudinary.uploader.upload(image_file)
                    image_url = upload_result['secure_url']
                    new_image = ProductImage(
                        url=image_url,
                        product_id=new_product.id
                    )
                    db.session.add(new_image)
                except Exception as e:
                    flash(f"Error uploading image: {str(e)}")
                    continue
        if not new_product.images:
            flash("At least one image is required")
            return render_template("add_product.html", form=form)
        db.session.commit()
        flash("Product added successfully!")
        return redirect(url_for("product.dashboard"))
    return render_template("add_product.html", form=form)


@product.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id and not current_user.is_admin:
        flash("Unauthorized")
        return redirect(url_for("product.dashboard"))
    categories = Category.query.all()    
    form = EditProduct(obj=product)
    form.category.choices = [(c.id, c.name) for c in categories]  
    if request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.brand.data = product.brand
        form.category.data = product.category_id
        form.description.data = product.description    
    if form.validate_on_submit():
        try:
            product.name = form.name.data
            product.price = form.price.data
            product.brand = form.brand.data
            product.category_id = form.category.data 
            product.description = form.description.data            
            if form.images.data and form.images.data[0].filename != '':
                for image_file in form.images.data:
                    if image_file.filename != '':
                        try:
                            upload_result = cloudinary.uploader.upload(image_file)
                            new_image = ProductImage(
                                url=upload_result['secure_url'],
                                product_id=product.id
                            )
                            db.session.add(new_image)
                        except Exception as e:
                            flash(f"Error uploading image: {str(e)}")          
            db.session.commit()
            flash("Product updated successfully!")
            return redirect(url_for("product.dashboard"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            db.session.rollback() 
    return render_template(
        "edit_product.html",
        form=form,
        product=product
    )
    

@product.route("/display-product/<int:product_id>")
@login_required
def display_product(product_id):
    product = Product.query.get(product_id)
    return render_template("display_product.html", product=product)


@product.route("/products/delete-image/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    image = ProductImage.query.get_or_404(image_id)    
    if image.product.user_id != current_user.id and not current_user.is_admin:
        return "Unauthorized"    
    try:
        db.session.delete(image)
        db.session.commit()
        return "Image deleted successfully"
    except Exception as e:
        return f"Error deleting image: {str(e)}"
    

@product.route("/add-category", methods=["POST"])
@login_required
def add_category():
    data = request.get_json()
    name = data.get("category_name")
    if not name:
        return jsonify({"error": "Category name is required"})
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"id": new_category.id, "name": new_category.name})


@product.route("/category/<int:category_id>")
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template("category_products.html", category=category, products=products)


@product.route("/cart/<int:product_id>", methods=["POST", "GET"])
@login_required
def add_to_cart(product_id):  
    if current_user.is_authenticated or current_user.is_admin:
        quantity = request.form.get("quantity")
        item = Cart.query.filter_by(product_id=product_id, user_id=current_user.id).first()
        if item:
            flash(f"Item is already added to cart!")
        else:
            cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)   
        db.session.commit()
        flash(f"Item added to cart successfully")
    return redirect(url_for("product.dashboard"))
    
    
@product.route("/cart-items/<int:user_id>", methods=["GET", "POST"])
@login_required
def cart_items(user_id):
    if current_user.is_authenticated or current_user.is_admin:
        if request.method == "POST":
            item_id = request.form.get("item_id", type=int)
            new_quantity = request.form.get("quantity", type=int)

            if item_id and new_quantity and new_quantity > 0:
                item = Cart.query.get_or_404(item_id)
                if item.user_id == current_user.id or current_user.is_admin:
                    item.quantity = new_quantity
                    db.session.commit()
                    return ""  
        total_sum = 0
        items = Cart.query.filter_by(user_id=user_id).all()
        for item in items:
            total_sum += item.quantity * item.product.price
        return render_template("cart.html", items=items, price=total_sum)
    
    return render_template("dashboard.html")


@product.route("/remove-from-cart/<int:item_id>", methods=["POST"])
@login_required
def remove_cart_item(item_id ):
    if current_user.is_authenticated or current_user.is_admin:
        item = Cart.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        flash(f"Item Removed Successfully ")
        return redirect(url_for("product.cart_items", user_id=current_user.id))
    items = Cart.query.filter_by(user_id=current_user.id)
    return render_template("cart.html", items=items)


@product.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    checkout_data = []
    price = 0
    customer_name = request.form.get("name")
    address = request.form.get("address")
    for item in cart_items:
        checkout_data.append({
            "product_name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
        })
        price += item.product.price * item.quantity
    checkout = Checkout(details=checkout_data, total_price=price, user_id=current_user.id, customer_name=customer_name, address=address)
    db.session.add(checkout)
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for("product.order_confirmation",order_id=checkout.id))


@product.route("/user-products/<int:user_id>", methods=["GET"])
@login_required
def user_product(user_id):
    categories = Category.query.all() 
    if current_user.is_admin:
        products = Product.query.all()
        return render_template("user_product.html", user_products=products, categories=categories) 
    else:
        products = Product.query.filter_by(user_id=user_id).all()
        return render_template("user_product.html", user_products=products, categories=categories) 
    
    
@product.route("/user-account")
@login_required
def user_account():
    user = User.query.get(current_user.id)
    return render_template("user_account.html", user=user)


@product.route("/admin-checkout")
@login_required
def admin_checkout():
    if current_user.is_admin:
        checkout_item = Checkout.query.all()
        return render_template("admin_checkout.html", checkout_item=checkout_item)
    return render_template("dashboard.html")
    
    
@product.route("/about")
@login_required
def about():
    return render_template("about.html")


@product.route("/contact")
@login_required
def contact():
    return render_template("contact.html")


@product.route("/shop")
def shop():
    products = Product.query.all() 
    return render_template("shop.html", products=products)


@product.route("/order-confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    checkout = Checkout.query.get_or_404(order_id)
    return render_template("order_confirmation.html", checkout=checkout)


@product.route('/search')
def search():
    query = request.args.get("q")
    if query:
        results = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    else:
        results = Product.query.all()
    return render_template("search_results.html", results=results, query=query)