# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hmac
import hashlib
import logging
import pprint
import requests
import base64
import psycopg2

from werkzeug.exceptions import Forbidden

import json
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.addons.website_sale.controllers.main import PaymentPortal
from odoo.addons.payment_paytr_kt.paytr import send

_logger = logging.getLogger(__name__)


class PayTRController(http.Controller):
    _return_url = '/payment/paytr/return'
    _iframe_token = '/payment/paytr/get-iframe-token'

    @http.route(_iframe_token, type='json', auth='public')
    def get_iframe_token(self, **data):
        """ Simulate the response of a payment request.

        :param dict data: The simulated notification data.
        :return: None
        """
        ref = data.get('reference')
        tx_sudo = request.env['payment.transaction'].sudo().search([('reference', '=', ref)])
        if tx_sudo.provider_reference:
            return {'token': tx_sudo.provider_reference}
        else:
            IP = request.httprequest.remote_addr
            payload = tx_sudo.provider_id._paytr_generate_vals(tx_sudo, IP)
            code, resp = send(payload)
            if code == -200:
                raise ValidationError("Lisans süreniz sona erdi.\nLütfen destek için Kitayazilim ile iletişime geçin")
            elif code == -100:
                raise ValidationError("Kullandığınız lisans geçersizdir.\nLütfen geçerli bir lisans anahtarı giriniz veya destek almak için Kitayazilim ile iletişime geçiniz")
            elif code == -1:
                raise ValidationError("PayTR ile bağlantı sağlanamıyor.\nLütfen internet bağlantınızı kontrol edin ve tekrar deneyin.\nSorun devam ederse, destek almak için Kitayazilim ile iletişime geçiniz.")
            elif code != 200:
                error = f"Hata oluştu! Status: {code}"
                _logger.warning("PayTR. Error: %s", error)
                raise ValidationError(f"PayTR. Error: {error}")

            res = json.loads(resp)
            if res["status"] == "success":
                tx_sudo.provider_reference = res.get('token')
                return res
            else:
                raise ValidationError(res["reason"])

    @http.route(
        _return_url, type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def paytr_return_from_checkout(self, **data):
        """ Process the notification data sent by Buckaroo after redirection from checkout.

        The route is flagged with `save_session=False` to prevent Odoo from assigning a new session
        to the user if they are redirected to this route with a POST request. Indeed, as the session
        cookie is created without a `SameSite` attribute, some browsers that don't implement the
        recommended default `SameSite=Lax` behavior will not include the cookie in the redirection
        request from the payment provider to Odoo. As the redirection to the '/payment/status' page
        will satisfy any specification of the `SameSite` attribute, the session of the user will be
        retrieved and with it the transaction which will be immediately post-processed.

        :param dict raw_data: The un-formatted notification data
        """
        _logger.info("handling redirection from PayTR with data:\n%s", pprint.pformat(data))

        # Check the integrity of the notification
        received_signature = data.get('hash')
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
            'paytr', data
        )
        self._verify_notification_signature(data, received_signature, tx_sudo)

        # Handle the notification data
        tx_sudo._handle_notification_data('paytr', data)
        return "OK"

    @staticmethod
    def _verify_notification_signature(notification_data, received_signature, tx_sudo):
        """ Check that the received signature matches the expected one.

        :param dict notification_data: The notification data
        :param str received_signature: The signature received with the notification data
        :param recordset tx_sudo: The sudoed transaction referenced by the notification data, as a
                                  `payment.transaction` record
        :return: None
        :raise: :class:`werkzeug.exceptions.Forbidden` if the signatures don't match
        """
        # Check for the received signature
        if not received_signature:
            _logger.warning("received notification with missing signature")
            raise Forbidden()

        hash_str = notification_data['merchant_oid'] + tx_sudo.provider_id.paytr_merchant_salt + notification_data['status'] + notification_data['total_amount']
        expected_signature = base64.b64encode(hmac.new(tx_sudo.provider_id.paytr_merchant_key.encode(), hash_str.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(received_signature.encode(), expected_signature):
            _logger.warning("received notification with invalid signature")
            raise Forbidden()


class PaymentPortalMondialRelay(PaymentPortal):

    @http.route()
    def shop_payment_transaction(self, *args, **kwargs):
        try:
            return super().shop_payment_transaction(*args, **kwargs)
        except psycopg2.errors.UniqueViolation as e:
            last_tx_id = request.session.get('__website_sale_last_tx_id')
            last_tx = request.env['payment.transaction'].browse(last_tx_id).sudo().exists()
            if last_tx and last_tx.provider_id.code == 'paytr' and last_tx.provider_reference and last_tx.state == 'draft':
                return last_tx._get_processing_values()
            else:
                raise e
