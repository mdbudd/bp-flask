import json
from flask_restful import Resource, reqparse
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields

# from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from blocklist import BLOCKLIST
from packages.core.utilities.data import call_procedure, call_function, call_statement
from resources.user import AuthSchema


class DataSchema(Schema):
    procedure = fields.Dict()
    function = fields.Dict()
    statement = fields.Dict()


class Data(MethodResource, Resource):
    @doc(description="Get pre-comp data", tags=["Data"])
    @use_kwargs(DataSchema, location="json")
    def post(self, **kwargs):
        data = kwargs
        out = []
        print(data)
        if "procedure" in data:
            procedure = data["procedure"]
            out = call_procedure(name=procedure["name"], params=procedure["params"])
        elif "function" in data:
            function = data["function"]
            out = call_function(name=function["name"], params=function["params"])
        elif "statement" in data:
            statement = data["statement"]
            out = call_statement(query=statement["query"])
        return out
