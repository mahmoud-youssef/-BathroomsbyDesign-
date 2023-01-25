import logging
import json

from openid import oidutil

import openerp.http as http
from openerp.http import request, Response

_logger = logging.getLogger(__name__)
oidutil.log = _logger.debug

class OpenIDController(http.Controller):

    @http.route('/report-task', auth='none', type='http', method=['GET'], cors='*')
    def process(self, **kw):
        data = []
        # WE Can make an auth here or pagination
        tasks = request.env['project.task'].sudo().search([])
        for task in tasks:
            subData = {
                'user_id': task.user_id.id,
                'project_id': task.project_id.id,
                'name': task.user_id.name,
                'delay_tasks': task.delay_tasks
            }
            if subData not in data:
                data.append(subData)

        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'message': data}}

        return Response(json.dumps(body), headers=headers)
