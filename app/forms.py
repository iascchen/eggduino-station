# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, HiddenField, TextAreaField
from wtforms.validators import NumberRange, InputRequired, EqualTo


class IntervalForm(FlaskForm):
    hidden_pid = HiddenField('Hidden ID')
    tem_interval = IntegerField('Temperature', default=20, validators=[NumberRange(min=20, max=255)])
    hum_interval = IntegerField('Humidity', default=70, validators=[NumberRange(min=5, max=255)])
    mov_interval = IntegerField('Movement', default=2000, validators=[NumberRange(min=300, max=65535)])
    env_interval = IntegerField('Environment', default=2, validators=[NumberRange(min=2, max=255)])

    # def validate(self):
    #     if not FlaskForm.validate(self):
    #         print 'Optional Form Errors: {0}'.format(self.errors)
    #         return False
    #
    #     print 'Optional Form Errors: {0}'.format(self.errors)
    #     return True


class SchedulesForm(FlaskForm):
    hidden_pid = HiddenField('Hidden ID')
    schedules = TextAreaField('Schedules', validators=[InputRequired()])

    def validate(self):
        if not FlaskForm.validate(self):
            print 'Optional Form Errors: {0}'.format(self.errors)
            return False

        print 'Optional Form Errors: {0}'.format(self.errors)
        return True


class PidForm(FlaskForm):
    hidden_pid = HiddenField('Hidden ID')
    pid = StringField('Process ID',
                      validators=[InputRequired(), EqualTo('hidden_pid', message='Must same with the process_id')])

    # def validate(self):
    #     if not FlaskForm.validate(self):
    #         print 'Optional Form Errors: {0}'.format(self.errors)
    #         return False
    #
    #     print 'Optional Form Errors: {0}'.format(self.errors)
    #     return True


class DataRenderForm(FlaskForm):
    tem_range = StringField('Range', validators=[InputRequired()])
    act = StringField('Action', validators=[InputRequired()])

    # def validate(self):
    #     if not FlaskForm.validate(self):
    #         print 'Optional Form Errors: {0}'.format(self.errors)
    #         return False
    #
    #     return True


class DataDownloadForm(FlaskForm):
    date_range = StringField('From Date', validators=[InputRequired()])
    act = StringField('Action', validators=[InputRequired()])

    # def validate(self):
    #     if not FlaskForm.validate(self):
    #         print 'Optional Form Errors: {0}'.format(self.errors)
    #         return False
    #
    #     return True
