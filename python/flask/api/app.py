from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api
from resources import resourceList

version = "v0"
app = Flask(__name__)
api = Api(app, prefix="/api/" + version)

spec = APISpec(
    title="Example API",
    info={
        "description": "Example API",
    },
    version=version,
    plugins=[MarshmallowPlugin()],
    openapi_version="2.0.0",
    # openapi_version="3.0.2",
)
api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

# spec.components.security_scheme("api_key", api_key_scheme)
# spec.components.security_scheme("jwt", jwt_scheme)
# print(spec.to_dict()["components"]["securitySchemes"])

app.config.update(
    {
        "APISPEC_SPEC": spec,
        "APISPEC_SWAGGER_URL": "/swagger.json",
        "APISPEC_SWAGGER_UI_URL": "/swag",
    }
)

docs = FlaskApiSpec(app)

for resource in resourceList:
    api.add_resource(resource["class"], *resource["route(s)"])
    docs.register(resource["class"])
