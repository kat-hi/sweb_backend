from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import current_app as app, render_template


class AuthenticatedView(ModelView):
	def is_accessible(self):
		app.logger.info('CURRENT USER AUTH VIEW: ' + str(current_user))
		app.logger.info(f'is authenticated: {current_user.is_authenticated}')
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return render_template('401.html')


class pflanzlistetable(AuthenticatedView):
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = True


class obstsortentable(AuthenticatedView):
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = True


class imagetable(AuthenticatedView):
	column_display_pk = True
	can_create = False
	can_delete = False
	can_edit = True
	can_export = True
	can_set_page_size = True
