from flask import Flask

app = Flask(__name__)

import routing

routing.init_app(app)