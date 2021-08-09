from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.validators import FileExtensionValidator
from django_select2 import forms as s2forms

from app.constants import DEFICIENCIA, IDADE_CLIENTES, ESTIMULO_COMPRA
from app.models import Proponente, Proposta, Atividade, Investimento, Contrato, Inscricao, Capacitacoes

file_types = ['pdf', 'png', 'jpeg', 'jpg']


class DateInput(forms.DateInput):

    input_type = 'date'
    input_format = '%d/%m/%Y'


class InitialForm(forms.Form):
    nome_projeto = forms.CharField(label='Nome do Empreendimento', widget=forms.TextInput())

    class Meta:
        labels = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for index in self.fields:
            self.fields[index].widget.attrs['style'] = 'font-size: large'


class ProponenteForm(forms.ModelForm):

    cpf = forms.CharField(label='CPF', widget=forms.TextInput(attrs={'class':'cpf'}))
    #data_nascimento = forms.DateField(widget=DateInput, required=False)
    email = forms.CharField(label='E-mail*', widget=forms.TextInput(attrs={'type': 'email'}), required=False)
    # telefone_2 = forms.CharField(label='Telefone2*', widget=forms.TextInput(attrs={'class':'telefone'}), required=False)

    file_rg_frente = forms.FileField(validators=[FileExtensionValidator(file_types)], label="RG Frente*", required=False)
    file_rg_verso = forms.FileField(validators=[FileExtensionValidator(file_types)], label="RG Verso*", required=False)
    file_cpf = forms.FileField(validators=[FileExtensionValidator(file_types)], label="CPF digitalizado*", required=False)
    file_comp_endereco = forms.FileField(validators=[FileExtensionValidator(file_types)],label="Comp. de endereço*", required=False)
    file_dec_endereco = forms.FileField(validators=[FileExtensionValidator(file_types)],label="Declaração de endereço", required=False)
    file_livre = forms.FileField(validators=[FileExtensionValidator(file_types)],label="Outro", required=False)

    deficiencia = forms.MultipleChoiceField(label='Possui algum tipo de deficiência?*', choices=DEFICIENCIA,
                                            widget=s2forms.Select2MultipleWidget(), required=False)

    class Meta:
        model = Proponente
        exclude = ('created_at', 'updated_at')

        widgets = {
            'bairro': s2forms.Select2Widget(),
            'situacao_conjugal': s2forms.Select2Widget(),
            'escolaridade': s2forms.Select2Widget(),
            'deficiencia': s2forms.Select2MultipleWidget(),
            'tipo_logradouro': s2forms.Select2Widget(),
            'trabalha_atualmente': s2forms.Select2Widget(),
            'renda': s2forms.Select2Widget(),
            'recebe_beneficio': s2forms.Select2Widget(),
            'residentes': s2forms.Select2Widget(),
            'experiencia': s2forms.Select2Widget(),
            'participou_curso_gerencial': s2forms.Select2Widget(),
            'participou_curso_tecnico': s2forms.Select2Widget(),
            'necessita_curso_tecnico': s2forms.Select2Widget(),
        }

        labels = {
            'data_nascimento': 'Data de nascimento*',
            'file_rg_frente': 'RG Frente*',
            'file_rg_vers': 'RG Verso*',
            'rg': 'RG*',
            'sexo': 'Sexo*',
            'nome_pai': 'Nome do Pai*',
            'nome_mae': 'Nome da Mãe*',
            'situacao_conjugal': 'Situação conjugal*',
            'qtde_filhos': 'Quantidade de filhos*',
            'telefone': 'Tel. Fixo',
            'logradouro': 'Logradouro*',
            'numero': 'Número*',
            'bairro': 'Bairro*',
            'cep': 'CEP*',
            'escolaridade': 'Escolaridade*',
            'deficiencia': 'Possui algum tipo de deficiência?*',
            'recebe_beneficio': 'Você recebe algum benefício social do Governo? ',
            'residentes': 'Quantas pessoas residem (moram) com você? ',
            'file_comp_endereco': 'Comprovante de endereço'
        }

    def clean_cep(self):
        data = self.cleaned_data['cep']
        if data:
            data = data.replace(".", "")
            data = data.replace("-", "")
        return data

    def clean_cpf(self):
        data = self.cleaned_data['cpf']
        if data:
            data = data.replace(".", "")
            data = data.replace("-", "")
        return data


class PropostaForm(forms.ModelForm):

    idade_cliente = forms.MultipleChoiceField(choices=IDADE_CLIENTES, widget=s2forms.Select2MultipleWidget(),
                                              required=False)
    estimulo_compra = forms.MultipleChoiceField(choices=ESTIMULO_COMPRA, widget=s2forms.Select2MultipleWidget(),
                                              required=False)

    class Meta:
        model = Proposta
        exclude = ('proponente', 'submissao', 'ult_avaliacao_ok', 'created_at', 'updated_at')

        widgets = {
            'bairro': s2forms.Select2Widget(),
            'setor': s2forms.Select2Widget(),
            'atividade': s2forms.Select2Widget(),
            'finalidade': s2forms.Select2Widget(),
            'outra_renda': s2forms.Select2Widget(),
            'estudo_setor': s2forms.Select2Widget(),
            'idade_cliente': s2forms.Select2MultipleWidget(),
            'frequencia': s2forms.Select2Widget(),
            'localizacao': s2forms.Select2Widget(),
            'tamanho_mercado': s2forms.Select2Widget(),
            'estimulo_compra': s2forms.Select2MultipleWidget(),
            'motivo_localizacao': s2forms.Select2Widget(),
            'concorrente_atendimento': s2forms.Select2Widget(),
            'concorrente_qualidade': s2forms.Select2Widget(),
            'concorrente_localizacao': s2forms.Select2Widget(),
            'concorrente_preco': s2forms.Select2Widget(),
            'concorrente_forma_pagamento': s2forms.Select2Widget(),
            'concorrente_forma_propaganda': s2forms.Select2Widget(),
            'divulgacao': s2forms.Select2Widget(),
        }

        labels ={
            'idade': 'Qual a Idade dos seus clientes',
            'divulgacao': 'Qual vai ser o principal meio de divulgação do seu negócio?',
        }

    def __init__(self, *args, **kwargs):
        is_post = kwargs.pop('is_post', None)
        super().__init__(*args, **kwargs)
        atividade = kwargs['instance']
        if is_post:
            self.fields['atividade'].queryset = Atividade.objects.all()
        elif atividade.setor:
            self.fields['atividade'].queryset = Atividade.objects.filter(setor=atividade.setor)
        else:
            self.fields['atividade'].queryset = Atividade.objects.none()


class InvestimentoForm(forms.ModelForm):

    valor = forms.DecimalField(max_digits=10, decimal_places=2, localize=True,
                               widget=forms.TextInput(attrs={'class':'dinheiro'}),
                               label='Valor unitário')

    class Meta:
        model = Investimento
        exclude = ('proposta', )


class ContratoForm(forms.ModelForm):
    file_cartao_cnpj = forms.FileField(validators=[FileExtensionValidator(file_types)], label="Cartão CNPJ",
                                     required=True)

    class Meta:
        model = Contrato
        fields = ('file_cartao_cnpj', 'cpf', 'proponente')

    #def __init__(self, *args, **kwargs):
    #    is_post = kwargs.pop('is_post', None)
    #    super().__init__(*args, **kwargs)
    #    print(is_post)
    #    self.fields['proponente'].queryset = Proponente.objects.filter(cpf=is_post)

    def clean_cpf(self):
        data = self.cleaned_data['cpf']
        if data:
            data = data.replace(".", "")
            data = data.replace("-", "")
        return data



class InscricoesForm(forms.ModelForm):
    #capacitacao = forms.ChoiceField(choices=Capacitacoes.objects.all(), widget=forms.RadioSelect())
    #proponente = forms.CharField(label="nome")
    #capacitacao = forms.ModelChoiceField(queryset=Capacitacoes.objects.all())

    def __init__(self, proponente=None, proponente_value=None, *args, **kwargs):
        super(InscricoesForm, self).__init__(*args, **kwargs)
        self.fields['capacitacao'].queryset = Capacitacoes.objects.all()

    class Meta:
        model = Inscricao
        exclude = ('created_at', 'update_at', 'frequencia')
