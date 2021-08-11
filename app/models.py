from datetime import datetime, date
from time import time

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
import uuid

from django.db.models import PROTECT

from app.constants import S_CONJ, ESCOLARIDADE, TRABALHA_ATUAL, TIPO_LOGRAOURO, RENDA_INDIVIDUAL, SIM_NAO, RESIDENTES, \
    AVALIACAO, FORMA_DE_PAGAMENTO, OBJETIVO, RAMO_ATIVIDADE, RAMO, IDADE_CLIENTES, FREQUENCIA, TAMANHO_MERCADO, \
    LOCALIZACAO, ESTIMULO_COMPRA, PRECO, PROPAGANDA, DIVULGACAO, TIPO_INV, VALOR_TOTAL_INVS, RESULTADOS, TIPO_CAPACITACAO, MOTIVO_LOCALIZACAO, STATUS
from app.utils import try_or
from app.validators import validate_CPF
from utils.utils import resizeImage


def upload_path_handler(instance, filename):
    cpf = instance.proposta.proponente.cpf if instance.__class__ == EntregaChip else instance.cpf
    return "docs/{cpf}/{file}".format(cpf=cpf, file=filename)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class Proponente(BaseModel):

    cpf = models.CharField(unique=True, max_length=11, validators=[validate_CPF], verbose_name='CPF')
    nome = models.CharField(max_length=100, null=True, verbose_name='Nome completo')
    rg = models.CharField(max_length=100, blank=True, null=True, verbose_name='RG')
    nome_pai = models.CharField(max_length=100, blank=True, null=True, verbose_name='Filiação 1')
    nome_mae = models.CharField(max_length=100, blank=True, null=True, verbose_name='Filiação 2')
    data_nascimento = models.DateField(blank=True, null=True, verbose_name='Data de nascimento')
    sexo = models.CharField(max_length=20, default='FEMININO', blank=True, null=True, verbose_name='Sexo')

    tipo_logradouro = models.CharField(max_length=150, choices=TIPO_LOGRAOURO, blank=True, null=True,
                                       verbose_name='Tipo Logradouro')
    logradouro = models.CharField(max_length=150, blank=True, null=True, verbose_name='Logradouro')
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=150, null=True, blank=True, verbose_name='Complemento')
    cep = models.CharField(max_length=10, blank=True, null=True, verbose_name='CEP')
    bairro = models.ForeignKey('Bairro', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Bairro')
    municipio = models.CharField(max_length=150, default='FORTALEZA', null=True, blank=True, verbose_name='Município')
    uf = models.CharField(max_length=150, null=True, default='CE',  blank=True, verbose_name='UF')

    ddd_1 = models.CharField(max_length=3, blank=True, null=True, verbose_name='DDD 1')
    telefone_1 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone 1')
    ddd_2 = models.CharField(max_length=3, blank=True, null=True, verbose_name='DDD 2')
    telefone_2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone 2')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='Email')

    situacao_conjugal = models.CharField(max_length=50, choices=S_CONJ, blank=True, null=True,
                                         verbose_name='Situação conjugal')
    qtde_filhos = models.IntegerField(blank=True, null=True, verbose_name='Qtde filhos')
    escolaridade = models.CharField(max_length=50, choices=ESCOLARIDADE, blank=True, null=True,
                                    verbose_name='Escolaridade')

    deficiencia = models.CharField(max_length=50, verbose_name='Deficiência', blank=True, null=True)
    deficiencia_outro = models.CharField(max_length=150, blank=True, null=True, verbose_name='Outra Deficiência')
    trabalha_atualmente = models.CharField(max_length=50, choices=TRABALHA_ATUAL, blank=True, null=True,
                                           verbose_name='Trabalha atualmente',)
    renda = models.CharField(max_length=50, choices=RENDA_INDIVIDUAL, blank=True, null=True,
                             verbose_name='Renda individual')
    recebe_beneficio = models.CharField(max_length=5, choices=SIM_NAO, blank=True, null=True,
                                               verbose_name='Trabalha atualmente')
    residentes = models.CharField(max_length=5, choices=RESIDENTES, blank=True, null=True,
                                  verbose_name='Qtde residentes')

    experiencia = models.CharField(max_length=5, choices=SIM_NAO, blank=True, null=True,
                                   verbose_name='Experiência Profissional')
    participou_curso_gerencial = models.CharField(max_length=5, choices=SIM_NAO, blank=True, null=True,
                                                  verbose_name='Participou de curso gerencial')
    participou_curso_tecnico = models.CharField(max_length=5, choices=SIM_NAO, blank=True, null=True,
                                                verbose_name='Participou de curso técnico')
    necessita_curso_tecnico = models.CharField(max_length=5, choices=SIM_NAO, blank=True, null=True,
                                               verbose_name='Necessita de curso técnico')

    file_rg_frente = models.FileField(upload_to=upload_path_handler, blank=True, null=True, verbose_name='RG Frente')
    file_rg_verso = models.FileField(upload_to=upload_path_handler, blank=True, null=True, verbose_name='RG Verso')
    file_cpf = models.FileField(upload_to=upload_path_handler, blank=True, null=True, verbose_name='CPF')
    file_comp_endereco = models.FileField(upload_to=upload_path_handler, blank=True, null=True,
                                          verbose_name='Comprovante de endereço')
    file_dec_endereco = models.FileField(upload_to=upload_path_handler, blank=True, null=True,
                                         verbose_name='Declaração de endereço')
    file_livre = models.FileField(upload_to=upload_path_handler, blank=True, null=True, verbose_name='Campo livre')

    submissao = models.DateTimeField(blank=True, null=True, verbose_name='Última subimissão')
    ult_avaliacao_ok = models.BooleanField(default=False, verbose_name='Avaliado')
    ultima_avaliacao = models.ForeignKey('AvaliacaoProponente', related_name='b_avaliacao', blank=True, null=True,
                                         on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Proponente"
        verbose_name_plural = "Proponentes"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.deficiencia:
            self.deficiencia=eval(self.deficiencia)

    def __str__(self):
        return '{} - {}'.format(self.cpf, self.nome)

    def get_required_fields_none(self):
        requireds = ['cpf', 'nome', 'rg', 'nome_pai', 'nome_mae', 'data_nascimento', 'sexo', 'tipo_logradouro',
                     'logradouro', 'numero', 'cep', 'bairro', 'municipio', 'uf', 'ddd_1', 'ddd_2',
                     'telefone_1', 'telefone_2', 'email', 'situacao_conjugal', 'qtde_filhos', 'escolaridade',
                     'trabalha_atualmente', 'renda', 'recebe_beneficio', 'residentes', 'experiencia',
                     'participou_curso_gerencial', 'participou_curso_tecnico', 'necessita_curso_tecnico',
                     'file_rg_frente', 'file_rg_verso', 'file_cpf', 'file_comp_endereco']
        list = []
        for field in requireds:
            if not getattr(self, field):
                list.append(Proponente._meta.get_field(field).verbose_name)
        return list

    def is_aproved(self):
        try:
            return self.ultima_avaliacao.resultado == '1'
        except Exception:
            return False

    def get_idade(self):
        if not self.data_nascimento:
            return 99
        today = date.today()
        if type(self.data_nascimento) is str:
            self.data_nascimento = datetime.strptime(self.data_nascimento, '%Y-%m-%d')
        y = today.year - self.data_nascimento.year
        if today.month < self.data_nascimento.month or today.month == self.data_nascimento.month \
                and today.day < self.data_nascimento.day:
            y -= 1
        return y

    def submeter(self):
        if not self.submissao:
            self.submissao = datetime.now()
            self.ult_avaliacao_ok = False
            self.save()
            return True
        return False

    def is_ready_to_send(self):
        return not self.submissao \
               and (not self.get_required_fields_none())

    def set_fields_by_perfil(self, perfil):
        try:
            if not self.cpf and 'numDocumento' in perfil:
                self.cpf = perfil['numDocumento']
            if not self.nome and 'nome' in perfil:
                self.nome = perfil['nome']

            if 'indSexo' in perfil:
                self.sexo = perfil['indSexo']
            elif 'genero' in perfil:
                self.sexo = perfil['genero']

            try:
                dt = int(perfil['dataNascimento'])
                perfil['dataNascimento'] = time.strftime('%Y-%m-%d', time.localtime(dt / 1000))
            except: pass
            self.data_nascimento = perfil['dataNascimento']

            if 'numDocumentoRG' in perfil:
                self.rg = perfil['numDocumentoRG']

            if 'filiacao1' in perfil:
                self.nome_pai = perfil['filiacao1']

            if 'filiacao2' in perfil:
                self.nome_mae = perfil['filiacao2']
            elif 'filiacao' in perfil:
                self.nome_mae = perfil['filiacao']

            if 'logradouro' in perfil:
                self.logradouro = perfil['logradouro']

            if 'numLogradouro' in perfil:
                self.numero = perfil['numLogradouro']
            elif 'numero' in perfil:
                self.numero = perfil['numero']

            if 'numCEP' in perfil:
                self.cep = perfil['numCEP']
            elif 'CEP' in perfil:
                self.cep = perfil['CEP']

            if 'complemento' in perfil:
                self.complemento = perfil['complemento']
            elif 'complementoExtenso' in perfil:
                self.complemento = perfil['complementoExtenso']

            if 'contatos' in perfil:
                contatos = perfil['contatos']['contato']
                for contato in contatos:
                    if contato['codigoTipoContato'] == '129':
                        self.email = contato['descricao']
                    if contato['codigoTipoContato'] == '127':
                        s = contato['descricao']
                        self.ddd_1 = s[s.find("(") + 1:s.find(")")]
                        self.telefone_1 = s.replace("("+self.ddd_1+")", '')
                    if contato['codigoTipoContato'] == '128':
                        s = contato['descricao']
                        self.ddd_2 = s[s.find("(") + 1:s.find(")")]
                        self.telefone_2 = s.replace("("+self.ddd_2+")", '')
            elif 'contatosWSVO' in perfil:
                contatos = perfil['contatosWSVO']
                for contato in contatos:
                    if contato['tipoContatoPessoa'] == 129:
                        self.email = contato['descricao']
                    if contato['tipoContatoPessoa'] == 127:
                        s = contato['descricao']
                        self.ddd_1 = s[s.find("(") + 1:s.find(")")]
                        self.telefone_1 = s.replace("("+self.ddd_1+")", '')
                    if contato['tipoContatoPessoa'] == 128:
                        s = contato['descricao']
                        self.ddd_2 = s[s.find("(") + 1:s.find(")")]
                        self.telefone_2 = s.replace("("+self.ddd_2+")", '')
            else:
                pass
        except Exception: pass

    def save(self):
        if self.file_rg_frente:
            self.file_rg_frente = resizeImage(self.file_rg_frente)
        if self.file_rg_verso:
            self.file_rg_verso = resizeImage(self.file_rg_verso)
        if self.file_cpf:
            self.file_cpf = resizeImage(self.file_cpf)
        if self.file_comp_endereco:
            self.file_comp_endereco = resizeImage(self.file_comp_endereco)
        if self.file_dec_endereco:
            self.file_dec_endereco = resizeImage(self.file_dec_endereco)
        if self.file_livre:
            self.file_livre = resizeImage(self.file_livre)
        super(Proponente, self).save()


class Proposta(BaseModel):
    proponente = models.OneToOneField('Proponente', unique=True, related_name='p_proponente', on_delete=models.CASCADE)

    # Dados do Empreendimento
    nome_empreendimento = models.CharField(max_length=100, null=True,
                                           verbose_name='Nome do negócio que você pretende abrir ou expandir')
    bairro = models.ForeignKey('Bairro', null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='Bairro do empreendimento/Negócio')
    finalidade = models.CharField(max_length=50, choices=OBJETIVO, verbose_name='Finalidade', blank=True, null=True)
    setor = models.ForeignKey('Setor', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Setor')
    atividade = models.ForeignKey('Atividade', blank=True, null=True, on_delete=models.SET_NULL,
                                  verbose_name='Tipo de Negócio/Atividade')
    outra_renda = models.CharField(max_length=5, choices=SIM_NAO, blank=True, null=True,
                                   verbose_name='Possui outra renda fora deste negócio?')

    estudo_setor = models.CharField(max_length=5, choices=SIM_NAO, blank=True, null=True,
                                    verbose_name='Você realizou estudo de mercado em outros empreendimentos?')
    idade_cliente = models.CharField(max_length=50, verbose_name='Qual a Idade dos seus clientes?',
                                     blank=True, null=True)
    frequencia = models.CharField(max_length=50, choices=FREQUENCIA,
                                  verbose_name='Com qual frequência o cliente vai ao seu estabelecimento?',
                                  blank=True, null=True)
    tamanho_mercado = models.CharField(max_length=250, choices=TAMANHO_MERCADO,
                                       verbose_name='Qual o tamanho do mercado em que você atua ou atuará?', blank=True,
                                       null=True)
    localizacao = models.CharField(max_length=250, choices=LOCALIZACAO,
                                   verbose_name='A localização do seu empreendimento fica ou ficará', blank=True,
                                   null=True)
    estimulo_compra = models.CharField(max_length=250,
                                       verbose_name='Na sua opinião, o que estimula o seu cliente a comprar o seu produto?',
                                       blank=True, null=True)
    motivo_localizacao = models.CharField(max_length=250, choices=MOTIVO_LOCALIZACAO,
                                          verbose_name='Qual o motivo da escolha da localização do empreendimento?',
                                          blank=True, null=True)

    concorrente_atendimento = models.CharField(max_length=100, choices=AVALIACAO, blank=True, null=True)
    concorrente_qualidade = models.CharField(max_length=100, choices=AVALIACAO, blank=True, null=True)
    concorrente_localizacao = models.CharField(max_length=100, choices=AVALIACAO, blank=True, null=True)
    concorrente_preco = models.CharField(max_length=100, choices=PRECO, blank=True, null=True)
    concorrente_forma_pagamento = models.CharField(max_length=100, choices=FORMA_DE_PAGAMENTO, blank=True, null=True)
    concorrente_forma_pagamento_outra = models.CharField(max_length=250, blank=True, null=True)
    concorrente_forma_propaganda = models.CharField(max_length=100, choices=PROPAGANDA, blank=True, null=True)

    divulgacao = models.CharField(max_length=100, choices=DIVULGACAO,
                                  verbose_name='Qual vai ser o principal meio de divulgação do seu negócio?',
                                  blank=True, null=True)
    divulgacao_outra = models.CharField(max_length=250, verbose_name='Divulgação Outro', blank=True, null=True)

    submissao = models.DateTimeField(blank=True, null=True, verbose_name='Última subimissão')
    ult_avaliacao_ok = models.BooleanField(default=False, verbose_name='Avaliado')
    ultima_avaliacao = models.ForeignKey('AvaliacaoProposta', related_name='p_avaliacao', blank=True, null=True,
                                         on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Proposta de Negócio"
        verbose_name_plural = "Propostas de Negócio"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.idade_cliente:
            self.idade_cliente = eval(self.idade_cliente)
        if self.estimulo_compra:
            self.estimulo_compra = eval(self.estimulo_compra)

    # def get_status(self):
    #     if self.ultima_avaliacao and self.ult_avaliacao_ok:
    #         return format_html(
    #             '<b style="color:{};">{}!<br><a style="font-size:16px">{}</a></b><br>',
    #             dict(RESULTADOS_CORES)[self.ultima_avaliacao.resultado] if self.ultima_avaliacao else 'gray',
    #             'Classificado' if self.is_selected() else 'Não classificado',
    #             #dict(RESULTADOS)[self.ultima_avaliacao.resultado] if self.ultima_avaliacao else 'Aguardando avaliação',
    #             self.ultima_avaliacao.motivo if self.ultima_avaliacao.resultado == '0' else 'Pontuação: {}'.format(
    #                 self.pontuacao),
    #         )
    #     else:
    #         if self.submetido:
    #             return format_html('<b style="color:gray;">Aguardando avaliação!</b>')
    #         return format_html('<b style="color:black;">Aguardando envio!</b>')

    def is_aproved(self):
        try:
            return self.ultima_avaliacao.resultado == '1'
        except Exception:
            return False

    def get_required_fields_none(self):
        requireds = ['nome_empreendimento', 'bairro', 'finalidade', 'setor', 'atividade', 'outra_renda',
                     'estudo_setor', 'idade_cliente', 'frequencia', 'tamanho_mercado', 'localizacao',
                     'estimulo_compra', 'motivo_localizacao', 'concorrente_atendimento', 'concorrente_qualidade',
                     'concorrente_localizacao', 'concorrente_preco', 'concorrente_forma_pagamento', 'divulgacao']
        list = []
        for field in requireds:
            if not getattr(self, field):
                list.append(Proposta._meta.get_field(field).verbose_name)
        return list

    def is_ready_to_send(self):
        return not self.submissao \
               and (not self.get_required_fields_none()) \
               and (not self.proponente.get_required_fields_none())

    def get_idade_cliente_formatted(self):
        try:
            return ', '.join([dict(IDADE_CLIENTES).get(i) for i in list(self.idade_cliente)])
        except:
            return '-'

    # def is_selected(self):
    #     try:
    #         selecionado = Selecionado.objects.get(cpf=self.socia_gestora.cpf)
    #         return True
    #     except Selecionado.DoesNotExist:
    #         return False

    def __str__(self):
        return self.nome_empreendimento

    def submeter(self):
        if not self.submissao:
            self.submissao = datetime.now()
            self.ult_avaliacao_ok = False
            self.save()
            return True
        return False


class Investimento(BaseModel):

    proposta = models.ForeignKey('Proposta', related_name='p_proposta', on_delete=models.CASCADE)

    tipo = models.CharField(max_length=50, choices=TIPO_INV, verbose_name='Tipo')
    descricao = models.CharField(max_length=100, verbose_name='Item')
    unidade = models.CharField(max_length=5, verbose_name='Unid. Medida')
    quantidade = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)], verbose_name='Qtde')
    valor = models.DecimalField(decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(0)],
                                verbose_name='Valor unitário')

    class Meta:
        verbose_name = "Investimento"
        verbose_name_plural = "Investimentos"

    def get_verbose_name_fields(self):
        values = []
        for f in self.get_fields():
            if f.startswith('get'):
                values.append(f.replace('get_', ''))
            else:
                values.append(self._meta.get_field(f).verbose_name)
        return values

    def get_values(self):
        values = []
        for f in self.get_fields():
            values.append(getattr(self, f))
        return values

    def get_fields(self):
        return ['descricao', 'quantidade', 'unidade', 'valor']

    def validade_new(self):
        invs = Investimento.objects.filter(proposta=self.proposta).\
            extra(select={'valor_total': 'valor * quantidade'})
        total_geral = 0
        for i in invs: total_geral += i.valor_total
        if (self.valor * self.quantidade) + total_geral > VALOR_TOTAL_INVS:
            return False, 'Valor total ultrapassa o limite de R$ {}'.format(VALOR_TOTAL_INVS)
        return True, ''

    def __str__(self):
        return self.descricao


class Bairro(BaseModel):

    descricao = models.CharField(max_length=100, verbose_name='Bairro')
    idh = models.FloatField(blank=False, null=False)
    pontuacao = models.IntegerField(blank=False, null=False)

    class Meta:
         verbose_name = "Bairro"

    def __str__(self):
        return self.descricao


class BeneficiadoAnterior(BaseModel):
    cpf = models.CharField(max_length=20, verbose_name='CPF')
    nome = models.CharField(max_length=200, verbose_name='Nome')
    projeto = models.CharField(max_length=100, verbose_name='Projeto')

    class Meta:
        verbose_name = "Beneficiado Anterior"
        verbose_name_plural = "Beneficiados Anteriores"
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Atividade(BaseModel):
    setor = models.ForeignKey('Setor', max_length=100, on_delete=PROTECT, verbose_name='Setor')
    descricao = models.CharField(max_length=100, verbose_name='Ocupação')
    cnae = models.CharField(max_length=30, verbose_name='CNAE')
    atividade_cnae = models.CharField(max_length=300, verbose_name='Atividade CNAE')

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class Setor(BaseModel):
    descricao = models.CharField(max_length=100, verbose_name='Ocupação')

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setor"
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class Configs(BaseModel):
    chave = models.CharField(unique=True, max_length=50, verbose_name='Chave')
    flag = models.BooleanField(default=False, verbose_name='Ativo')
    valor = models.TextField(max_length=2000, verbose_name='Valor', blank=True, null=True)

    class Meta:
        verbose_name = "Config"
        verbose_name_plural = "Configs"

    @classmethod
    def get_valor(cls, chave):
        try:
            valor = Configs.objects.get(chave=chave).valor
        except Configs.DoesNotExist:
            valor = None
        return valor

    @classmethod
    def get_flag(cls, chave):
        try:
            flag = Configs.objects.get(chave=chave).flag
        except Configs.DoesNotExist:
            flag = False
        return flag

    def __str__(self):
        return '{}'.format(self.chave)


class LocalEntrega(BaseModel):
    descricao = models.CharField(max_length=100, verbose_name='Local')

    class Meta:
        verbose_name = "Local Entrega de Chip"
        verbose_name_plural = "Locais de Entrega de Chip"
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class AgendamentoChip(BaseModel):

    proposta = models.OneToOneField('Proposta', unique=True, related_name='ac_proposta', on_delete=models.CASCADE)
    local = models.ForeignKey('LocalEntrega', on_delete=PROTECT, verbose_name='Local Entrega')
    data = models.DateTimeField(verbose_name='Data/Hora do Agendamento')

    class Meta:
        verbose_name = "Agendamento para Entrega de Chip"
        verbose_name_plural = "Agendamento para Entrega de Chip"

    def __str__(self):
        return '{} - {}'.format(self.proposta, self.local)


class EntregaChip(BaseModel):

    proposta = models.OneToOneField('Proposta', unique=True, related_name='ec_proposta', on_delete=models.CASCADE)
    data = models.DateTimeField(verbose_name='Data/hora da entrega')
    termo = models.FileField(upload_to=upload_path_handler, blank=True, null=True, verbose_name='Termo')
    documento = models.FileField(upload_to=upload_path_handler, blank=True, null=True,
                                 verbose_name='Documento Identificação')
    foto = models.FileField(upload_to=upload_path_handler, blank=True, null=True, verbose_name='Foto da entrega')

    class Meta:
        verbose_name = "Entrega de Chip"
        verbose_name_plural = "Entrega de Chip"

    def __str__(self):
        return '{} - {}'.format(self.proposta, self.data)


class PropostaEntregaChipProxy(Proposta):
    class Meta:
        proxy = True
        verbose_name = "Entrega de Chip"
        verbose_name_plural = "Entrega de Chip"

    def __str__(self):
        return self.nome_empreendimento


class Avaliacao(BaseModel):
    resultado = models.CharField(max_length=20, choices=RESULTADOS, verbose_name='Resultado', blank=False, null=False)
    avaliador = models.ForeignKey(User, on_delete=models.PROTECT)
    motivo = models.TextField(max_length=1500, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} por {} em {}'.format(dict(RESULTADOS).get(self.resultado),
                                        self.avaliador,
                                        timezone.localtime(self.created_at).strftime('%d/%m/%Y %H:%M'))


class AvaliacaoProposta(Avaliacao):
    projeto = models.ForeignKey('Proposta', related_name='proposta_avaliado',
                                on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Avaliacao Proposta"
        ordering = ['created_at']


class AvaliacaoProponente(Avaliacao):
    proponente = models.ForeignKey('Proponente', related_name='proponente_avaliado',
                                on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Avaliacao Proponente"
        ordering = ['created_at']


class Contrato(BaseModel):
    proponente = models.OneToOneField('Proponente', unique=True, related_name='c_proponente', on_delete=models.CASCADE)
    cpf = models.CharField(max_length=30)
    file_cartao_cnpj = models.FileField(upload_to=upload_path_handler, blank=True, null=True,
                                        verbose_name='Cartao CNPJ')
    status = models.CharField(max_length=30, choices=STATUS, default='1')

    submissao = models.DateTimeField(blank=True, null=True, verbose_name='Última subimissão')
    ult_avaliacao_ok = models.BooleanField(default=False, verbose_name='Avaliado')
    ultima_avaliacao = models.ForeignKey('AvaliacaoContrato', related_name='c_avaliacao', blank=True, null=True,
                                         on_delete=models.CASCADE)

    def __str__(self):
        return self.proponente.nome

    def submeter(self):
        if not self.submissao:
            self.submissao = datetime.now()
            self.ult_avaliacao_ok = False
            self.save()
            return True
        return False


class AvaliacaoContrato(Avaliacao):
    contrato = models.ForeignKey('Contrato', related_name='contrato_avaliado',
                                on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Avaliacao Contrato"
        ordering = ['created_at']


class Capacitacoes(BaseModel):
    titulo = models.CharField(max_length=300, verbose_name='Título')
    data_aula = models.DateTimeField(null=True)
    vagas = models.IntegerField(verbose_name='Número de vagas', null=True)
    tipo_capacitacao = models.CharField(max_length=200, choices=TIPO_CAPACITACAO, null=True,
                                       verbose_name='Tipo de Capacitação')
    link = models.CharField(max_length=300, verbose_name='Link da aula virtual', null=True, blank=True)

    class Meta:
        verbose_name = "Capacitação"
        verbose_name_plural = "Capacitações"

    def __str__(self):
        return self.titulo


class Inscricao(BaseModel):
    proponente = models.OneToOneField('Proponente', on_delete=models.CASCADE, unique=True)
    capacitacao = models.ForeignKey('Capacitacoes', on_delete=models.CASCADE, verbose_name='Capacitação')
    frequencia = models.BooleanField(default=False, verbose_name='Frequência')

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Inscrições"
        verbose_name_plural = "Inscrições"
