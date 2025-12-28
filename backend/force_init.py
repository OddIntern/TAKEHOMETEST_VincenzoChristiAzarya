from app import create_app, db
from app.models import User, Task

app = create_app()

with app.app_context():
    print(f"Connected to: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # 1. Drop everything (Clean start)
    print("Dropping old tables...")
    db.drop_all()
    
    # 2. Create everything (Force creation)
    print("Creating new tables...")
    db.create_all()
    
    print("Tables created successfully!")
    print("You can now run the server.")