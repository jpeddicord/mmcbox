from functools import wraps

from flask import request, render_template, abort
from flask.ext.login import current_user

from mmc.models import Website


def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def check_domain():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            domain = request.view_args.get('domain')
            if domain:
                w = Website.query.filter_by(domain=domain).first()
                if w and w.user.id == current_user.id:
                    return f(*args, **kwargs)
            return abort(404)

