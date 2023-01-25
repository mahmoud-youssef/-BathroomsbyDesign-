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
from openerp.osv import osv, fields
from openerp import api, _
from openerp.http import request
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

TIMEOUT = 50

#----------------------------------------------------------
# Bus
#----------------------------------------------------------
def json_dump(v):
    return simplejson.dumps(v, separators=(',', ':'))

def hashable(key):
    if isinstance(key, list):
        key = tuple(key)
    return key

class ImBus(osv.Model):
    _inherit = 'project.task'


    _columns = {
        'user_image': fields.related('user_id', 'image', string="Image", type="binary"),
        # 'user_image': fields.binary('Image', compute='_compute_user_image'),
    }

    @api.one
    @api.depends('user_image')
    def _compute_user_image(self):
        print (self.user_id)
        for rec in self:
            if rec.user_id:
                rec.user_image = rec.user_id.image
