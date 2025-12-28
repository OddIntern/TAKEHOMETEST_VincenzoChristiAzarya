from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import User
from app.schemas import user_schema
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Helper for route protection (Duplicate of tasks.py, usually strictly shared in utils)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token: return jsonify({'message': 'Token missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except: return jsonify({'message': 'Token invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    new_user = User(
        username=data.get('username'),
        password_hash=generate_password_hash(data.get('password')),
        board_title=f"{data.get('username')}'s Board" # Default custom name
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if not user or not check_password_hash(user.password_hash, data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token, 'user': user_schema.dump(user)})

# --- NEW ROUTE: Update Board Title ---
@bp.route('/board-title', methods=['PUT'])
@token_required
def update_board_title(current_user):
    data = request.get_json()
    new_title = data.get('title')
    
    if new_title:
        current_user.board_title = new_title
        db.session.commit()
        return jsonify({'message': 'Title updated', 'user': user_schema.dump(current_user)})
    
    return jsonify({'message': 'No title provided'}), 400