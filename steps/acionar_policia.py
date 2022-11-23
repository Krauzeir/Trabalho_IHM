from behave import when, then
from bdd_analise import *

@when("a probabilidade de ser uma irregulariedade alta eh {probabilidade_irregulariedade_alta} porcento")
def when_irregulariedade_alta(context, probabilidade_irregulariedade_alta):
    context.total_de_trabalhadores_presos = acionar_policia(context.trabalhadores_em_reconhecimento, int(probabilidade_irregulariedade_alta))

@then("a policia deve ser acionada para busca do trabalhador")
def then_prender_trabalhador(context):
    assert context.total_de_trabalhadores_presos >= 0

@then("o trabalhador recebera apenas a multa e sera liberado")
def then_trabalhador_com_multa(context):
    assert context.total_de_trabalhadores_presos == 0