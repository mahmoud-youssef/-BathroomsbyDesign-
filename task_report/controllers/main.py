import logging
import json
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)
oidutil.log = _logger.debug

class OpenIDController(http.Controller):

    @http.route('/report-task', auth='none', type='http', method=['GET'], cors='*')
    def process(self, **kw):
        partners = request['res.partners'].sudo().search_read([])

        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'message': partners}}

        return Response(json.dumps(body), headers=headers)
