# -*- coding: utf-8 -*-
from odoo import api, fields, models

class BilanReportWizard(models.TransientModel):
    _name = 'bilan.report.wizard'

    mois = fields.Selection([
        ('janvier', 'يناير'),
        ('fevrier', 'فبراير'),
        ('mars', 'مارس'),
        ('avril', 'أبريل'),
        ('mai', 'ماي'),
        ('juin', 'يونيو'),
        ('juillet', 'يوليو'),
        ('aout', 'غشت'),
        ('septembre', 'شتنبِر'),
        ('octobre', 'اكتوبر'),
        ('novembre', 'نونبِر'),
        ('decembre', 'دجنبر'),
    ], string="الشهر", required=True)

    type_infraction = fields.Selection([
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3'),
        ('type4', 'Type 4'),
    ], string="نوع المخالفة" , required=True)

    def print_report(self):
        self.ensure_one()
        record_ids = self.env['bilan'].search([('mois', '=', self.mois),('type_infraction', '=', self.type_infraction)])
        data = {
            'record_ids' : record_ids
            }
        return self.env.ref('bilan_mensuel.action_bilan_report_pdf').report_action(self, data=data)
