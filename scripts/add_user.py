from dashboards import db, create_app, bcrypt
from dashboards.models import User
import getpass


email = input("Email: ")
password = getpass.getpass("Password: ")
hashed_password = bcrypt.generate_password_hash(password=password).decode("utf-8")

app = create_app(False)
with app.app_context():
    User.__table__.drop(db.engine)
    User.__table__.create(db.engine)

    db.session.add(User(email=email, password=hashed_password))
    db.session.commit()
