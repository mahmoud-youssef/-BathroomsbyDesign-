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
        projects_ids = []
        tasks_ids = []
        # WE Can make an auth here or pagination
        tasks = request.env['project.task'].sudo().search([])
        for task in tasks:
            task_obj = []
            project_obj = {}
            if task.user_id.id not in users_ids:
                users_ids.append(task.user_id.id)
                projects_ids.append({
                    task.user_id.id : [task.project_id.id]
                })
                subData = {
                    'user_id': task.user_id.id,
                    'projects': [{
                        'id': task.project_id.id,
                        'delay_tasks': task.delay_tasks,
                    }],
                    'name': task.user_id.name,
                }
                data.append(subData)
            else:
                for projects_id in projects_ids:
                    print (projects_id.get(task.user_id.id))
                    if projects_id.get(task.user_id.id) and task.project_id.id not in projects_id.get(task.user_id.id):
                        projects_id.get(task.user_id.id).append(task.project_id.id)
                        subData = {
                            'user_id': task.user_id.id,
                            'projects': [{
                                'id': task.project_id.id,
                                'delay_tasks': task.delay_tasks,
                            }],
                            'name': task.user_id.name,
                        }
                        data.append(subData)



        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'message': data}}

        return Response(json.dumps(body), headers=headers)
