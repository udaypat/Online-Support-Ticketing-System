import json, re
from werkzeug.exceptions import HTTPException
from flask import make_response

from app.data.models import User
from app.data.db import db


class NotFound(HTTPException):
    def __init__(self, status_code, msg=''):
        self.response = make_response(json.dumps(msg), status_code)


class ValidationErr(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        msg = {
            'error_code': error_code,
            'error_msg': error_msg
        }
        self.response = make_response(json.dumps(msg), status_code)


class Validation():
    def is_valid_string_value(field_value, field_name, alpha_only=True, allow_special_chars=False):
        if not isinstance(field_value, str):
            raise ValidationErr(
                status_code = 400,
                error_code = 'NON_STRING_ERR',
                error_msg = field_name+ ' should be a string'
            )

        if not field_value:
            raise ValidationErr(
                status_code = 400,
                error_code = 'EMPTY_FIELD_ERR',
                error_msg = field_name + ' should not be empty'
            )

        if alpha_only:
            if not field_value.isalpha():
                raise ValidationErr(
                    status_code = 400,
                    error_code = 'NON_ALPHABET_ERR',
                    error_msg = field_name + ' should only have alphabets'
                )

        if not allow_special_chars:
            prohibited_characters = {'@', '#', '$', '%', '^', '*', ';' , '{', '}'}
            for character in field_value:
                if character in prohibited_characters:
                    raise ValidationErr(
                        status_code = 400,
                        error_code = 'PROHIBITED_CHAR_ERR',
                        error_msg = field_name + ' should not contain @, #, $, %, ^, *, ;, {, } characters'
                    )

        return True


    def is_valid_email(email, new_user=True):
        pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
        if not re.match(pattern, email):
            raise ValidationErr(
                status_code = 400,
                error_code = 'INVALID_EMAIL_ERR',
                error_msg = 'Email is not valid'
            )

        if new_user:
            user = db.session.query(User).filter(User.email == email).first()
            if user:
                raise ValidationErr(
                    status_code = 400,
                    error_code = 'EMAIL_EXISTS_ERR',
                    error_msg = 'Email already registered. Try logging in'
                )
        return True


    def is_valid_username(username, new_user=True):
        pattern = r'^[A-Za-z0-9]+$'
        if not re.match(pattern, username):
            raise ValidationErr(
                status_code = 400,
                error_code = 'INVALID_USERNAME_ERR',
                error_msg = 'Username can contain only letters and numbers'
            )

        if new_user:
            user = db.session.query(User).filter(User.username == username).first()
            if user:
                raise ValidationErr(
                    status_code = 400,
                    error_code = 'USERNAME_EXISTS_ERR',
                    error_msg = 'Username not available'
                )
        return True


    def is_valid_password(password):
        if len(password) >= 8:
            return True
        raise ValidationErr(
            status_code = 400,
            error_code = 'PASSWORD_ERR',
            error_msg = 'Password must be atleast 8 characters long'
        )

    def is_valid_fullname(fullname):
        pattern = r'^[A-Za-z ]+$'
        if re.match(pattern, fullname):
            return True
        raise ValidationErr(
            status_code = 400,
            error_code = 'FULLNAME_ERR',
            error_msg = 'Full Name can only contain texts and spaces'
        )

    def is_valid_report_format(report_format):
        formats = ['html', 'pdf']
        if report_format in formats:
            return True
        raise ValidationErr(
            status_code = 400,
            error_code = 'REPORT_FORMAT_ERR',
            error_msg = 'Only html and pdf formats are supported'
        )

    def is_valid_image(image):
        allowed_image_extensions = ['jpg', 'jpeg', 'png', 'svg']
        if image:
            extension = image.filename.split('.')[-1]
            if extension in allowed_image_extensions:
                return extension
            else:
                raise ValidationErr(
                    status_code = 400,
                    error_code = 'IMAGE_EXTENSION_ERR',
                    error_msg = 'The uploaded image should only be in one of the following formats: {}'.format(tuple(allowed_image_extensions))
                )
        else:
            raise ValidationErr(
                status_code = 400,
                error_code = 'IMAGE_UPLOAD_ERR',
                error_msg = 'Image not found for upload. Please Select an image file'
            )

    def is_valid_image_bool(image):
        allowed_image_extensions = ['jpg', 'jpeg', 'png', 'svg']
        extension = image.filename.split('.')[-1]
        if extension in allowed_image_extensions:
            return True, extension
        else:
            err = 'The uploaded image should only be in one of the following formats: {}'.format(tuple(allowed_image_extensions))
            return False, err








