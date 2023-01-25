# -*- coding: utf-8 -*-
import datetime
import json
import logging
import select
import threading
import time
import random

import simplejson
import openerp
from openerp.osv import osv ,fields
from openerp import api, _
from openerp.http import request
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

TIMEOUT = 50

def json_dump(v):
    return simplejson.dumps(v, separators=(',', ':'))

def hashable(key):
    if isinstance(key, list):
        key = tuple(key)
    return key

class ImBus(osv.Model):
    _inherit = 'project.task'

    @api.multi
    @api.depends('open_tasks','stage_id')
    def _compute_open_tasks(self):
        print("Sdsds")
        for rec in self:
            if rec.id:
                rec.open_tasks = rec.search_count([('stage_id', '!=', 7), ('user_id', '=', rec.user_id.id), ('project_id', '=', rec.project_id.id)])
                print("Open Tasks",rec.open_tasks)
            else:
                self.open_tasks = 0

    @api.multi
    @api.depends('delay_tasks','stage_id')
    def _compute_delay_tasks(self):
        for rec in self:
            if rec.id:
                current_date = datetime.date.today()
                print("D Tasks", current_date)
                rec.delay_tasks = rec.search_count([('stage_id', '!=', 7), ('user_id', '=', rec.user_id.id), ('project_id', '=', rec.project_id.id), ('date_deadline', '<', current_date)])
                print("D Tasks", rec.delay_tasks)
            else:
                rec.delay_tasks = 0

    @api.multi
    @api.depends('past_week_finished_tasks','stage_id')
    def _compute_finish_week(self):
        for rec in self:
            if rec.id:
                today = datetime.date.today()
                weekday = today.weekday()
                start_delta = datetime.timedelta(days=weekday, weeks=1)
                end_delta = datetime.timedelta(days=weekday, weeks=0)
                start_of_past_week = today - start_delta
                end_of_past_week = today - end_delta
                print("W Tasks", start_of_past_week, end_of_past_week)

                rec.past_week_finished_tasks = rec.search_count(
                        [('stage_id', '=', 7), ('user_id', '=', rec.user_id.id), ('date_deadline', '>=', start_of_past_week), ('project_id', '=', rec.project_id.id), ('date_deadline', '<', end_of_past_week)])
                print("W Tasks", rec.past_week_finished_tasks)
            else:
                rec.past_week_finished_tasks = 0

    @api.multi
    @api.depends('current_month_finished_tasks','stage_id')
    def _compute_finish_month(self):
        for rec in self:
            if rec.id:
                current_date = datetime.date.today()
                start_of_current_month = current_date.replace(day=1)
                # add 31 days to the input datetime
                res = current_date + relativedelta(day=31)
                last_of_the_current_month = res

                print("M Tasks", start_of_current_month,last_of_the_current_month)
                rec.current_month_finished_tasks = rec.search_count(
                        [('stage_id', '=', 7), ('user_id', '=', rec.user_id.id), ('project_id', '=', rec.project_id.id), ('date_deadline', '>=', start_of_current_month),
                         ('date_deadline', '<=', last_of_the_current_month)])
                print("M Tasks", rec.current_month_finished_tasks)
            else:
                rec.current_month_finished_tasks = 0

    _columns = {
        'user_image': fields.related('user_id', 'image', string="Image", type="binary"),
        'open_tasks': fields.integer('Open',compute='_compute_open_tasks'),
        'delay_tasks': fields.integer('Delay', compute="_compute_delay_tasks"),
        'past_week_finished_tasks': fields.integer('finish-week:', compute="_compute_finish_week"),
        'current_month_finished_tasks': fields.integer('finish-month:', compute="_compute_finish_month"),
    }

