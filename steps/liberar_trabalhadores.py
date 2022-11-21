from behave import when, then
from bdd_analise import *

@when("a probabilidade de liberacao pelo sistema eh {probabilidade} porcento")
def when_probabilidade_de_liberacao(context, probabilidade):
    context.total_de_trabalhadores_liberados = liberar_trabalhador(context.trabalhadores_em_reconhecimento, int(probabilidade))

@then("pelo menos um trabalhador deve ser liberado")
def then_trabalhadores_liberados(context):
    assert context.total_de_trabalhadores_liberados > 0

@then("nenhum trabalhador sera liberado")
def then_nenhum_trabalhador_liberado(context):
    assert context.total_de_trabalhadores_liberados == 0