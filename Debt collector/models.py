from app import db

class Debtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    debt = db.Column(db.Float, nullable=False)
    reminder_interval = db.Column(db.Integer, nullable=False)
    email_enabled = db.Column(db.Boolean, nullable=False)
    sms_enabled = db.Column(db.Boolean, nullable=False)
    whatsapp_enabled = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Debtor {self.name}'
