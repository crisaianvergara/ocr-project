from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# WTForms
class UploadForm(FlaskForm):
    image_file = FileField(
        "Select Receipt",
        validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg"])],
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        return redirect(url_for("receipt"))
    return render_template("index.html", form=form, title="Home")


@app.route("/receipt")
def receipt():
    return render_template("receipt.html", title="Receipt")


if __name__ == "__main__":
    app.run(debug=True)
