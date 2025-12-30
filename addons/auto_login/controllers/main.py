from odoo.addons.web.controllers.home import Home
from odoo import http
from odoo.http import request


class AutoLogin(Home):

    @http.route('/web/login', type='http', auth='none', readonly=False)
    def web_login(self, redirect=None, **kw):
        # If already logged in, let the super method handle the redirect
        if request.session.uid:
            return super(AutoLogin, self).web_login(redirect=redirect, **kw)

        # Attempt Auto Login
        if request.httprequest.method == 'GET':
            try:
                # Get available databases
                dbs = []
                try:
                    dbs = http.db_list()
                except Exception:
                    # db_list might be disabled
                    pass

                if not dbs and http.tools.config['db_name']:
                    dbs = http.tools.config['db_name'].split(',')

                if dbs:
                    # Use the first database found
                    db = dbs[0]

                    # Authenticate using system parameters or defaults
                    ICPSudo = request.env['ir.config_parameter'].sudo()
                    login = ICPSudo.get_param('auto_login.username', 'admin')
                    password = ICPSudo.get_param(
                        'auto_login.password', 'admin'
                    )

                    credential = {
                        'login': login,
                        'password': password,
                        'type': 'password'
                    }
                    auth_info = request.session.authenticate(db, credential)

                    if auth_info and auth_info.get('uid'):
                        request.params['login_success'] = True
                        return request.redirect(
                            self._login_redirect(
                                auth_info['uid'], redirect=redirect
                            )
                        )
            except Exception:
                # Fallback to normal login if anything goes wrong
                pass

        return super(AutoLogin, self).web_login(redirect=redirect, **kw)
