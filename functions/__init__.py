from flask import Flask, Blueprint

bp = Blueprint(
    'nabi',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/nabi/static'
)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix='/nabi')
    return app
