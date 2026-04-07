from marshmallow import Schema, fields, validate, ValidationError
from flask import request, jsonify
from functools import wraps

class VitalSignsSchema(Schema):
    heart_rate = fields.Int(validate=validate.Range(min=30, max=250), allow_none=True)
    blood_pressure_systolic = fields.Int(validate=validate.Range(min=70, max=250), allow_none=True)
    blood_pressure_diastolic = fields.Int(validate=validate.Range(min=40, max=200), allow_none=True)
    temperature = fields.Float(validate=validate.Range(min=35.0, max=42.0), allow_none=True)
    oxygen_saturation = fields.Int(validate=validate.Range(min=50, max=100), allow_none=True)
    respiratory_rate = fields.Int(validate=validate.Range(min=8, max=40), allow_none=True)

class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(required=True)

vital_schema = VitalSignsSchema()
user_schema = UserRegistrationSchema()

def validate_vital_signs(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            vital_schema.load(request.json)
            return f(*args, **kwargs)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
    return decorated

def validate_user_registration(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_schema.load(request.json)
            return f(*args, **kwargs)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
    return decorated
