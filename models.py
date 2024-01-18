from extensions import db

class Svar(db.Model):
    svar_id = db.Column(db.Integer, primary_key=True)
    overskrift = db.Column(db.String, nullable=False)
    svar_innhold = db.Column(db.String, nullable=False)

    def __init__(self, overskrift, svar_innhold) -> None:
        self.overskrift = overskrift
        self.svar_innhold = svar_innhold



