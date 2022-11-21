from behave import given, when, then
from bdd_analise import *

@given("que o ambiente e dispositivos esteja preparado com sucesso")
def given_ambiente_preparado_com_sucesso(context):
    preparado, context.configuracao = preparar()

    assert preparado
    
@when("a foto {foto} de motoristas for capturada")
def when_foto_de_visitantes_capturada(context, foto):
    context.motoristas = simular_chegadas(foto)

    assert context.motoristas is not None
    
@then("pelo menos um trabalhador deve ser reconhecido")
def then_um_trabalhador_reconhecido(context):
    trabalhadores_reconhecidos, context.trabalhadores = reconhecer_trabalhadores(context.configuracao, context.motoristas)

    assert trabalhadores_reconhecidos
    
@then("pelo menos um trabalhador deve ter seu perfil analisado no banco de dados")
def then_um_trabalhador_analisado(context):
    tem_trabalhador_em_analise, context.trabalhadores_em_analise = reconhecer_motoristas(context.trabalhadores)

    assert tem_trabalhador_em_analise
    
@then("nenhum trabalhador deve ser reconhecido")
def then_nenhum_trabalhador_reconhecido(context):
    trabalhadores_reconhecidos, _ = reconhecer_trabalhadores(context.configuracao, context.motoristas)
    
    assert not trabalhadores_reconhecidos