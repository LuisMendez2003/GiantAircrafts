from flask import Flask
from services.endpoints import api

#Initializing
app = Flask(__name__)
app.register_blueprint(api)


#Main
if __name__ == "__main__":
    app.run(debug = True)
