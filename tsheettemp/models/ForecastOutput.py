from odoo import api,fields, models,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as obtained_system_date_format
import datetime
class ForecastOutput(models.TransientModel):
    _name = 'project.forecastoutput'
    _description = 'Forecast Output'

    date = fields.Date(
        string='Date',
        required=False)
    employee = fields.Char(
        string='Employee',
        required=False)
    amount = fields.Float(
        string='Rate',
        required=False)

    def test_function(self):
        all_forecast_input = self.env['project.forecasting'].search([])
        print("----------",all_forecast_input)
        for current_forecast in all_forecast_input:
            employee_name = current_forecast.employee_name
            print(current_forecast.employee_name)
            print()
            print(employee_name)
            start = datetime.datetime.strptime(current_forecast.from_date, obtained_system_date_format)
            end = datetime.datetime.strptime(current_forecast.to_date, obtained_system_date_format)
    
            delta = end - start
    
            for i in range(delta.days + 1):
                single_date = (start + datetime.timedelta(days=i)).date()
                print(single_date, employee_name, 2000)
                self.env['project.forecastoutput'].create({
                    'date': single_date,
                    'employee': employee_name,
                    'amount': 2000
                })
                view_id = self.env['ir.model.data'].get_object_reference('tsheettemp', 'forecast_output_view_tree')[1]
        return {
            'name': ('Forecasting output of Input'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'view_id': view_id,
            'res_model': 'project.forecastoutput',
            'target':'new'
        }