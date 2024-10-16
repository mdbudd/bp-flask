from datetime import datetime
from email import message
import os
from unittest import TextTestRunner
from flask_restful import Resource, reqparse
import os
import datetime
import json
import sys
from flask import request, jsonify
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
# from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from blocklist import BLOCKLIST

from packages.security.token import getTykTokenPayload

# from packages.pi_core.utilities.user import get_jwt_identity, get_jwt, replace_sub
# from packages.pi_core.services.employee import GetUserByRacf, GetUserBySrn


class UserInfoSchema(Schema):
    selection = fields.String()


class AuthSchema(Schema):
    Authorization = fields.String(doc_default="Tyk Access Token", required=False)
    Token = fields.String(doc_default="Bearer XXXX", required=False)


class TokenSchema(Schema):
    passcode = fields.String(doc_default="XXXXXXXXXXX", required=True)
    token = fields.String(doc_default="", required=True)


class UserAuth(MethodResource, Resource):
    @doc(description="", tags=["User"])
    @use_kwargs(AuthSchema, location="headers")
    def get(self, **kwargs):
        from flask import request

        headers = request.headers
        token = ""
        if "tyk-claimsetjwt" in headers:
            print("token in tyk header")
            token = headers["tyk-claimsetjwt"]
        else:
            print("no tyk header present")
            access_token = kwargs["Token"] if "Token" in kwargs else None
            if access_token == None:
                return jsonify(message="No JWT in request", error="token_missing")
            return jsonify(access_token=access_token)
        payload = getTykTokenPayload(token)
        if payload == None:
            return jsonify(message="The IAM token has expired", error="token_expired")
        else:
            additional_claims = {"imp": False, "tyk": payload}
