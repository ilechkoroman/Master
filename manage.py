import argparse
import os

from app import create_app

app = create_app(os.environ.get("FLASK_CONFIG", "default"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",
                        type=str,
                        default="0.0.0.0")
    parser.add_argument("--port",
                        type=int,
                        default=5000)
    args = parser.parse_args()
    app.run(host=args.host,
            port=args.port)
