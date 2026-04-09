import os
from datetime import timedelta
from flask import Flask

from core.config.config import SECRET_KEY
from core.extensions import limiter
from core.routes.system_routes import system_bp
from core.routes.auth_routes.auth_routes import auth_bp
from core.routes.captcha.routes_captcha import captcha_bp
from core.security.security import csrf_protect, inject_csrf
from core.models.transaction import transaction_bp

# APP
app = Flask(__name__)
app.secret_key = SECRET_KEY

# CONFIG
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)

# EXTENSIONS
limiter.init_app(app)

# BLUEPRINTS
app.register_blueprint(system_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(captcha_bp)
app.register_blueprint(transaction_bp)

# MIDDLEWARE & CONTEXT
app.before_request(csrf_protect)
app.context_processor(inject_csrf)

# START
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
<<<<<<< HEAD
        debug=os.getenv("FLASK_DEBUG") == "True"
    )
=======
        debug=os.getenv("FLASK_DEBUG") == "false"            
    )
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)
