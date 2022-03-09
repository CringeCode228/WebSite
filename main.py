from app import application
from app import views
from app import models


if __name__ == "__main__":
    application.run(port=8080, debug=True)
