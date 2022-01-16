from dashboards import db, create_app, bcrypt
from dashboards.models import User


DEBUG = True

hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")

testUser = User(email="test@gmail.com", password=hashed_password)

app = create_app(DEBUG)
with app.app_context():
    User.__table__.drop(db.engine)
    User.__table__.create(db.engine)
    db.session.add(testUser)
    db.session.commit()
