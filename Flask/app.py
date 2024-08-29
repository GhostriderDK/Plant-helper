import base64
from io import BytesIO
from flask import Flask, render_template

app = Flask(__name__)
app.run(debug=True)

@app.route('/')
def home():
    return render_template('index.html')