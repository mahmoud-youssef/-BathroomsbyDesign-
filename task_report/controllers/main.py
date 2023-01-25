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
        users_ids = []
        # WE Can make an auth here or pagination
        tasks = request.env['project.task'].sudo().search([])
        for task in tasks:
            projects_ids = []
            if task.user_id.id not in users_ids:
                users_ids.append(task.user_id.id)
                tasks_per_user = request.env['project.task'].sudo().search([('user_id','=',task.user_id.id)])
                subData = {
                    'user_id': task.user_id.id,
                    'projects': [],
                    'name': task.user_id.name,
                    'image': task.user_id.image
                }
                for task_per_user in tasks_per_user:
                    if task_per_user.project_id.id not in projects_ids:
                        projects_ids.append(task_per_user.project_id.id)
                        subDataPro = {
                                'id': task_per_user.project_id.id,
                                'delay_tasks': task_per_user.delay_tasks,
                                'past_week_finished_tasks': task_per_user.past_week_finished_tasks,
                                'current_month_finished_tasks': task_per_user.current_month_finished_tasks,
                        }
                        subData['projects'].append(subDataPro)
                data.append(subData)

        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'message': data}}

        return Response(json.dumps(body), headers=headers)
