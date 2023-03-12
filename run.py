from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from wtforms.validators import DataRequired
import json
import requests
import io

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# Constants
URL = "https://ocr.asprise.com/api/v1/receipt"

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
        file_data = form.image_file.data.read()
        # Create an in-memory file object from the uploaded file data
        file_obj = io.BytesIO(file_data)

        response = requests.post(
            URL,
            data={"api_key": "TEST", "recognizer": "auto", "ref_no": "oct_python_123"},
            files={"file": file_obj},
        )

        with open("response.json", "w") as file:
            json.dump(json.loads(response.text), file)

        return redirect(url_for("receipt"))
    return render_template("index.html", form=form, title="Home")


@app.route("/receipt")
def receipt():
    with open("response.json", "r") as file:
        data = json.load(file)
    return render_template("receipt.html", data=data, title="Receipt")


if __name__ == "__main__":
    app.run(debug=True)
