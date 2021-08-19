TIPO_BENEFICIARIO = (
)

TIPO_LOGRAOURO = (
    ('1', u'RUA'),
    ('2', u'AVENIDA'),
    ('3', u'TRAVESSA'),
    ('3', u'VILA'),
    ('5', u'ALAMEDA'),
    ('6', u'LOTEAMENTO'),
    ('7', u'PARQUE'),
    ('8', u'PRAÇA'),
)

TIPO_CAPACITACAO = (
    ('Presencial', u'PRESENCIAL'),
    ('Virtual', U'VIRTUAl')
)

TIPO_CONTA = (
    ('1', u'CONTA CORRENTE'),
    ('2', u'CONTA POUPANCA'),
)

DV = (
    ('0', u'0'),
    ('1', u'1'),
    ('2', u'2'),
    ('3', u'3'),
    ('4', u'4'),
    ('5', u'5'),
    ('6', u'6'),
    ('7', u'7'),
    ('8', u'8'),
    ('9', u'9'),
    ('X', u'X'),
)


RESULTADOS = (
    (None, u'Não Avaliado'),
    ('0', u'Não Habilitado'),
    ('1', u'Habilitado'),
)

TIPO_TREINAMENTO = (
    ('P', u'Presencial'),
    ('O', u'Online'),
)

RESULTADOS_CORES = (
    (None, u'gray'),
    ('0', u'red'),
    ('1', u'green'),
)

SEXO = (
    ('M', u'Masculino'),
    ('F', u'Feminino'),
)

S_CONJ = (
    ('solteira', u'Solteira'),
    ('casada', u'Casada'),
    ('viuva', u'Viúva'),
    ('un_estavel', u'União Estável'),
)

ESCOLARIDADE = (
    ('sem_escolaridade', u'Sem escolaridade'),
    ('fundamental_1', u'Fundamental I – (1º ao 4º ano)'),
    ('fundamental_2', u'Fundamental II – 5º ao 9º ano'),
    ('medio_incompleto', u'Ensino Médio (2ª grau) Incompleto'),
    ('medio_completo', u'Ensino Médio (2ª grau) Completo'),
    ('superior_incompleto', u'Superior Incompleto'),
    ('superior_completo', u'Superior Completo'),
    ('pos_graduacao', u'Pós Graduação'),

)

PONT_ESCOLARIDADE = (
    (None, 0),
    ('1', 0),
    ('2', 0),
    ('3', 0),
    ('4', 0),
    ('5', 5),
    ('6', 15),
    ('7', 25),
)


MOTIVOS_PAROU_ESTUDAR = (
    ('1', u'Trabalho'),
    ('2', u'Viagem'),
    ('3', u'Problemas de Saúde'),
    ('4', u'Desinteresse'),
    ('5', u'Filho/casamento'),
    ('6', u'Situação de risco, Qual?'),
    ('7', u'Outros: Qual?'),
    ('8', u'Falta de recursos financeiros'),
)

DEFICIENCIA = (
    # ('nenhuma', u'Nenhuma'),
    ('visual', u'Visual'),
    ('auditiva', u'Auditiva'),
    ('fisica', u'Física'),
    ('outra', u'Outra, Qual?'),
)

TRABALHA_ATUAL = (
    ('sim_com_carteira', u'Sim, com carteira assinada'),
    ('sim_sem_carteira', u'Sim, sem carteira assinada'),
    ('sim_pequeno_negocio', u'Sim, abri um pequeno negócio'),
    ('nao', u'Não'),
)

RENDA_INDIVIDUAL = (
    ('ate_1SM', u'Até 1SM'),
    ('1_a_2SM', u'De 1 até 2 SM'),
    ('2_a_3SM', u'De 2 até 3 SM'),
)

RESIDENTES = (
    ('1', u'1'),
    ('2', u'2'),
    ('3', u'3'),
    ('4', u'4'),
    ('>5', u'Mais que 5'),
)

QUANTOS_RESIDEM = (
    ('0', u'Nenhuma'),
    ('1', u'1'),
    ('2', u'2'),
    ('3', u'3'),
    ('4', u'4'),
    ('5', u'5'),
    ('6', u'6'),
    ('7', u'7'),
    ('8', u'8'),
    ('9', u'9'),
    ('10', u'10'),
    ('11', u'11'),
    ('12', u'12'),
    ('13', u'13'),
    ('14', u'14'),
    ('15', u'15'),
)

RAMO_ATIVIDADE = (
    ('1', u'Confecção'),
    ('2', u'Economia Criativa'),
    ('3', u'Gastronomia'),
    ('4', u'Outro'),
)

OBJETIVO = (
    ('1', u'Implantação'),
    ('2', u'Ampliação'),
)

SIM_NAO = (
    ('nao', u'Não'),
    ('sim', u'Sim'),
)

RESULTADOS_RECURSO = (
    (None, u'Não avaliado'),
    ('0', u'Não aprovado'),
    ('1', u'Aprovado'),
)

IDADE_CLIENTES = (
    ('10', u'Crianças - Até 10 anos'),
    ('11_14', u'Adolescentes de 11 a 14 anos'),
    ('15_29', u'Jovens de 15 a 29 anos'),
    ('30_59', u'Adultos de 30 a 59 anos'),
    ('60', u'Idosos de mais de 60 anos'),
#    ('todas', u'Todas as idades'),
)

CLIENTE_MORA = (
    ('mesma_rua', u'Na mesma rua'),
    ('seu_bairro', u'No seu bairro'),
    ('bairros_vizinhos', u'Nos bairros vizinhos'),
    ('outras_cidades', u'Em outras cidades'),
    ('outros_estados', u'Em outros Estados'),
)

FREQUENCIA = (
    ('1', u'Diariamente'),
    ('3', u'Semanalmente'),
    ('4', u'Quinzenalmente'),
    ('5', u'Mensalmente'),
)

ESTIMULO_COMPRA = (
    ('forma_pagamento', u'Forma de Pagamento'),
    ('marca', u'A marca'),
    ('atendimento', u'Atendimento'),
    ('entrega', u'O prazo de entrega'),
    ('pagamento', u'O prazo de pagamento'),
    ('preco', u'Preço'),
    ('qualidade', u'Qualidade dos produtos e/ou serviços'),
)

TAMANHO_MERCADO = (
    ('sua_rua', u'É apenas na sua rua'),
    ('seu_bairro', u'No seu bairro'),
    ('bairos_vizinhos', u'Nos bairros vizinhos'),
    ('sua_cidade', u'Na sua cidade'),
    ('todo_estado', u'Todo o estado'),
)

LOCALIZACAO = (
    ('RESIDENCIA', u'Na sua residência'),
    ('LOCAL_DESTINADO', u'Em local físico destinado para o negócio'),
    ('AMBULANTE', u'Não possui local fixo – Ambulante'),
)

MOTIVO_LOCALIZACAO = (
    ('CUSTO', u'Custo'),
    ('PROXIMIDADE', u'Proximidade do cliente'),
)

AVALIACAO = (
    ('otimo', u'Ótimo'),
    ('bom', u'Bom'),
    ('regular', u'Regular'),
    ('pessimo', u'Péssimo'),
    ('n_aplica', u'Não se aplica'),
)

PRECO = (
    ('1', u'Muito barato'),
    ('2', u'Barato'),
    ('3', u'Preço justo'),
    ('4', u'Caro'),
    ('5', u'Muito caro'),
)

FORMA_DE_PAGAMENTO = (
    ('dinheiro', u'Dinheiro'),
    ('credito', u'Cartão de crédito'),
    ('debito', u'Cartão de débito'),
    ('caderneta', u'Caderneta'),
    ('boleto', u'Boleto'),
    ('Outra', u'Outra'),
)

FORNECEDOR_COND_PAGAMENTO = (
    ('vista', u'À vista'),
    ('prazo', u'À prazo'),
)

PROPAGANDA = (
    ('rede_social', u'Rede Social'),
    ('radio', u'Rádio'),
    ('lista', u'Lista/Revista de bairro'),
    ('panfleto', u'Panfletos'),
    ('folders_banners', u'Folders e Banner'),
)

DIVULGACAO = (
    ('boca_a_boca', u'Boca a boca'),
    ('rede_social', u'Rede Social'),
    ('panfleto', u'Panfletos'),
    ('banner', u'Banner'),
    ('radio', u'Rádio'),
    ('tv', u'TV'),
    ('outro', u'Outros, qual?'),
)

RAMO = (
    ('INDÚSTRIA', u'Indústria'),
    ('COMÉRCIO', u'Comércio'),
    ('SERVIÇOS', u'Serviços'),
)

TIPO_INV = (
    ('1', u'Máquinas a serem adquiridas com o recurso do financiamento'),
    ('2', u'Equipamentos a serem adquiridos com o recurso do financiamento'),
    ('3', u'Insumos a serem adquiridos com o recurso do financiamento'),
)

TIPO_INV_FINANC = ['1', '2', '4']
TIPO_INV_PROPRIO = ['3', '5']
TIPO_INV_OUTRO = ['6']

TIPO_INV_PO = (
    ('1', u'Despesas de Formalização'),
    ('2', u'Obras e/ou reformas'),
    ('3', u'Divulgação'),
    ('4', u'Curso ou Treinamento'),
    ('5', u'Outras despesas'),
)

TIPO_CUSTOS = (
    ('1', u'Matéria Prima'),
    ('2', u'Embalagem'),
    ('3', u'Frete'),
    ('4', u'Mão de obra'),
    ('5', u'Comissão de vendedores'),
    ('6', u'Impostos'),
    ('7', u'Outros'),
)

TIPO_CUSTOS_FIXOS = (
    ('1', u'Aluguel'),
    ('2', u'Condomínio'),
    ('3', u'Impostos'),
    ('4', u'Água'),
    ('5', u'Energia Elétrica'),
    ('6', u'Telefone'),
    ('7', u'Manutenção dos Equipamentos'),
    ('8', u'Material de Limpeza'),
    ('9', u'Material de Escritório'),
    ('10', u'Deslocamento'),
    ('11', u'Serviço de Terceiros'),
    ('12', u'Pró-labore'),
    ('13', u'Outras Despesas'),
)

MESES = (
    ('1', u'Janeiro'),
    ('2', u'Fevereiro'),
    ('3', u'Março'),
    ('4', u'Abril'),
    ('5', u'Maio'),
    ('6', u'Junho'),
    ('7', u'Julho'),
    ('8', u'Agosto'),
    ('9', u'Setembro'),
    ('10', u'Outubro'),
    ('11', u'Novembro'),
    ('12', u'Dezembro'),
)

ANOS = (
    ('1', u'Primeiro Ano'),
    ('2', u'Segundo Ano'),
    ('3', u'Terceiro Ano'),
    ('4', u'Quarto Ano'),
    ('5', u'Quinto Ano'),
)

STATUS = (
    ('1', u'Aguardando envio de documentação'),
    ('Documentação enviada e em análise pela equipe do Programa Nossas Guerreiras', u'Documentação enviada e em análise pela equipe do Programa Nossas Guerreiras'),
    ('3', u'Documentação analisada com sucesso sua documentação foi aceita'),
    ('4', u'Documentação analisada com sucesso sua documentação não foi aceita'),
    ('5', u'Aguardando realização da Capacitação'),
    ('6', u'Aguardando assinatura do contrato'),
    ('7', u'Aguardando publicação do contrato'),
    ('8', u'Contrato publicado, aguarde o repasse do recurso')
)

TIPO_CAPACITACAO = (
    ('Presencial', u'PRESENCIAL'),
    ('Virtual', U'VIRTUAl')
)

TIPO_NENHUM = (
    ('0', u'Itens'),
)

VALOR_TOTAL_INVS = 3000

QUERY_GET_AVALIADOR = ''' WITH 
                            avaliadores AS (
                                SELECT t1.id, t1.username, count(t4.*) as qtde
                                  FROM auth_user t1
                                  JOIN auth_user_groups t2 ON (t1.id = t2.user_id)
                                  JOIN auth_group t3 ON (t2.group_id = t3.id)
                              LEFT JOIN web_projeto t4 ON (t1.id = t4.avaliador_id)
                                WHERE t3.name = 'Avaliadores'
                              GROUP BY 1, 2
                            )
                            SELECT id
                              FROM avaliadores
                            WHERE qtde = (select min(qtde) from avaliadores)
                            LIMIT 1; 
                      '''