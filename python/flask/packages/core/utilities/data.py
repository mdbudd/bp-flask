import pandas as pd
import json
from api.db import db, engine


class ThreadManager:
    def __init__(self):
        self.managers = []

    def getManagers(self, manager, GetActivePositionManagementByManagerId):
        posMan = GetActivePositionManagementByManagerId(manager["position_id"])
        manager["reportee_count"] = len(posMan)
        self.managers.append(manager)


def call_procedure(name, params):
    import cx_Oracle

    results = []
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        out = cursor.var(cx_Oracle.CURSOR)
        params = [out if x == "cursor" else x for x in params]
        cursor.callproc(name, params)
        data = out.getvalue().fetchall()
        cursor.close()
        connection.commit()
        if len(data) == 0:
            data = {}
        df = pd.DataFrame(data, columns=[i[0] for i in out.getvalue().description])
        df.columns = map(str.lower, df.columns)
        return json.loads(df.to_json(orient="records"))
    except Exception as e:
        return {"message": "No corresponding procedure found."}, 404
    finally:
        connection.close()


def call_function(name, params):
    results = []
    try:
        conn = engine.connect()
        result = conn.execute(name, params).all()
        for r in result:
            results = dict(r._mapping)
    except Exception as e:
        return {"error": e}, 404
    return results


def get_func_val(dictionary):
    return list(dictionary.values())[0]


def call_statement(query, as_df=False):
    df = pd.read_sql(query, engine)
    df.columns = map(str.lower, df.columns)
    if "start_date" in df.columns:
        df["start_date"] = df["start_date"].astype("string")
    if "end_date" in df.columns:
        df["end_date"] = df["end_date"].astype("string")
    result = df
    if not as_df:
        result = json.loads(df.to_json(orient="records"))
    return result


def upsert_statement(sql):
    result = engine.execute(sql)
    return result


def phrase_caps(phrase):
    new_s = phrase.title()
    return new_s


def snake_to_camel(str):
    components = str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def keys_to_camel(test_dict):
    res = dict()
    for key in test_dict.keys():
        newKey = snake_to_camel(key)
        if isinstance(test_dict[key], dict):
            res[newKey] = keys_to_camel(test_dict[key])
        else:

            if isinstance(test_dict[key], list):
                innerRes = []
                for item in test_dict[key]:
                    if isinstance(item, dict):
                        innerRes.append(keys_to_camel(item))
                    else:
                        innerRes.append(item)
                res[newKey] = innerRes
            else:
                res[newKey] = test_dict[key]
    return res


def data_handler(obj):
    import datetime

    return (
        obj.isoformat() if isinstance(obj, (datetime.datetime, datetime.date)) else None
    )


def try_parsing_date(text):
    from datetime import datetime

    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).strftime("%d/%m/%Y")
        except ValueError:
            pass
    raise ValueError("No valid date format found.")
