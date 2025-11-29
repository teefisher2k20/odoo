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
                dbs = http.db_list()
                if dbs:
                    # Use the first database found
                    db = dbs[0]
                    
                    # Authenticate as admin
                    # Note: In Odoo 18, authenticate takes a credential dict
                    credential = {'login': 'admin', 'password': 'admin', 'type': 'password'}
                    auth_info = request.session.authenticate(db, credential)
                    
                    if auth_info and auth_info.get('uid'):
                        request.params['login_success'] = True
                        return request.redirect(self._login_redirect(auth_info['uid'], redirect=redirect))
            except Exception as e:
                # Fallback to normal login if anything goes wrong
                pass 

        return super(AutoLogin, self).web_login(redirect=redirect, **kw)
