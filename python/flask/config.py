import json
import platform
import pandas as pd
import os
import configparser
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# from flask_apispec.extension import FlaskApiSpec

config = configparser.ConfigParser()
config.read("/python/flask/envfile.ini")
print(config["DEFAULT"]["DEBUG"])

debug = config["DEFAULT"]["DEBUG"]
context = config["DEFAULT"]["CONTEXT"]
sslSet = config["DEFAULT"]["SSLSET"]
port = config["DEFAULT"]["PORT"]

if sslSet == "None":
    sslSet = None
if context == "None":
    context = None
if debug == "True":
    debug = True

oracle_username = config["DEFAULT"]["ORACLE_USERNAME"]
oracle_password = config["DEFAULT"]["ORACLE_PASSWORD"]
ORACLEDB = config["DEFAULT"]["ORACLEDB"]
oracle_host = config["DEFAULT"]["ORACLE_HOST"]
oracle_port = config["DEFAULT"]["ORACLE_PORT"]
oracle_client = config["DEFAULT"]["ORACLE_CLIENT"]
dsnStr = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={})(PORT={}))(CONNECT_DATA=(SERVICE_NAME={})))".format(oracle_host, oracle_port, ORACLEDB)

DATABASE_URL = "oracle://" + oracle_username + ":" + oracle_password + "@" + dsnStr

jwt_secret = config["DEFAULT"]["JWT_SECRET"]

ldaps_host = config["DEFAULT"]["LDAPS_HOST"]
ldaps_port = config["DEFAULT"]["LDAPS_PORT"]
ldap_europa = config["DEFAULT"]["LDAP_EUROPA"]
ldap_fm = config["DEFAULT"]["LDAP_FM"]
ldap_user = config["DEFAULT"]["LDAP_USER"]
ldap_pass = config["DEFAULT"]["LDAP_PASS"]
ldap_fmuser = config["DEFAULT"]["LDAP_FM_USER"]
ldap_fmpass = config["DEFAULT"]["LDAP_FM_PASS"]

mod_path = config["DEFAULT"]["MOD_PATH"]
# admin_un = config["DEFAULT"]["ADMIN_UN"]
# admin_srn = config["DEFAULT"]["ADMIN_SRN"]
# admin_dm = config["DEFAULT"]["ADMIN_DM"]
super_un = config["DEFAULT"]["SUPER1_DM"]
super_srn = config["DEFAULT"]["SUPER1_SRN"]
super_dm = config["DEFAULT"]["SUPER1_DM"]
admin_un = config["DEFAULT"]["ADMIN_UN"]
admin_srn = config["DEFAULT"]["ADMIN_SRN"]
admin_dm = config["DEFAULT"]["ADMIN_DM"]
test_srn = config["DEFAULT"]["TEST_SRN"]
test_position = config["DEFAULT"]["TEST_POSITION"]
test_start = config["DEFAULT"]["TEST_START"]
test_racf = config["DEFAULT"]["TEST_RACF"]

if os.getenv("VCAP_APPLICATION"):
    context = None
    spacename = json.loads(os.getenv("VCAP_APPLICATION", "{}")).get("space_name")

    if spacename == "PRD":
        debug = False
        ORACLEDB = "XXXX.XXXX"
    elif spacename == "DEV":
        debug = True
    elif spacename == "UAT":
        debug = False
    elif spacename == "DEV-SANDBOX":
        debug = False

# if platform.system() in ["Linux", "Windows"]:
if platform.system() in ["Linux"]:
    sslSet = ("certs/cloudcert.pem", "certs/cloudcert.key")
    # port = 443
