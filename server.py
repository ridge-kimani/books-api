import os
import uvicorn

from app import app

port = int(os.environ.get("PORT", 5000))

uvicorn.run(app, host='0.0.0.0', port=port)

