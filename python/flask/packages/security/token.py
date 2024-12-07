def getTykTokenPayload(token):
    from .jwks import JwkStore
    from config import jwks_url
    import jwt
    import datetime
    from cryptography.hazmat.primitives import serialization

    url = jwks_url
    key = ""
    payload = ""
    # token = ""
    alg = "ES256"
    kid = jwt.get_unverified_header(token)["kid"]
    alg = jwt.get_unverified_header(token)["alg"]
    keyStore = JwkStore(url, 5 * 60, 4 * 3600)
    key = (
        keyStore.get(kid, "RS256")
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode()
    )
    payload = jwt.decode(
        token,
        key=key,
        options={"verify_exp": False},
        issuer="InternalGateway",
        audience="my-security",
        algorithms=["ES256"],
    )
    expToNow = (payload["exp"] + 600) - datetime.datetime.now(
        datetime.timezone.utc
    ).timestamp()  # 10 minutes leeway as token expires v quickly!
    print(expToNow)
    if expToNow < 0:
        return None
    return payload


def createToken():
    import jwt
    import datetime

    from cryptography.hazmat.primitives import serialization

    payload = {
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=7, seconds=0),
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "id": 123,
        "imp": False,
        "roles": ["admin"],
    }

    with open("certs/privateKey.key", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    key = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    return jwt.encode(payload, key, algorithm="ES256")
