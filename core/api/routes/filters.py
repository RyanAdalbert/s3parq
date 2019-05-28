from core.helpers.session_helper import SessionHelper as SHelp
import requests, sqlalchemy.orm, json
from flask import Blueprint, request
import core.api.routes.auth as auth
from core.models.configuration import (
    Pipeline,
    Brand,
    PharmaceuticalCompany
)

bp = Blueprint('filters', __name__)

@bp.route('/filters', methods=['GET'])
def filters():
    if not "Authorization" in request.headers:
        return "Login token not specified.", 401
    if not auth.check_cookie(request.headers.get('Authorization')):
        return "Invalid session token.", 403
    helper = SHelp()
    sess = helper.session
    query = sess.query(Pipeline).all()
    filters = {}
    brands = set()
    companies = set()
    types = set()
    status = set()
    for pl in query:
      brands.add(pl.brand.name)
      companies.add(pl.brand.pharmaceutical_company.name)
      types.add(pl.pipeline_type.name)
      if pl.is_active:
        status.add('Active')
      else:
        status.add('Inactive')
    filters['brands'] = brands
    filters['companies'] = companies
    filters['types'] = types
    filters['status'] = status
    mainObj = {"data" : filters}
    return json.dumps(mainObj), 200