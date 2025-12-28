from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Task, User
from app.schemas import task_schema, tasks_schema
import jwt
from functools import wraps
from datetime import datetime

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# --- JWT Decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# --- 1. GET ALL TASKS ---
@bp.route('', methods=['GET'])
@token_required
def get_tasks(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.position.asc()).all()
    return jsonify(tasks_schema.dump(tasks))

# --- 2. CREATE TASK (No AI) ---
@bp.route('', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    
    # Direct mapping from Frontend -> Database
    # No AI guessing, just defaults if the user left it blank
    title = data.get('title')
    description = data.get('description', '')
    priority = data.get('urgency', 'Low')   # Default to Low
    selected_tag = data.get('tag', 'Feature') # Default to Feature
    due_date = data.get('dueDate')          # Default to None (Empty)

    count = Task.query.filter_by(user_id=current_user.id, status='To Do').count()
    
    new_task = Task(
        title=title,
        description=description,
        status=data.get('status', 'To Do'),
        position=count,
        user_id=current_user.id,
        tag=selected_tag,
        priority=priority,
        due_date=due_date,
        assigned_user_ids=data.get('assignedUserIds', []),
        history=[{'action': 'Created', 'date': datetime.utcnow().isoformat()}]
    )
    
    db.session.add(new_task)
    db.session.commit()
    return task_schema.dump(new_task), 201

# --- 3. UPDATE TASK ---
@bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    changes = [] 

    if 'title' in data and data['title'] != task.title:
        changes.append(f"Title changed to '{data['title']}'")
        task.title = data['title']

    if 'description' in data and data['description'] != task.description:
        changes.append("Description updated")
        task.description = data['description']

    if 'status' in data and data['status'] != task.status:
        changes.append(f"Moved to {data['status']}")
        task.status = data['status']

    new_urgency = data.get('urgency')
    if new_urgency and new_urgency != task.priority:
        changes.append(f"Urgency changed to {new_urgency}")
        task.priority = new_urgency

    if 'tag' in data and data['tag'] != task.tag:
        changes.append(f"Tag changed to {data['tag']}")
        task.tag = data['tag']

    if 'dueDate' in data and data['dueDate'] != task.due_date:
        changes.append(f"Due date set to {data['dueDate']}")
        task.due_date = data['dueDate']

    if 'assignedUserIds' in data:
        new_ids = data['assignedUserIds']
        if set(new_ids) != set(task.assigned_user_ids or []):
            changes.append("Assignees updated")
            task.assigned_user_ids = new_ids

    if changes:
        timestamp = datetime.utcnow().isoformat()
        new_logs = [{'action': msg, 'date': timestamp} for msg in changes]
        current_history = list(task.history) if task.history else []
        current_history.extend(new_logs)
        task.history = current_history

    db.session.commit()
    return task_schema.dump(task)

# --- 4. DELETE TASK ---
@bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

# --- 5. DUPLICATE TASK ---
@bp.route('/<int:task_id>/duplicate', methods=['POST'])
@token_required
def duplicate_task(current_user, task_id):
    original = Task.query.get_or_404(task_id)
    if original.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    new_task = Task(
        title=f"{original.title} (Copy)",
        description=original.description,
        status=original.status,
        position=original.position + 1,
        user_id=current_user.id,
        tag=original.tag,
        priority=original.priority,
        due_date=original.due_date,
        assigned_user_ids=list(original.assigned_user_ids or []),
        history=[{'action': f'Duplicated from "{original.title}"', 'date': datetime.utcnow().isoformat()}]
    )
    
    db.session.add(new_task)
    db.session.commit()
    return task_schema.dump(new_task), 201

# --- 6. REORDER TASKS ---
@bp.route('/reorder', methods=['PATCH'])
@token_required
def reorder_tasks(current_user):
    data = request.get_json()
    new_status = data.get('status')
    task_ids = data.get('task_ids', [])
    timestamp = datetime.utcnow().isoformat()

    for index, task_id in enumerate(task_ids):
        task = Task.query.get(task_id)
        if task and task.user_id == current_user.id:
            if task.status != new_status:
                log = {'action': f"Moved to {new_status}", 'date': timestamp}
                existing_history = list(task.history) if task.history else []
                existing_history.append(log)
                task.history = existing_history 
            
            task.status = new_status
            task.position = index
            
    db.session.commit()
    return jsonify({'message': 'Board updated'})