from flask import Flask, request, jsonify
from extensions import db
from models import Svar  # Import models after initializing db
from config import DATABASE_URI
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # Dette laster inn variablene fra .env-filen



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)

migrate = Migrate(app, db)


@app.route('/svar', methods=['POST'])
def lagre_svar():
    try:
        # Få JSON-data fra forespørselen
        svar_data = request.json

        # Opprett et nytt svar-objekt
        nytt_svar = Svar(overskrift=svar_data['overskrift'], svar_innhold=svar_data['svar_innhold'])

        # Legg til det nye svaret i databasen
        db.session.add(nytt_svar)
        db.session.commit()

        # Returner en suksessmelding
        return jsonify({"melding": "Svar lagret vellykket"}), 201

    except Exception as e:
        # Returner en feilmelding hvis noe går galt
        return jsonify({"feil": str(e)}), 500

@app.route('/svar', methods=['GET'])
def hent_svar():
    try:
        # Hent alle svar fra databasen - dette er sqlacademy som hjelper med - jeg kan skrive det sånn så tar den seg av å konventere det til faktisk sql spørring, fordi det er jo det jeg må, jeg må inn i databasen min og hente ut dataen som ligger der i tabellen min svar 
        alle_svar = Svar.query.all()

        # Konverter svar til en liste av ordbøker for JSON-respons 
        # dette er nødvendig fordi jeg skriver i python, sqlen som hentes fra databasetabbel må oversettes til dictonaries - fordi det er det python forstår
        # json skrives akkuratt som ordbøker i python - så derfor kan man bare gjøre det om til dette

        svar_liste = [{"overskrift": svar.overskrift, "svar_innhold": svar.svar_innhold, "svar_id": svar.svar_id} for svar in alle_svar]

        # Returner svar
        return jsonify(svar_liste)

    except Exception as e:
        # Returner en feilmelding hvis noe går galt
        return jsonify({"feil": str(e)}), 500


#midlertidig gpt
import random

sporsmal = [
    "Hva er du mest takknemlig for i dag?",
    "Nevn tre personer du er takknemlig for å ha i livet ditt.",
    "Hvilket nylig øyeblikk har gitt deg glede og takknemlighet?",
    # Flere spørsmål...
]

@app.route('/api/takknemlighetssporsmal', methods=['GET'])
def takknemlighetssporsmal():
    return jsonify(random.choice(sporsmal))


if __name__ == '__main__':
    app.run(debug=True)