# -*- coding: utf-8 -*-
from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class BilanMensuel(models.Model):
    _name = 'bilan'
    _description = 'حصيلة محاضر المخالفات الغابوية برسم سنة 2023'
    _rec_name = 'regione'

    # Fields
    mois = fields.Selection([
        ('janvier', 'يناير'),
        ('fevrier', 'فبراير'),
        ('mars', 'مارس'),
        ('avril', 'أبريل'),
        ('mai', 'مايو'),
        ('juin', 'يونيو'),
        ('juillet', 'يوليوز'),
        ('aout', 'غشت'),
        ('septembre', 'شتنبر'),
        ('octobre', 'أكتوبر'),
        ('novembre', 'نونبر'),
        ('decembre', 'دجنبر'),
    ], string="الشهر")

    annee = fields.Selection([
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
    ], string="السنة")

    numero_proces_verbal = fields.Char(string="رقم المحضر")
    date_inspection = fields.Date(string="تاريخ المعاينة")
    nom_redacteur_proces_verbal = fields.Char(string="اسم محرر المحضر")
    nom_prenom_infraction = fields.Char(string="اسم ونسب المخالف")
    infraction = fields.Char(string="ب. و للمخالف")

    type_infraction = fields.Selection([
        ('type1', 'حجز شاحنة'),
        ('type2', 'قطع ونقل العود اليابس بدون رخصة'),
        ('type3', 'Type 3'),
        ('type4', 'Type 4'),
        ('Autres', 'أخرى'),
    ], string="نوع المخالفة")

    autres = fields.Char(string="نوع المخالفة")

    infraction_category = fields.Selection([
        ('type1', 'حجز'),
        ('type2', 'قطع و/أو حمل العود'),
        ('type3', 'Type 3'),
        ('type4', 'Type 4'),
        ('Autres', 'أخرى'),
    ], string="تصنيف المخالفة")

    autre_category = fields.Char(string="تصنيف المخالفة")

    date_cachetage_proces_verbal = fields.Date(string="تاريخ ختم المحضر")
    dif_jours_inspection_cachetage = fields.Char(compute="_compute_dif_jours",
                                                 string="الفرق بالأيام بين المعاينة والختم")
    dif_mois_inspection_cachetage = fields.Char(compute="_compute_dif_mois",
                                                string="الفرق بالأشهر بين المعاينة والختم")
    date_envoi_tribunal = fields.Date(string="تاريخ ارسال المحضر للمحكمة")
    dif_jours_cachetage_envoi_tribunal = fields.Char(compute="_compute_dif_jours_cachetage_envoi",
                                                     string="الفرق بالأيام بين الختم والارسال الى المحكمة")
    date_conciliation = fields.Date(string="تاريخ الصلح")
    montant_conciliation = fields.Float(string="مبلغ التصالح")
    date_jugement = fields.Date(string="تاريخ الحكم")
    jugement_appel = fields.Boolean(string="حكم مستأنف")
    entree_base_donnees = fields.Boolean(string="مدرجة في القاعدة المعلوماتية( نعم أو لا)")
    date_entree_base_donnees = fields.Date(string="تاريخ ادراجه في القاعدة المعلوماتية")
    dif_jours_envoi_tribunal_jugement = fields.Char(compute="_compute_dif_jours_envoi_jugement",
                                                    string="الفرق بالأيام بين الارسال الى المحكمة والحكم")
    date_notification = fields.Date(string="تاريخ التبليغ")
    date_execution = fields.Date(string="تاريخ التنفيذ")
    notes = fields.Text(string="ملاحظات")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    sanctions_propos_ids = fields.One2many(
        'propos',
        'propos_id',
        string='العقوبات المقترحة',
    )
    prison = fields.Char(string="العقوبة السجنية")

    regione = fields.Many2one('res.company', string="المديرية الجهوية")
    branch = fields.Many2one('res.branch', string="المديرية الإقليمية ")
    area = fields.Many2one('area', string="دائرة تنمية المجال الغابوي")
    forest_area = fields.Many2one('forest.area', string=" الوحدة و المركز الغابويين")

    class SanctionsPropos(models.Model):
        _name = 'propos'
        _description = 'العقوبات المقترحة'

        penalite = fields.Float(string='الغرامة بالدرهم')
        remboursement = fields.Float(string='الارجاع بالدرهم')
        compensation = fields.Float(string='التعويض بالدرهم')
        propos_id = fields.Many2one(
            'bilan',
            string='العقوبات المقترحة',
        )

    sanctions_prononce_ids = fields.One2many(
        'prononce',
        'prononce_id',
        string='العقوبات المحكومة',
    )
    prison_prononce = fields.Char(string="العقوبة السجنية")

    class SanctionsPrononce(models.Model):
        _name = 'prononce'
        _description = 'العقوبات المحكومة'

        penalite = fields.Float(string='الغرامة بالدرهم')
        remboursement = fields.Float(string='الارجاع بالدرهم')
        compensation = fields.Float(string='التعويض بالدرهم')
        prononce_id = fields.Many2one(
            'bilan',
            string='العقوبات المحكومة',
        )

    class ResCompany(models.Model):
        _inherit = 'res.company'
        parent_id = fields.Many2one('res.company', string='Parent Company', index=True, ondelete='cascade')

    class ResBranch(models.Model):
        _inherit = 'res.branch'

        branch_id = fields.Many2one('res.branch', string='Branches', index=True, ondelete='cascade')
        forest_areas = fields.One2many('forest.area', 'branch_id', string='Forest Areas')

    class ForestArea(models.Model):
        _name = 'forest.area'

        name = fields.Char(string='Forest Area')
        branch_id = fields.Many2one('res.branch', string='Branch', ondelete='cascade')
        area_id = fields.Many2one('area', string='Area')  # This field should link to area model

    class Area(models.Model):
        _name = 'area'

        name = fields.Char(string='Forest Area')
        branch_id = fields.Many2one('res.branch', string='Branch', ondelete='cascade')

    @api.onchange('regione, branch')
    def _onchange_region(self):
        if self.regione:
            return {'domain': {'regione': [('parent_id', '=', self.branch_id)]}}
        else:
            return {'domain': {'regione': []}}

    @api.onchange('branch')
    def _onchange_branch(self):
        if self.branch:
            return {'domain': {'forest_area': [('branch_id', '=', self.branch.id)],
                               'area': [('branch_id', '=', self.branch.id)]}}
        else:
            return {'domain': {'forest_area': [], 'area': []}}

    @api.onchange('area')
    def _onchange_area(self):
        if self.area:
            return {'domain': {'forest_area': [('area_id', '=', self.area.id)]}}
        else:
            return {'domain': {'forest_area': []}}

    @api.depends('date_inspection', 'date_cachetage_proces_verbal')
    def _compute_dif_jours(self):
        for record in self:
            if record.date_inspection and record.date_cachetage_proces_verbal:
                if record.date_inspection <= record.date_cachetage_proces_verbal:
                    difference = record.date_cachetage_proces_verbal - record.date_inspection
                    record.dif_jours_inspection_cachetage = f"{difference.days} أيام"
                else:
                    record.dif_jours_inspection_cachetage = "0 أيام"
                    raise UserError("يجب أن يكون تاريخ المعاينة قبل أو يساوي تاريخ الختم المحضر")
            else:
                record.dif_jours_inspection_cachetage = "0 أيام"

    @api.depends('date_inspection', 'date_cachetage_proces_verbal')
    def _compute_dif_mois(self):
        for record in self:
            if record.date_inspection and record.date_cachetage_proces_verbal:
                if record.date_inspection <= record.date_cachetage_proces_verbal:
                    difference = relativedelta(record.date_cachetage_proces_verbal, record.date_inspection)
                    difference_months = difference.years * 12 + difference.months
                    record.dif_mois_inspection_cachetage = f"{max(difference_months, 0)} أشهر"
                else:
                    record.dif_mois_inspection_cachetage = "0 أشهر"
                    raise UserError("يجب أن يكون تاريخ المعاينة قبل أو يساوي تاريخ الختم المحضر.")
            else:
                record.dif_mois_inspection_cachetage = "0 أشهر"

    @api.depends('date_cachetage_proces_verbal', 'date_envoi_tribunal')
    def _compute_dif_jours_cachetage_envoi(self):
        for record in self:
            if record.date_cachetage_proces_verbal and record.date_envoi_tribunal:
                difference = record.date_envoi_tribunal - record.date_cachetage_proces_verbal
                record.dif_jours_cachetage_envoi_tribunal = f"{difference.days} أيام"
            else:
                record.dif_jours_cachetage_envoi_tribunal = "0 أيام"

    @api.depends('date_envoi_tribunal', 'date_jugement')
    def _compute_dif_jours_envoi_jugement(self):
        for record in self:
            if record.date_envoi_tribunal and record.date_jugement:
                difference = record.date_jugement - record.date_envoi_tribunal
                record.dif_jours_envoi_tribunal_jugement = f"{difference.days} أيام"
            else:
                record.dif_jours_envoi_tribunal_jugement = "0 أيام"

    @api.onchange('type_infraction,autres')
    def _onchange_autres(self):
        if self.type_infraction == 'Autres':
            self.autres = True
        else:
            self.autres = False

    @api.onchange('infraction_category,autre_category')
    def _onchange_autres(self):
        if self.infraction_category == 'Autres':
            self.autre_category = True
        else:
            self.autre_category = False


