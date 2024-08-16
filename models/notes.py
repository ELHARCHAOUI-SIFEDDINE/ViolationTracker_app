# -*- coding: utf-8 -*-
# notes.py

# Concepts et Techniques Avancés dans le module 'bilan.py'

"""
1. Méthodes de Calcul (`@api.depends`):
   ------------------------------------
   Odoo utilise le décorateur `@api.depends` pour définir des méthodes de calcul. Ces méthodes mettent
   automatiquement à jour la valeur d'un champ lorsque les champs spécifiés dans le décorateur changent.

   Exemple dans `bilan.py`:
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

   Explication:
   - Le décorateur `@api.depends` indique à Odoo que la méthode `_compute_dif_jours` dépend des champs
     `date_inspection` et `date_cachetage_proces_verbal`.
   - Lorsque l'un de ces champs change, Odoo appelle automatiquement la méthode de calcul pour recalculer
     la valeur de `dif_jours_inspection_cachetage`.
   - Cette méthode calcule la différence en jours entre les deux dates et met à jour le champ.
   - Si `date_inspection` est postérieure à `date_cachetage_proces_verbal`, elle déclenche une `UserError`.

2. Méthodes Onchange (`@api.onchange`):
   -------------------------------------
   Le décorateur `@api.onchange` dans Odoo est utilisé pour définir des méthodes qui doivent être exécutées
   lorsque des champs spécifiques changent. Ces méthodes peuvent mettre à jour dynamiquement d'autres champs
   ou fournir une validation.

   Exemple dans `bilan.py`:
   @api.onchange('regione, branch')
   def _onchange_region(self):
       if self.regione:
           return {'domain': {'regione': [('parent_id', '=', self.branch_id)]}}
       else:
           return {'domain': {'regione': []}}

   Explication:
   - Le décorateur `@api.onchange` déclenche la méthode `_onchange_region` chaque fois que les champs `regione`
     ou `branch` changent.
   - Cette méthode définit dynamiquement le domaine du champ `regione` en fonction de la valeur du champ `branch_id`.
   - Si `regione` est défini, il retourne un domaine qui filtre `regione` par `parent_id`.
   - Si `regione` n'est pas défini, il retourne un domaine vide, rendant tous les enregistrements sélectionnables.

3. Héritage et Extension (`_inherit`):
   ------------------------------------
   Odoo permet aux modèles d'hériter et d'étendre les modèles existants en utilisant l'attribut `_inherit`.
   Cela permet d'ajouter des champs et des méthodes personnalisés aux modèles standard.

   Exemple dans `bilan.py`:
   class ResCompany(models.Model):
       _inherit = 'res.company'
       parent_id = fields.Many2one('res.company', string='Parent Company', index=True, ondelete='cascade')

   Explication:
   - La classe `ResCompany` hérite du modèle existant `res.company`.
   - L'attribut `_inherit` spécifie le modèle à étendre.
   - Un nouveau champ `parent_id` est ajouté au modèle `res.company`, permettant à chaque entreprise d'avoir
     une société mère.
   - Cette approche permet d'étendre la fonctionnalité des modèles standard d'Odoo sans modifier le code source original.

4. Champs Relationnels (`Many2one`, `One2many`, `Many2many`):
   -----------------------------------------------------------
   Odoo prend en charge divers types de champs relationnels comme `Many2one`, `One2many` et `Many2many` pour établir
   des relations entre différents modèles.

   Exemple dans `bilan.py`:
   region_id = fields.Many2one('res.company', string="المديرية الجهوية")
   branch_id = fields.Many2one('res.branch', string="المديرية الإقليمية ")
   area_id = fields.Many2one('area', string="دائرة تنمية المجال الغابوي")
   forest_area_id = fields.Many2one('forest.area', string=" الوحدة و المركز الغابويين")

   Explication:
   - `Many2one`: Ce type de champ crée une relation plusieurs-à-un, ce qui signifie que plusieurs enregistrements
     de ce modèle peuvent référencer un seul enregistrement d'un autre modèle.
   - Dans cet exemple, `region_id`, `branch_id`, `area_id` et `forest_area_id` sont des champs `Many2one` référant
     leurs modèles respectifs. Cela crée une structure hiérarchique, où chaque enregistrement de `bilan` peut être
     associé à une région, une branche, une zone et une zone forestière spécifiques.

5. Domaines et Contextes:
   -----------------------
   Les domaines dans Odoo sont utilisés pour filtrer les enregistrements en fonction de certains critères,
   tandis que les contextes fournissent des informations supplémentaires qui peuvent influencer le comportement
   des champs et des méthodes.

   Exemple dans `bilan.py`:
   @api.onchange('branch')
   def _onchange_branch(self):
       if self.branch:
           return {'domain': {'forest_area': [('branch_id', '=', self.branch.id)],
                              'area': [('branch_id', '=', self.branch.id)]}}
       else:
           return {'domain': {'forest_area': [], 'area': []}}

   Explication:
   - La méthode `_onchange_branch` définit le domaine pour les champs `forest_area` et `area` en fonction de la branche sélectionnée.
   - Si une branche est sélectionnée, elle filtre `forest_area` et `area` pour ne montrer que les enregistrements liés à la branche sélectionnée.
   - Si aucune branche n'est sélectionnée, elle définit un domaine vide, rendant aucun enregistrement sélectionnable.

6. Sécurité et Contrôle d'Accès:
   ------------------------------
   Odoo utilise des mécanismes de sécurité et de contrôle d'accès pour gérer les permissions pour différents groupes d'utilisateurs.
   Cela inclut la définition de listes de contrôle d'accès (ACL) et des règles d'enregistrement.

   Exemple dans `bilan.py` (référencé dans le manifeste du module):
   'data': [
       'security/ir.model.access.csv',
       'security/security.xml',
   ]

   Explication:
   - Le fichier `ir.model.access.csv` définit les permissions pour chaque modèle, spécifiant quels groupes peuvent lire, écrire, créer et supprimer des enregistrements.
   - Le fichier `security.xml` peut définir des règles de sécurité et des restrictions plus complexes basées sur des conditions spécifiques.
   - Ces fichiers de sécurité garantissent que seuls les utilisateurs autorisés peuvent accéder et modifier les données selon leurs rôles.

7. Modèles de Rapport (QWeb):
   ---------------------------
   Odoo permet de créer des modèles de rapport personnalisés en utilisant QWeb, un moteur de template basé sur XML.

   Exemple dans le manifeste du module:
   'data': [
       'report/report_bilan_template.xml',
   ]

   Explication:
   - Le fichier `report_bilan_template.xml` définit la structure et la mise en page du rapport.
   - Les templates QWeb utilisent une syntaxe XML pour définir comment les données doivent être affichées dans le rapport.
   - Ces templates peuvent inclure du contenu statique, des champs dynamiques et des boucles pour générer des rapports détaillés et personnalisés.

En comprenant et en utilisant ces concepts et techniques avancés, vous pouvez construire des modules Odoo puissants et flexibles qui répondent à des exigences métier complexes.




# Explications des Concepts et Techniques Avancés dans le Fichier 'security.xml'

1. Règles d'Accès au Modèle (`ir.model.access`):
   ---------------------------------------------
   Odoo utilise des enregistrements `ir.model.access` pour définir les permissions de base pour chaque modèle.
   Ces enregistrements spécifient les groupes d'utilisateurs qui peuvent lire, écrire, créer et supprimer des enregistrements.

   Exemple:
   <record id="access_bilan_user" model="ir.model.access">
       <field name="name">bilan user access</field>
       <field name="model_id" ref="model_bilan"/>
       <field name="group_id" ref="base.group_user"/>
       <field name="perm_read" eval="1"/>
       <field name="perm_write" eval="1"/>
       <field name="perm_create" eval="1"/>
       <field name="perm_unlink" eval="1"/>
   </record>

   Explication:
   - `model_id` réfère au modèle auquel les règles s'appliquent.
   - `group_id` spécifie le groupe d'utilisateurs auquel les permissions sont accordées.
   - `perm_read`, `perm_write`, `perm_create`, `perm_unlink` définissent les permissions de lecture, écriture, création et suppression.

2. Règles Basées sur le Domaine (`ir.rule`):
   -----------------------------------------
   Les règles basées sur le domaine permettent de restreindre l'accès aux enregistrements en fonction de conditions spécifiques.
   Ces règles utilisent l'attribut `domain_force` pour appliquer des filtres sur les enregistrements accessibles par les utilisateurs.

   Exemple:
   <record id="rule_bilan_user" model="ir.rule">
       <field name="name">Bilan user rule</field>
       <field name="model_id" ref="model_bilan"/>
       <field name="groups" eval="[(4, ref('base.group_user'))]"/>
       <field name="domain_force">['|', ('regione', 'in', user.company_ids.ids), ('branch', 'in', user.branch_ids.ids)]</field>
   </record>

   Explication:
   - `model_id` réfère au modèle auquel la règle s'applique.
   - `groups` spécifie les groupes d'utilisateurs auxquels la règle s'applique.
   - `domain_force` définit les conditions de filtrage des enregistrements accessibles.
   - Dans cet exemple, la règle permet aux utilisateurs d'accéder aux enregistrements de `bilan` associés à leurs régions (`regione`) ou à leurs branches (`branch`).

3. Utilisation de la Gestion Multi-Branches:
   ------------------------------------------
   Le module utilise la gestion multi-branches pour contrôler l'accès aux enregistrements en fonction des régions et des provinces attribuées aux utilisateurs.
   Cela permet de restreindre l'accès aux données sensibles et d'assurer que les utilisateurs ne peuvent voir que les informations pertinentes pour leurs régions ou branches.

   Exemple dans `domain_force`:
   - `('regione', 'in', user.company_ids.ids)`: Restriction d'accès basée sur les régions auxquelles l'utilisateur a accès.
   - `('branch', 'in', user.branch_ids.ids)`: Restriction d'accès basée sur les branches auxquelles l'utilisateur a accès.

   Explication:
   - `user.company_ids.ids` et `user.branch_ids.ids` sont des listes d'IDs des régions et branches respectivement associées à l'utilisateur.
   - En utilisant ces listes dans `domain_force`, Odoo restreint l'accès aux enregistrements en fonction des régions et branches de l'utilisateur.
"""



