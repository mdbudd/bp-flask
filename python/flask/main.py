import os
from api.app import api, app, docs
from config import port as port_dev, debug, context
from resources.awesome import AwesomeAPI

port = int(os.getenv("PORT", port_dev))



if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=port, debug=debug, use_reloader=True, ssl_context=context
    )
