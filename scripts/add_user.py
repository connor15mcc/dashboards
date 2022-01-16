from dashboards import db, create_app, bcrypt
from dashboards.models import User


DEBUG = True

if not DEBUG:
    email = input("Email: ")
    password = input("Password: ")
    hashed_password = bcrypt.generate_password_hash(password=password).decode("utf-8")

    app = create_app(False)
    with app.app_context():
        db.session.add(User(email=email, password=hashed_password))
        db.session.commit
else:
    hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")
    testUser = User(email="test@gmail.com", password=hashed_password)

    app = create_app(DEBUG)
    with app.app_context():
        User.__table__.drop(db.engine)
        User.__table__.create(db.engine)
        db.session.add(testUser)
        db.session.commit()
