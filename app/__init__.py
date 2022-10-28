from flask import Flask, Response

app = Flask(__name__)

from . import index  # NOQA
from . import job_endpoints  # NOQA
from . import energy_data_endpoints  # NOQA
