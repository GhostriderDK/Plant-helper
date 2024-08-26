import base64
from io import BytesIO
from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.run(debug=True)

@app.route('/')
def home():
    return render_template('index.html')