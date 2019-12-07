from core import create_app
from config import Config
from core.views import uber


flask_app = create_app(Config)
flask_app.register_blueprint(uber)

if __name__ == "__main__":
    flask_app.run(debug=True)
