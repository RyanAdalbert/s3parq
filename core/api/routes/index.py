from core.helpers.session_helper import SessionHelper as SHelp
import requests, sqlalchemy.orm, json
from flask import Blueprint, request
import core.api.routes.auth as auth
from core.models.configuration import (
    Pipeline,
    Brand,
    PharmaceuticalCompany
)

bp = Blueprint('index', __name__)

@bp.route('/index', methods=['GET'])
def index():
    if not "Authorization" in request.headers:
        return "Login token not specified.", 401
    if not auth.check_cookie(request.headers.get('Authorization')):
        return "Invalid session token.", 403
    helper = SHelp()
    sess = helper.session
    query = sess.query(Pipeline).all()
    toJSON = {}
    for pl in query:
        key = pl.id
        pl_data = {}
        pl_data['name'] = pl.name
        pl_data['brand'] = pl.brand.name
        pl_data['pharma_company'] = pl.brand.pharmaceutical_company.name
        pl_data['type'] = pl.pipeline_type.name
        if pl.is_active:
            pl_data['status'] = "Active"
        else:
            pl_data['status'] = "Inactive"
        pl_data['description'] = pl.description
        pl_data['run_freq'] = pl.run_frequency
        states = []
        transforms = []
        for state in pl.pipeline_states:
            states.append(state.pipeline_state_type.name)
            for transform in state.transformations:
                transforms.append(transform.transformation_template.name)
        pl_data['states'] = states
        pl_data['transformations'] = transforms
        toJSON[key] = pl_data
    return json.dumps(toJSON), 200