import requests
import time
import jwt.algorithms
import jwt
from math import inf
from typing import Optional
from typing import Dict
import logging
import threading

logger = logging.getLogger(__name__)


class JwksStore:
    def __init__(
        self, url: str, refresh_not_sooner_than_s: int, refresh_not_later_than_s: int
    ):
        self.lock = threading.Lock()
        print(self.lock)
        self.public_keys: Optional[Dict] = None
        self.updated = inf
        self.url = url
        # refresh after refresh_not_later_than_s to mitigate the risk of using a known compromised key
        # and refresh when a key is not found, but sooner than refresh_not_sooner_than_s after last download attempt
        assert refresh_not_sooner_than_s <= refresh_not_later_than_s
        self.refresh_not_sooner_than_s = refresh_not_sooner_than_s
        self.refresh_not_later_than_s = refresh_not_later_than_s

    def _locked_download_jwks(self):
        logger.info(
            "Downloading JDKS url=%r, time since update %r",
            self.url,
            time.monotonic() - self.updated,
        )
        self.updated = time.monotonic()
        r = requests.get(self.url, verify=False)
        logger.debug("Downloaded JWKS")
        jwks = r.json()
        logger.debug("Downloaded JWKS, number of keys %r", len(jwks["keys"]))
        return jwks

    def _locked_update(self):
        jwks = self._locked_download_jwks()
        # discard previous key set in case is it was compromised and then regenerated
        self.public_keys = {}
        # inspried by https://renzolucioni.com/verifying-jwts-with-jwks-and-pyjwt
        for jwk in jwks["keys"]:
            self.maybe_add_key(jwk)

    def maybe_add_key(self, jwk):
        if "use" in jwk and jwk["use"] != "sig":
            return False
        curr_kid = jwk["kid"]
        cache_key = (curr_kid, jwk["alg"])
        # ignore keys with key types not supported as per RFC 7517, section 5
        if jwk["kty"] == "EC":
            self.public_keys[cache_key] = jwt.algorithms.ECAlgorithm.from_jwk(jwk)
            return True
        return False

    def get(self, kid: str, alg: str):
        cache_key = (kid, alg)
        with self.lock:
            now = time.monotonic()
            if self.updated + self.refresh_not_later_than_s < now:
                self.public_keys = None
            if (
                self.public_keys is None
                or cache_key not in self.public_keys
                and self.updated + self.refresh_not_sooner_than_s < now
            ):
                self.public_keys = {}
                self._locked_update()
            return self.public_keys[cache_key]
