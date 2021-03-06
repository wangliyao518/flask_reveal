from flask import g, Blueprint
from flask.ext.login import login_user

from social.actions import do_auth, do_complete, do_disconnect
from social.apps.flask_app.utils import strategy


social_auth = Blueprint('social', __name__)


@social_auth.route('/login/<string:backend>/', methods=['GET', 'POST'])
@strategy('social.complete')
def auth(backend):
    return do_auth(g.strategy)


@social_auth.route('/complete/<string:backend>/', methods=['GET', 'POST'])
@strategy('social.complete')
def complete(backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    return do_complete(g.strategy, login=lambda strat, user: login_user(user),
                       user=g.user, *args, **kwargs)


@social_auth.route('/disconnect/<string:backend>/', methods=['POST'])
@social_auth.route('/disconnect/<string:backend>/<string:association_id>/',
                   methods=['POST'])
@strategy()
def disconnect(backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(g.strategy, g.user, association_id)
