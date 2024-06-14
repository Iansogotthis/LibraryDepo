from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10))
    borrows = db.relationship('Borrow', back_populates='user')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        roles = request.form.getlist('role')  # Get list of selected roles
        new_user = User(username=username, password=hashed_password, role=','.join(roles))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(13), nullable=False)
    publisher = db.Column(db.String(100))
    description = db.Column(db.Text)
    borrows = db.relationship('Borrow', back_populates='book')
    
class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User', back_populates='borrows')
    book = db.relationship('Book', back_populates='borrows')

User.borrows = db.relationship('Borrow', back_populates='user')
Book.borrows = db.relationship('Borrow', back_populates='book')

# Ensure tables are created in the correct context
with app.app_context():
    db.create_all()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Admins only!'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year, 'isbn': book.isbn, 'publisher': book.publisher, 'description': book.description} for book in books])

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year, 'isbn': book.isbn, 'publisher': book.publisher})

@app.route('/book', methods=['POST'])
@login_required
@admin_required
def add_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        year=data['year'],
        isbn=data['isbn'],
        publisher=data['publisher'],
        description=data['description']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully!'}), 201

@app.route('/book/<int:book_id>', methods=['PUT'])
@login_required
@admin_required
def update_book(book_id):
    data = request.json
    book = Book.query.get_or_404(book_id)
    book.title = data['title']
    book.author = data['author']
    book.year = data['year']
    book.isbn = data['isbn']
    book.publisher = data['publisher']
    book.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})

@app.route('/book/<int:book_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully!'})

@app.route('/search', methods=['GET'])
@login_required
def search_books():
    query = request.args.get('query')
    if query:
        results = Book.query.filter(
            (Book.title.contains(query)) |
            (Book.author.contains(query)) |
            (Book.publisher.contains(query))
        ).all()
        return jsonify([{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'isbn': book.isbn,
            'publisher': book.publisher,
            'description': book.description
        } for book in results])
    return jsonify({'message': 'No search query provided.'})

app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.borrows.filter_by(return_date=None).first():
        return jsonify({'message': 'Book already borrowed!'}), 400
    borrow = Borrow(user_id=current_user.id, book_id=book_id)
    db.session.add(borrow)
    db.session.commit()
    return jsonify({'message': 'Book borrowed successfully!'})

@app.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    borrow = Borrow.query.get_or_404(borrow_id)
    if borrow.user_id != current_user.id:
        return jsonify({'message': 'Not authorized!'}), 403
    borrow.return_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Book returned successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
