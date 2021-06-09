"""Python Flask Cryptr Resource server integration sample
"""
from flask import Flask, jsonify
 
app = Flask(__name__)

app.config.from_object('config')