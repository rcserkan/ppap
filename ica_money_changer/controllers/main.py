from odoo.http import request, route, Controller


class MoneyChangerController(Controller):
    @route("/ica/ica-money-changer", auth="public")
    def standalone_app(self):
        return request.render(
            'ica_money_changer.standalone_app',
            {
                'session_info': request.env['ir.http'].get_frontend_session_info(),
            }
        )

    @route("/ica/login", auth="none", type="json")
    def login(self, *args, **kwargs):
        try:
            username = kwargs.get('username')
            password = kwargs.get('password')
            request.session.authenticate(request.session.db, username, password)
            return {'isFullFilled': True, "message": "Login Successfully."}
        except Exception as e:
            return {'isFullFilled': False, "message": str(e)}

    @route("/ica/logout", auth="user", type="json")
    def logout(self, *args, **kwargs):
        try:
            request.session.logout()
            return {'isFullFilled': True, "message": "Login Successfully."}
        except Exception as e:
            return {'isFullFilled': False, "message": str(e)}

