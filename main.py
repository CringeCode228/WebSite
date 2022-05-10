from app import application
from app import views
from app import models


if __name__ == "__main__":
    application.run(host="127.0.0.1", port=5000, debug=True)
