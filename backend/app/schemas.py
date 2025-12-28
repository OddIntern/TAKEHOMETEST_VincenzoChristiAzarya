from app import ma
from app.models import User, Task
from marshmallow import fields, validate

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',) # Hide password
        
    # Explicitly define new fields to ensure they appear in JSON
    board_title = fields.String(dump_default="Project Board")

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        include_fk = True
    
    # Custom validations
    status = fields.String(validate=validate.OneOf(['To Do', 'In Progress', 'Done']))
    
    # JSON Fields
    assigned_user_ids = fields.List(fields.String())
    history = fields.List(fields.Dict())

# Init schemas
user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)