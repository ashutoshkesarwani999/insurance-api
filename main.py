import uvicorn
import argparse

from core.config import config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI server")
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(
        app="core.server:app",
        host="0.0.0.0",
        port=args.port,
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1,
    )
