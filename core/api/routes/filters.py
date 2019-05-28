from flask import Flask, Blueprint, request, session
from core.helpers.session_helper import SessionHelper as SHelp

bp = Blueprint('filters', __name__)