from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Default route to redirect to home
@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    message = "Home Page"
    return render_template("index.html", message=message)

@app.route("/about")
def about():
    message = "About Page"
    return render_template("index.html", message=message)

@app.route("/service")
def service():
    message = "Service Page"
    return render_template("index.html", message=message)

@app.route("/contact")
def contact():
    message = "Contact Page"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
