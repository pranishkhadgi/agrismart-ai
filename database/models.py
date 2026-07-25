from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    role       = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    predictions = db.relationship('Prediction', backref='user', lazy=True)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.email}>'


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    N           = db.Column(db.Float)
    P           = db.Column(db.Float)
    K           = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity    = db.Column(db.Float)
    ph          = db.Column(db.Float)
    rainfall    = db.Column(db.Float)
    crop        = db.Column(db.String(100))
    confidence  = db.Column(db.Float)
    yield_kg    = db.Column(db.Float)
    zone        = db.Column(db.String(100))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Prediction {self.crop} by User {self.user_id}>'


class CropData(db.Model):
    __tablename__ = 'crop_data'

    id          = db.Column(db.Integer, primary_key=True)
    crop_name   = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    season      = db.Column(db.String(100))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CropData {self.crop_name}>'


class MLModelRecord(db.Model):
    __tablename__ = 'ml_models'

    id          = db.Column(db.Integer, primary_key=True)
    model_name  = db.Column(db.String(100), nullable=False)
    filename    = db.Column(db.String(200), nullable=False)
    accuracy    = db.Column(db.Float)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MLModel {self.model_name}>'