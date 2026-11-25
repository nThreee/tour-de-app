import os

from dotenv import load_dotenv

_ = load_dotenv()

from app import create_app, init_db  # pyright: ignore[reportImplicitRelativeImport]

app = create_app()
init_db(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
