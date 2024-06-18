import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC454b5fef337b8560d48e48c077f9a6c1'
    TWILIO_SYNC_SERVICE_SID = 'ISab5dc00337226bcf628f5888dce5b204'
    TWILIO_API_KEY = 'SK28ab672d39ea68978c07838add1ce1cf'
    TWILIO_API_SECRET = 'Vwj1TYL35RdhvYpRkQB8MTDzbZ60Jkef'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    textintoform = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(textintoform)
    coolfile = "workfile.txt"
    return send_file(coolfile, as_attachment=True)
    
if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
