from flask import Flask, render_template, url_for, redirect
import os
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, The Home Depot!'

if __name__ == "__main__":
    app.run(debug=True)