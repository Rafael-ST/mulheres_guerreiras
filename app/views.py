from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import formats, timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from sso.exceptions import CanNotRefreshToken
from sso.decorators import check_auth_sso
from sso.views import get_cadastro, redirect_to_login
from weasyprint import HTML, CSS

from app.constants import TIPO_NENHUM, TIPO_INV
from app.forms import InitialForm, ProponenteForm, PropostaForm, InvestimentoForm, ContratoForm,InscricoesForm#, EntregaChipForm
from app.models import Proposta, BeneficiadoAnterior, Proponente, Configs, Atividade, Investimento, EntregaChip, \
    AgendamentoChip, Capacitacoes, Inscricao, Contrato
from app.utils import export_pdf
from utils.helper import set_readonly_fields_sumetido, set_readonly_fields_sogiag
import tempfile


@csrf_exempt
@check_auth_sso
def index(request, token_parsed):
    projeto = None
    if request.method == "POST":
        pass
        nome_projeto = request.POST.get('nome_projeto')
        prop = Proponente()
        perfil = get_cadastro(request)
        if perfil and 'sucesso' in perfil and perfil['sucesso'] == 'true':
            prop.set_fields_by_perfil(perfil)
            if prop.sexo in []: #['M']:
                messages.error(request, 'Para enviar uma proposta é necessário ser do sexo Feminino!')
            elif prop.get_idade() < 18:
                messages.error(request, 'Para enviar uma proposta é necessário ter no mínimo 18 anos!')
            else:
                prop.save()
                proposta = Proposta()
                proposta.nome_empreendimento = nome_projeto
                proposta.proponente = prop
                proposta.save()
                # send_email_in_thread(projeto.socia_gestora.email, SUBJECT_EMAIL_CADASTRO,
                #                      MESSAGE_EMAIL_CADASTRO.format(projeto.nome_empreendimento))
        else:
            messages.error(request, 'Não foi possível obter seus dados, tente novamente! {}'.format(perfil))
        return redirect('/')
    else:
        try:
            proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
            return render(request, "app/index.html", {'projeto': proposta})
        except Proposta.DoesNotExist:
            form = None
            try:
                beneficiario_anterior = BeneficiadoAnterior.objects.get(cpf=token_parsed['preferred_username'])
                if beneficiario_anterior:
                    messages.error(request,
                                   '{} você não poderá enviar uma proposta pois já foi contemplado anteriormente '
                                   'no projeto {}.'.format(beneficiario_anterior.nome, beneficiario_anterior.projeto))
            except BeneficiadoAnterior.DoesNotExist:
                form = InitialForm()
    return render(request, "app/index.html", {'form': form, 'projeto': projeto, 'username': token_parsed['name'],
                                              'cpf': token_parsed['preferred_username']})


@csrf_exempt
@check_auth_sso
def cadastro_proponente(request, token_parsed):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    proponente = proposta.proponente
    form = None
    if request.method == "POST":
        if not Configs.get_flag('cadastroprojeto'):
            messages.error(request, "Alteração não realizada em {} ! As inscrições já foram encerradas, "
                                    "não é possível alterar.".format(proponente.nome))
            return redirect('/')
        else:
            if proponente.submissao:
                messages.error(request, "Alteração não realizada em {} ! Este projeto já foi submetido, "
                                        "não é possível alterar.".format(proponente.nome))
                return redirect('/')
            else:
                form = ProponenteForm(request.POST, request.FILES, instance=proponente)
                if form.is_valid():
                    p = form.save(commit=False)
                    p.save()
                    step = request.POST.get('step', '0')
                    if 'nextstep' in request.POST and int(step) < 9:
                        return redirect('/cadastro-proponente/?step={}'.format(int(step) + 1))
                    elif 'previousstep' in request.POST and int(step) > 0:
                        return redirect('/cadastro-proponente/?step={}'.format(int(step) - 1))
                    else:
                        messages.info(request, "Proponente {} atualizado com sucesso!".format(p.nome))
                        return redirect('/')
    else:
        if proposta:
            form = ProponenteForm(instance=proponente)
            set_readonly_fields_sogiag(form)
            if proponente.submissao:
                set_readonly_fields_sumetido(form)
    return render(request, "app/cadastro_proponente.html", {'form': form})


@csrf_exempt
@check_auth_sso
def cadastro_proposta(request, token_parsed):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    if request.method == "POST":
        if not Configs.get_flag('cadastroprojeto'):
            messages.error(request, "Alteração não realizada em projeto {}! As inscrições já foram encerradas"
                                    ", não é possível alterar.".format(proposta.nome_empreendimento))
            return redirect('/')
        else:
            if proposta.submissao:
                messages.error(request, "Alteração não realizada em projeto {}! Este projeto já foi "
                                        "submetido, não é possível alterar.".format(proposta.nome_empreendimento))
                return redirect('/')
            else:
                form_proposta = PropostaForm(request.POST, instance=proposta, is_post=True)
                if form_proposta.is_valid():
                    print('Projeto válido')
                    proposta = form_proposta.save(commit=False)
                    proposta.save()
                    step = request.POST.get('step', '0')
                    if 'nextstep' in request.POST and int(step) < 9:
                        return redirect('/cadastro-proposta/?step={}'.format(int(step) + 1))
                    elif 'previousstep' in request.POST and int(step) > 0:
                        return redirect('/cadastro-proposta/?step={}'.format(int(step) - 1))
                    elif 'submitinvestimento' in request.POST:
                        return redirect('/cadastro-investimento/?step_back={}'.format(3))
                    else:
                        messages.info(request, "Proposta {} atualizado com sucesso!".format(proposta.nome_empreendimento))
                        return redirect('/')
    else:
        context = {}
        form_proposta = PropostaForm(instance=proposta)
        if proposta.submissao:
            set_readonly_fields_sumetido(form_proposta)
        objects, groups, total_geral = get_ext_groups(proposta, Investimento, TIPO_INV)
        context.update({'form': form_proposta, 'objects': objects, 'groups_inv': groups, 'total_geral_inv': total_geral})

    return render(request, "app/cadastro_projeto.html", context)


@csrf_exempt
def load_atividades(request):
    setor_id = request.GET.get('setor')
    try:
        atividades = Atividade.objects.filter(setor_id=setor_id).order_by('descricao')
    except:
        atividades = Atividade.objects.none()
    return render(request, 'app/atividades_dropdown_list_options.html', {'atividades': atividades})


@csrf_exempt
@check_auth_sso
def cadastro_investimento(request, token_parsed):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    if request.method == "POST":
        if proposta.submissao:
            messages.error(request, "Atualização não realizada. Plano de negócio já foi enviado anteriormente!")
            return redirect('/')

        form = InvestimentoForm(request.POST, request.FILES)
        if form.is_valid():
            obj_new = form.save(commit=False)
            obj_new.proposta = proposta
            is_valid, message = obj_new.validade_new()
            if is_valid:
                obj_new.save()
                messages.info(request, 'Item inserido com sucesso! '+message)
            else:
                messages.error(request, 'Item não inserido! '+message)
            form = InvestimentoForm()
    else:
        form = InvestimentoForm()

    if proposta.submissao:
        set_readonly_fields_sumetido(form)
    context = {'form': form, 'nome': Investimento._meta.verbose_name.title(), 'label': 'Investimentos', 'delete_url': 'delete url',
               'with_group': True, 'id_comp_plano': Investimento.__name__}

    objects, groups, total_geral = get_ext_groups(proposta, Investimento, TIPO_INV)
    context.update({'objects': objects, 'groups': groups, 'total_geral': total_geral})

    return render(request, "app/extensionsform.html", context)


def get_ext_groups(proposta, objClass, types):
    # todo: rever esse código -> if not type: TIPO_NENHUM
    if not type: TIPO_NENHUM
    # todo: rever o if abaixo
    if 'quantidade' in [f.name for f in objClass._meta.get_fields()]:
        exts = objClass.objects.filter(proposta=proposta).extra(select={'valor_total': 'valor * quantidade'})
    elif 'valor' in [f.name for f in objClass._meta.get_fields()]:
        exts = objClass.objects.filter(proposta=proposta).extra(select={'valor_total': 'valor * 1'})
    else:
        exts = objClass.objects.filter(proposta=proposta)

    total_geral = 0
    for i in exts: total_geral += i.valor_total

    groups = []
    for key, value in dict(types).items():
        if key != '0':
            _exts = exts.filter(tipo=key)
        else:
            _exts = exts
        if _exts:
            total = 0
            for i in _exts: total += i.valor_total
            total = total
            try:
                perc = round(((total * 100) / total_geral), 2)
            except Exception as e:
                perc = 0
            groups.append({'exts': _exts, 'label': value,
                           'total': formats.localize(total, use_l10n=True),
                           'perc': perc})
    return exts, groups, formats.localize(total_geral, use_l10n=True)


@csrf_exempt
@check_auth_sso
def delete_investimento(request, token_parsed, pk):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    if proposta.submissao:
        messages.error(request, "Atualização não realizada. Proposta já foi enviado anteriormente!")
        return redirect('/cadastro-proposta/')
    try:
        obj = Investimento.objects.get(pk=pk, proposta=proposta)
        obj.delete()
        messages.info(request, "Item excluído com sucesso!")
    except Investimento.DoesNotExist:
        messages.info(request, "Item não encontrado!")
    return redirect('/cadastro-investimento/')


@csrf_exempt
@check_auth_sso
def export_proposta_pdf(request, token_parsed):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    objects, groups, total_geral = get_ext_groups(proposta, Investimento, TIPO_INV)
    form = PropostaForm(request.POST, request.FILES, instance=proposta)
    return export_pdf({'form': form, 'projeto': proposta, 'groups_inv': groups, 'total_geral_inv': total_geral},
                      token_parsed['name'], 'app/pdf.html', request.build_absolute_uri())


@csrf_exempt
@check_auth_sso
def export_proposta_pdf_prop(request, token_parsed):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    proponente = proposta.proponente
    form = ProponenteForm(request.POST, request.FILES, instance=proponente)

    return export_pdf({'form': form, 'projeto': proposta},
                      token_parsed['name'], 'app/pdfProp.html', request.build_absolute_uri())


@csrf_exempt
@check_auth_sso
def entrega_chip(request, token_parsed):
    if not Configs.get_flag('entregachip'):
        messages.error(request, "Alteração não realizada! Agendamento de entrega de Chip inativo.")
        return redirect('/')

    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    try:
        if proposta.ultima_avaliacao.resultado == '1':
            try:
                agendamento = AgendamentoChip.objects.get(proposta=proposta)
            except AgendamentoChip.DoesNotExist:
                agendamento = None

            try:
                entrega = EntregaChip.objects.get(proposta=proposta)
            except EntregaChip.DoesNotExist:
                entrega = None

            return render(request, "app/entrega_chip.html",
                          {'agendamento': agendamento, 'entrega': entrega})
    except Exception:
        messages.error(request, "Não é possível realizar esta operação!")
        return redirect('/')


@csrf_exempt
@check_auth_sso
def submeter_proposta(request, token_parsed):

    if not Configs.get_flag('cadastroprojeto'):
        return redirect('/')

    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])

    try:
        is_valid = True
        msg = 'O(s) campo(s) obrigatório(s) ({}) para o {} deve(m) ser preenchido(s).'
        fields = proposta.get_required_fields_none()
        if fields:
            messages.error(request, msg.format(', '.join(fields), 'proposta ' + proposta.nome_empreendimento))
            is_valid = False

        if is_valid:
            if proposta.submeter():
                messages.info(request, 'Proposta enviada com sucesso!')
                # todo Enviar Email
                # send_email_in_thread(projeto.socia_gestora.email, SUBJECT_EMAIL_SUBMETIDO,
                #                      MESSAGE_EMAIL_SUBMETIDO.format(projeto.nome_empreendimento))
            else:
                messages.warning(request, 'Operação não realizada, pois a proposta já estava submetida!')
        else:
            messages.error(request, 'Proposta não enviada! Favor preencha os campos acima e envie novamente.')
        return redirect('/')
    except Proposta.DoesNotExist:
        messages.error(request, 'Proposta não encontrada!')
    except Exception as e:
        messages.error(request, 'Erro ao enviar proposta! {}'.format(e))
    return redirect('/')


@csrf_exempt
@check_auth_sso
def submeter_proponente(request, token_parsed):

    if not Configs.get_flag('cadastroproponente'):
        return redirect('/')

    proponente = Proponente.objects.get(cpf=token_parsed['preferred_username'])

    try:
        is_valid = True
        msg = 'O(s) campo(s) obrigatório(s) ({}) para o {} deve(m) ser preenchido(s).'
        fields = proponente.get_required_fields_none()
        if fields:
            messages.error(request, msg.format(', '.join(fields), 'proponente ' + proponente.nome))
            is_valid = False

        if is_valid:
            if proponente.submeter():
                messages.info(request, 'Dados do proponente enviados com sucesso!')
                #todo Enviar Email
                # send_email_in_thread(projeto.socia_gestora.email, SUBJECT_EMAIL_SUBMETIDO,
                #                      MESSAGE_EMAIL_SUBMETIDO.format(projeto.nome_empreendimento))
            else:
                messages.warning(request, 'Operação não realizada, pois a proposta já estava submetido!')
        else:
            messages.error(request, 'Proposta não enviado! Favor preencha os campos acima e envie novamente.')
        return redirect('/')
    except Proponente.DoesNotExist:
        messages.error(request, 'Proposta não encontrado')
    except Exception as e:
        messages.error(request, 'Erro ao enviar projeto! {}'.format(e))
    return redirect('/')


@csrf_exempt
@check_auth_sso
def cadastro_contrato(request, token_parsed):
    proponente = Proponente.objects.get(cpf=token_parsed['preferred_username'])
    proponente = "a"
    if request.method == "POST":
        imprimir = ""
        form = ContratoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ContratoForm(initial={'cpf': token_parsed['preferred_username']})
        form.fields['cpf'].widget.attrs['readonly'] = True
        try:
            contrato = Contrato.objects.get(cpf=token_parsed['preferred_username'])
            imprimir = True
        except Contrato.DoesNotExist:
            imprimir = False

    return render(request, "app/cadastro-contrato.html", {'form': form, 'imprimir': imprimir})


@csrf_exempt
@check_auth_sso
def inscricao(request, token_parsed):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    proponente = proposta.proponente.cpf
    capacitacoes = Capacitacoes.objects.all().order_by('titulo')
    if request.method == "POST":
            if not Configs.get_flag('inscricaocapacitacao'):
                messages.error(request, "As inscrições já foram encerradas, não é possível alterar.")
                return redirect('/')
            else:
                capacitacao = request.POST['capacitacao']
                proponente = get_object_or_404(Proponente, cpf=proponente)
                capacitacao = get_object_or_404(Capacitacoes, titulo=capacitacao)
                inscricao = Inscricao.objects.create(proponente=proponente, capacitacao=capacitacao)
                inscricao.save()
                vagas = capacitacao.vagas
                Capacitacoes.objects.filter(titulo=capacitacao).update(vagas=vagas - 1)
                return redirect('/')

                form = InscricoesForm(request.POST)
                if form.is_valid():
                    a = form.save(commit=False)
                    a.save()
                    return redirect('/')
    else:
        form = InscricoesForm()
        insc = ""
        try:
            insc = Inscricao.objects.get(proponente=proposta.proponente)
            ins = True
        except Inscricao.DoesNotExist:
            ins = False
    return render(request, 'app/inscricao.html', {'form': form, 'proponente': proponente, 'capacitacoes': capacitacoes,
                                                  'ins': ins, 'insc': insc})

@csrf_exempt
@check_auth_sso
def cancelar_inscricao(request, token_parsed):
    proposta = Proposta.objects.get(proponente__cpf=token_parsed['preferred_username'])
    proponente = proposta.proponente
    insc = Inscricao.objects.get(proponente=proponente)
    cap = insc.capacitacao
    capacitacao = get_object_or_404(Capacitacoes, titulo=cap)
    vagas = capacitacao.vagas
    Capacitacoes.objects.filter(titulo=capacitacao).update(vagas=vagas + 1)
    insc.delete()
    return redirect('/')

