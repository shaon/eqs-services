from flask import Flask
from eqs_services.views import general, jenkins

from eqs_services import views

app = Flask(__name__)

app.config.from_object('config')

app.register_blueprint(general.machine_views)
app.register_blueprint(jenkins.jenkins_view)
