from app.extensions import app, db
from app.main.routes import main
from app.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
	db.create_all()

# This fixes the gonicons error when importing the package
__all__ = ["app"]

