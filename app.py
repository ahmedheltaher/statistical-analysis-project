import flask
import flask_wtf
import wtforms
import flask_sqlalchemy

from datetime import datetime
from regressor import predict

app = flask.Flask(__name__)

db = flask_sqlalchemy.SQLAlchemy(app)

app.config["SECRET_KEY"] = "6ca6df7509ec15434385a7ba1dbce8de"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"


class PatientEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.Integer, nullable=False)
    fasting = db.Column(db.Integer, nullable=False)
    exercise_angina = db.Column(db.Integer, nullable=False)
    chest_pain_type = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.Integer, nullable=False)
    cholesterol = db.Column(db.Integer, nullable=False)
    max_hr = db.Column(db.Integer, nullable=False)
    old_peak = db.Column(db.Integer, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)

    date_submitted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)


class RegistrationForm(flask_wtf.FlaskForm):
    sex = wtforms.SelectField(
        u'Sex', choices=[(1, 'Male'), (0, 'Female')], validators=[wtforms.validators.DataRequired()])
    fasting = wtforms.SelectField(
        u'Have been Fasting regularly', choices=[(1, 'Yes'), (0, 'No')], validators=[wtforms.validators.DataRequired()])
    exercise_angina = wtforms.SelectField(
        u'Do You Have exercise angina ', choices=[(1, 'Yes'), (0, 'No')], validators=[wtforms.validators.DataRequired()])
    chest_pain_type = wtforms.SelectField(
        u'What is your chest pain type', choices=[(0, 'ATA'), (1, 'NAP'), (2, 'ASY'), (3, 'TA')], validators=[wtforms.validators.DataRequired()])

    age = wtforms.IntegerField(
        'Age', validators=[wtforms.validators.DataRequired()])
    blood_pressure = wtforms.IntegerField(
        'Blood Pressure', validators=[wtforms.validators.DataRequired()])
    cholesterol = wtforms.IntegerField(
        'Cholesterol Level', validators=[wtforms.validators.DataRequired()])
    max_hr = wtforms.IntegerField(
        'Max HR', validators=[wtforms.validators.DataRequired()])
    old_peak = wtforms.IntegerField(
        'Old Peak', validators=[wtforms.validators.DataRequired(), wtforms.validators.NumberRange(min=1)])

    submit = wtforms.SubmitField('submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        value = predict([int(form.age.data), int(form.sex.data), int(form.chest_pain_type.data), int(form.blood_pressure.data), int(form.cholesterol.data),
                         int(form.fasting.data), int(form.max_hr.data), int(form.exercise_angina.data), int(form.old_peak.data) - 1])
        patient_entry = PatientEntry(
            sex=int(form.sex.data), fasting=int(form.fasting.data),
            exercise_angina=int(form.exercise_angina.data), chest_pain_type=int(form.chest_pain_type.data),
            age=int(form.age.data), blood_pressure=int(form.blood_pressure.data), cholesterol=int(form.cholesterol.data),
            max_hr=int(form.max_hr.data), old_peak=int(form.old_peak.data) - 1, prediction=value)
        db.session.add(patient_entry)
        db.session.commit()
        return flask.render_template("response.html", value=value)
    return flask.render_template("index.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
