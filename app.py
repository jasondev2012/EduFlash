from flask import Flask, render_template
from routes.auth import auth_bp
from routes.courses import courses_bp
from routes.quiz import quiz_bp
from routes.history import history_bp
from routes.seguridad import seguridad_bp
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'autonoma-ing-software'

# Registrar rutas
app.register_blueprint(auth_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(history_bp)
app.register_blueprint(seguridad_bp)

@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nosotros")
def nosostros():
    return render_template("nosotros.html")

if __name__ == "__main__":
    app.run(debug=True)
