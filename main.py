#! venv/bin/python3
from app import app, db
from models import User
import view
import random
import arguments
import os

if __name__ == "__main__":
    app.run(host='0.0.0.0')
