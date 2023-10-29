from app import create_app, db
import os


app = create_app(os.getenv("FLASK_ENV", "dev"))

def init_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()