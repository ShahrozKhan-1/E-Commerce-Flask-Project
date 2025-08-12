# E-Commerce Flask Project

An online shopping platform built with Python's Flask framework, featuring user authentication, product catalog, product management with permissions, and a shared dashboard for users and admins.

## 🛠️ Features

- **User Authentication**: Secure login and registration system.
- **Product Management**:
  - Users can **create**, **edit**, and **delete** products they have added.
  - Admins can **edit** and **delete** any product.
  - Other users can only **view** products and **add them to the cart**.
- **Shared Dashboard**: The dashboard is the same for admins and users but shows controls based on user permissions.
- **Product Catalog**: Browse and search products.
- **Shopping Cart**: Add, update, or remove items.

## 🧱 Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ShahrozKhan-1/E-Commerce-Flask-Project.git
   cd E-Commerce-Flask-Project
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   >>> pip install -r requirements.txt
   ```

5. Set up the database:

   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. Run the application:

   ```bash
   python app.py
   ```

   The app will be accessible at `http://127.0.0.1:5000/`.

## 📂 Project Structure

```
E-Commerce-Flask-Project/
│
├── app.py            # Main application file
├── config.py         # Configuration settings
├── models.py         # Database models
├── forms.py          # WTForms for form handling
├── templates/        # HTML templates
│   ├── layout.html
│   ├── index.html
│   ├── login.html
│   └── register.html
└── static/           # Static files (CSS, JS, Images)
    ├── css/
    ├── js/
    └── images/
```
