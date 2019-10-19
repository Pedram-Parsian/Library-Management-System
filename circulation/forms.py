from bootstrap_modal_forms.forms import BSModalForm

from . import models


class ReserveForm(BSModalForm):
    class Meta:
        model = models.Reserve
        fields = ['document', 'description']
