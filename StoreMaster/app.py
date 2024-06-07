from flask import render_template
from flask_login import  current_user, login_required
from flask import Blueprint

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html",name=current_user.name)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
