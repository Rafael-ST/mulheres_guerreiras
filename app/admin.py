import csv

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from app.constants import RESULTADOS_CORES, TIPO_INV
from app.models import EntregaChip, Proposta, AgendamentoChip, PropostaEntregaChipProxy, AvaliacaoProposta, \
    Investimento, AvaliacaoProponente, Proponente
from app.utils import export_pdf
from .models import Configs, Bairro, Atividade, Setor, LocalEntrega, Contrato, Capacitacoes, \
    Inscricao
from .views import get_ext_groups

from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage


class AgendamentoChipInline(admin.StackedInline):
    model = AgendamentoChip
    extra = 1


class EntregaChipInline(admin.StackedInline):
    model = EntregaChip
    extra = 1
    fields = ['termo_', 'data', 'termo', 'documento', 'foto', ]
    readonly_fields = ['termo_']

    def termo_(self, obj):
        link = reverse('admin:termo', args=[obj.proposta.id])
        return format_html('<a href="{}" target="_blank">{}</a>', link,
                           'Termo de Entrega e Responsabilidade do CHIP')


class AvaliacaoProponenteInline(admin.StackedInline):
    model = AvaliacaoProponente
    readonly_fields = ['avaliador', 'created_at']
    extra = 1


class ProponenteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'cpf', 'ult_avaliacao_ok', 'submissao', 'ultima_avaliacao_fmt']
    search_fields = ('nome', 'cpf', )
    inlines = [AvaliacaoProponenteInline, ]
    list_filter = ('bairro', 'ultima_avaliacao__resultado', 'ult_avaliacao_ok', )

    fieldsets = (
        (None, {
            # 'classes': ('collapse', 'open'),
            'fields': (
                       ('id', 'cpf', 'nome'),
            )
        }),
        ('Dados Pessoais', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                     ('rg', 'nome_pai', 'nome_mae', 'data_nascimento', 'sexo', 'ddd_1', 'telefone_1', 'ddd_2',
                      'telefone_2', 'email', 'situacao_conjugal', 'qtde_filhos', ),
            )
        }),
        ('Dados Residênciais', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                    ('tipo_logradouro', 'logradouro', 'numero', 'complemento', 'cep', 'bairro', 'municipio', 'uf', ),
            )
        }),
        ('Dados Sócio Econômicos', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                    ('escolaridade', 'deficiencia', 'deficiencia_outro', 'trabalha_atualmente', 'renda',
                     'recebe_beneficio', 'residentes', 'experiencia', 'participou_curso_gerencial',
                     'participou_curso_tecnico', 'necessita_curso_tecnico'),
            )
        }),
        ('Documentos', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                     ('file_rg_frente', 'file_rg_verso', 'file_cpf', 'file_comp_endereco', 'file_dec_endereco',
                      'file_livre'),
            )
        }),
        (None, {
            # 'classes': ('collapse', 'open'),
            'fields': (
                ('submissao', 'ult_avaliacao_ok',),
            )
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(submissao__isnull=False)

    def ultima_avaliacao_fmt(self, obj):
        return format_html(
        '<b style="color:{};">{}</b>',
        dict(RESULTADOS_CORES)[obj.ultima_avaliacao.resultado] if obj.ultima_avaliacao else 'gray',
        obj.ultima_avaliacao if obj.ultima_avaliacao else 'Não Avaliado',
        )
    ultima_avaliacao_fmt.allow_tags = True
    ultima_avaliacao_fmt.admin_order_field = 'ultima_avaliacao'
    ultima_avaliacao_fmt.short_description = 'Última Avaliação'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.__class__ == AvaliacaoProponente:
                instance.avaliador = request.user
                instance.save()
                if instance.resultado == '0':
                    instance.proponente.submissao = None
                instance.proponente.ult_avaliacao_ok = True
                instance.proponente.ultima_avaliacao = instance
                instance.proponente.save()
                #todo habilitar envio de emails
                # if instance.resultado == '1':
                #     send_email_in_thread(instance.projeto.socia_gestora.email, SUBJECT_EMAIL_APROVADO,
                #                          MESSAGE_EMAIL_APROVADO.format(instance.projeto.nome_empreendimento))
                # elif instance.resultado == '0':
                #     send_email_in_thread(instance.projeto.socia_gestora.email, SUBJECT_EMAIL_REPROVADO,
                #                          MESSAGE_EMAIL_REPROVADO.format(instance.projeto.nome_empreendimento, instance.motivo))
        formset.save_m2m()

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return ['id', 'proponente']
            else:
                return ['id', 'created_at', 'updated_at',
                        'cpf', 'nome', 'rg', 'nome_pai', 'nome_mae', 'data_nascimento', 'sexo', 'tipo_logradouro',
                        'logradouro', 'numero', 'complemento', 'cep', 'bairro', 'municipio', 'uf', 'ddd_1', 'ddd_2',
                        'telefone_1', 'telefone_2', 'email', 'situacao_conjugal', 'deficiencia_outro', 'qtde_filhos',
                        'escolaridade', 'deficiencia', 'trabalha_atualmente', 'renda', 'recebe_beneficio',
                        'residentes', 'experiencia', 'participou_curso_gerencial', 'participou_curso_tecnico',
                        'necessita_curso_tecnico', 'file_rg_frente', 'file_rg_verso', 'file_cpf', 'file_comp_endereco',
                        'file_dec_endereco', 'file_livre', 'submissao', 'ult_avaliacao_ok']


class AvaliacaoPropostaInline(admin.StackedInline):
    model = AvaliacaoProposta
    readonly_fields = ['avaliador', 'created_at']
    extra = 1


class PropostaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_empreendimento', 'ult_avaliacao_ok', 'submissao', 'ultima_avaliacao_fmt']
    search_fields = ('nome_empreendimento', )
    inlines = [AvaliacaoPropostaInline, ]
    list_filter = ('ultima_avaliacao__resultado', 'ult_avaliacao_ok', )

    fieldsets = (
        (None, {
            # 'classes': ('collapse', 'open'),
            'fields': (
                       ('id', 'nome_empreendimento', ),
            )
        }),
        ('Dados do Empreedimento', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                     ('bairro', 'finalidade', 'setor', 'atividade', 'outra_renda', ),
            )
        }),
        ('Informações de Mercado I', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                    ('estudo_setor', 'idade_cliente', 'frequencia', 'tamanho_mercado', 'localizacao',
                     'motivo_localizacao', 'divulgacao', 'divulgacao_outra', 'estimulo_compra',
                     ),
            )
        }),
        ('Análise de Mercado II', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                    ('concorrente_atendimento', 'concorrente_localizacao', 'concorrente_forma_pagamento',
                     'concorrente_forma_propaganda', 'concorrente_qualidade', 'concorrente_preco',
                     'concorrente_forma_pagamento_outra',
                     ),
            )
        }),
        ('Investimento', {
            # 'classes': ('collapse', 'open'),
            'fields': (
                     ('investimentos_', ),
            )
        }),
        (None, {
            # 'classes': ('collapse', 'open'),
            'fields': (
                ('submissao', 'ult_avaliacao_ok', ),
            )
        }),
    )

    def ultima_avaliacao_fmt(self, obj):
        return format_html(
        '<b style="color:{};">{}</b>',
        dict(RESULTADOS_CORES)[obj.ultima_avaliacao.resultado] if obj.ultima_avaliacao else 'gray',
        obj.ultima_avaliacao if obj.ultima_avaliacao else 'Não Avaliado',
        )
    ultima_avaliacao_fmt.allow_tags = True
    ultima_avaliacao_fmt.admin_order_field = 'ultima_avaliacao'
    ultima_avaliacao_fmt.short_description = 'Última Avaliação'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(submissao__isnull=False, proponente__ultima_avaliacao__resultado='1')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.__class__ == AvaliacaoProposta:
                instance.avaliador = request.user
                instance.save()
                if instance.resultado == '0':
                    instance.projeto.submissao = None
                instance.projeto.ult_avaliacao_ok = True
                instance.projeto.ultima_avaliacao = instance
                instance.projeto.save()
                #todo habilitar envio de emails
                # if instance.resultado == '1':
                #     send_email_in_thread(instance.projeto.socia_gestora.email, SUBJECT_EMAIL_APROVADO,
                #                          MESSAGE_EMAIL_APROVADO.format(instance.projeto.nome_empreendimento))
                # elif instance.resultado == '0':
                #     send_email_in_thread(instance.projeto.socia_gestora.email, SUBJECT_EMAIL_REPROVADO,
                #                          MESSAGE_EMAIL_REPROVADO.format(instance.projeto.nome_empreendimento, instance.motivo))
        formset.save_m2m()

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('adm-investimentos/<uuid:pk>/',
                 self.admin_site.admin_view(self.adm_investimentos),
                 name="adm_investimentos"),
        ]
        return my_urls + urls

    def investimentos_(self, obj):
        link = reverse('admin:adm_investimentos', args=[obj.id])
        return format_html('<a href="{}">{}</a>', link, Investimento._meta.verbose_name_plural.title())

    def adm_investimentos(self, request, pk):
        plano_negocio = Proposta.objects.get(id=pk)
        invs, groups, total_geral = get_ext_groups(plano_negocio, Investimento, TIPO_INV)
        return TemplateResponse(request, "app/extensionsadm.html", {'title':Investimento._meta.verbose_name_plural.title(),
                                                                    'groups': groups, 'total_geral': total_geral})

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return ['id', 'proponente', 'investimentos_']
            else:
                return ['id', 'created_at', 'updated_at',
                        'proponente', 'nome_empreendimento', 'bairro', 'finalidade', 'setor', 'atividade',
                        'outra_renda', 'estudo_setor', 'idade_cliente', 'frequencia', 'tamanho_mercado',
                        'localizacao', 'estimulo_compra', 'motivo_localizacao', 'concorrente_atendimento',
                        'concorrente_qualidade', 'concorrente_localizacao', 'concorrente_preco',
                        'concorrente_forma_pagamento', 'concorrente_forma_pagamento_outra',
                        'concorrente_forma_propaganda', 'divulgacao', 'divulgacao_outra', 'submissao',
                        'ult_avaliacao_ok', 'ultima_avaliacao', 'investimentos_']


class PropostaEntregaChipAdmin(admin.ModelAdmin):
    inlines = [AgendamentoChipInline, EntregaChipInline]
    fields = ['proponente', 'nome_empreendimento', 'todo_']
    # fields = ['proponente', 'nome_empreendimento', 'bairro', 'termo_']
    #
    # def termo_(self, obj):
    #     link = reverse('admin:termo', args=[obj.id])
    #     return format_html('<a href="{}" target="_blank">{}</a>', link,
    #                        'Termo de Entrega e Responsabilidade do CHIP')

    def todo_(self, obj):
        return 'Verificar se é necessário  trazer mais informações sobre projeto e proponente'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('termo/<pk>/',
                 self.admin_site.admin_view(self.termo),
                 name="termo"),
        ]
        return my_urls + urls

    def termo(self, request, pk):
        try:
            proposta = Proposta.objects.get(pk=pk)
            termo = Configs.get_valor('termoentregachip')
            termo = termo.replace('__NOME__', proposta.proponente.nome)
            termo = termo.replace('__CPF__', proposta.proponente.cpf)
            return export_pdf({'termo': format_html(termo)}, 'termo', 'app/termo_changelist.html',
                              request.build_absolute_uri())
        except Exception as e:
            return TemplateResponse(request, "app/termo_changelist.html",
                                    {'termo': 'Não foi possível gerar o termo de responsabilidade! '
                                              'Verifique se as configurações foram feitas. Erro:{}'.format(e)})

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(submissao__isnull=False, ultima_avaliacao__resultado='1')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return ['proponente', 'nome_empreendimento', 'bairro', 'todo_']
            else:
                return ['proponente', 'nome_empreendimento', 'bairro', 'todo_']


class ConfigsAdmin(admin.ModelAdmin):
    list_display = ['chave', 'valor', 'flag']
    search_fields = ('chave', )

    actions = ['to_enable', 'to_disable']

    def to_enable(self, request, queryset):
        for conf in queryset:
            conf.flag = True
            conf.save()
    to_enable.short_description = 'Ativar Funcionalidade'

    def to_disable(self, request, queryset):
        for conf in queryset:
            conf.flag = False
            conf.save()
    to_disable.short_description = 'Desativar Funcionalidade'


class CapacitacoesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_capacitacao',)
    search_fields = ('tipo_capacitacao', 'titulo')
    fields = ['titulo', 'data_aula', 'vagas', 'tipo_capacitacao', 'link']


class ToPdf:
    def html_to_pdf_view(self, request, queryset):
        nomes = []

        for obj in queryset:
            print(getattr(obj, "proponente"))
            nomes.append(getattr(obj, "proponente"))

        html_string = render_to_string('app/pdf_template.html', {'nomes': nomes})

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response

    html_to_pdf_view.short_description = "Criar pdf de alunos selecionados"


class InscricaoAdmin(admin.ModelAdmin, ToPdf):
    list_display = ['id', 'proponente', 'capacitacao', 'frequencia']
    list_editable = ('frequencia',)
    search_fields = ('capacitacao__titulo',)
    actions = ['html_to_pdf_view']
    list_filter = ('capacitacao',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return ['id']
            else:
                return ['id', 'proponente', 'capacitacao']

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    #def save_formset(self, request, form, formset, change):
    #    instances = formset.save(commit=False)
    #    for obj in formset.deleted_objects:
    #        obj.delete()
    #    for instance in instances:
    #        instance.user = request.user
    #        instance.save()
    #    formset.save_m2m()


admin.site.register(Configs, ConfigsAdmin)
admin.site.register(Bairro)
admin.site.register(Atividade)
admin.site.register(Setor)
admin.site.register(LocalEntrega)
admin.site.register(Proposta, PropostaAdmin)
admin.site.register(Proponente, ProponenteAdmin)
admin.site.register(PropostaEntregaChipProxy, PropostaEntregaChipAdmin)
admin.site.register(Contrato)
admin.site.register(Capacitacoes, CapacitacoesAdmin)
admin.site.register(Inscricao, InscricaoAdmin)
# admin.site.register(EntregaChip, EntregaChipAdmin)
