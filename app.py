from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from datetime import datetime

# DO NOT import models here to avoid circular import
# from models import User  # <-- remove this

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models AFTER db is set up to avoid circular import
    from models import User

    @app.post('/api/users')
    def create_user():
        payload = request.get_json(force=True, silent=False)
        username = payload.get('user')
        raw_password = payload.get('password')
        dosha = payload.get('dosha')

        if not username or not raw_password:
            return jsonify({"error": "'user' and 'password' are required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "user already exists"}), 409

        user = User(
            username=username,
            password_hash=generate_password_hash(raw_password),
            dosha=dosha or None,
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    @app.get('/api/users')
    def list_users():
        users = User.query.order_by(User.id.asc()).all()
        return jsonify([u.to_dict() for u in users])

    @app.get('/api/users/<int:user_id>')
    def get_user(user_id: int):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @app.patch('/api/users/<int:user_id>')
    def update_user(user_id: int):
        user = User.query.get_or_404(user_id)
        payload = request.get_json(force=True, silent=False)

        if 'user' in payload and payload['user']:
            new_username = payload['user']
            if User.query.filter(User.username == new_username, User.id != user_id).first():
                return jsonify({"error": "user already exists"}), 409
            user.username = new_username

        if 'password' in payload and payload['password']:
            user.password_hash = generate_password_hash(payload['password'])

        if 'dosha' in payload:
            user.dosha = payload['dosha'] or None

        user.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(user.to_dict())

    @app.delete('/api/users/<int:user_id>')
    def delete_user(user_id: int):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return ('', 204)

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User}

    return app


# For `flask run`
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
