from core.helpers.session_helper import SessionHelper as SHelp
import requests
import sqlalchemy.orm
from flask import Flask, Blueprint, request, session
from core.models.configuration import (
    Pipeline,
    Brand,
    PharmaceuticalCompany
)

bp = Blueprint('index', __name__)