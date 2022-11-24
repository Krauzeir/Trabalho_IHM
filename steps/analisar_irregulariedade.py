from behave import when, then
from bdd_analise import *

@when("a probabilidade de estar irregular for {probabilidade} porcento")
def when_probabilidade_de_irregular(context, probabilidade):
    context.total_de_trabalhadores_irregulares = analisar_irregulariedade(context.trabalhadores_em_reconhecimento, int(probabilidade))

@then("pelo menos um trabalhador deve receber multa")
def then_trabalhadores_irregulares(context):
    assert context.total_de_trabalhadores_irregulares > 0

@then("nenhum trabalhador recebera multa")
def then_nenhum_trabalhador_irregular(context):
    assert context.total_de_trabalhadores_irregulares == 0