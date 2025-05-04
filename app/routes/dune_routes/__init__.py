from flask import Blueprint

dune_bp = Blueprint('dune', __name__)

from . import routes 