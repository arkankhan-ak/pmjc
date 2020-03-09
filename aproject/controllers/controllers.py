# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Aproject(http.Controller):
    @http.route('/aproject/helloworld/',type="http", auth='public')
    def index(self, **kw):
        return "Hello, world, Arkankhan"


    @http.route('/aproject/work_item_details',type='http',auth='public',website='true')
    def get_timesheet_details(self,**kwargs):
        workitem_list = request.env['project.task'].sudo().search([])
        print(workitem_list)
        return request.render('../views/work_items_page',{'work_items':workitem_list})

    # @http.route('/aproject/aproject/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('aproject.listing', {
    #         'root': '/aproject/aproject',
    #         'objects': http.request.env['aproject.aproject'].search([]),
    #     })
    #
    # @http.route('/aproject/aproject/objects/<model("aproject.aproject"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('aproject.object', {
    #         'object': obj
    #     })