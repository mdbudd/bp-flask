# from flask import Flask
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields


class AwesomeResponseSchema(Schema):
    message = fields.Str(default="Success")


class AwesomeRequestSchema(Schema):
    api_type = fields.String(
        required=True, description="API type of awesome API"
    )


#  Restful way of creating APIs through Flask Restful
class AwesomeAPI(MethodResource, Resource):
    @doc(description="My First GET Awesome API.", tags=["Awesome"])
    @marshal_with(AwesomeResponseSchema)  # marshalling
    def get(self):
        """
        Get method represents a GET API method
        """
        return {"message": "Example API"}

    @doc(description="My First GET Awesome API.", tags=["Awesome"])
    @use_kwargs(AwesomeRequestSchema, location=("json"))
    @marshal_with(AwesomeResponseSchema)  # marshalling
    def post(self, **kwargs):
        """
        Get method represents a GET API method
        """
        return {"message": "Example API"}
