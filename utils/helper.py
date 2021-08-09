import json


def set_readonly_fields_sogiag(instanceForm):
    instanceForm.fields['cpf'].widget.attrs['readonly'] = True
    instanceForm.fields['nome'].widget.attrs['readonly'] = True


def set_readonly_fields_sumetido(instanceForm):
    for field in instanceForm.fields:
        instanceForm.fields[field].widget.attrs['readonly'] = True
        instanceForm.fields[field].widget.attrs['disabled'] = 'disabled'


