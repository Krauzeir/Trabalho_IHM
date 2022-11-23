Feature: Analisando a irregulariedade do trabalhador para apreender ou nao

    Scenario: Um trabalhador teve irregulariedade alta e deve ser preso
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens2.jpg de motoristas for capturada
        Then pelo menos um trabalhador deve ser reconhecido
        Then pelo menos um trabalhador deve ter seu perfil analisado no banco de dados
        When a probabilidade de estar irregular for 100 porcento
        When a probabilidade de ser uma irregulariedade alta eh 100 porcento
        Then a policia deve ser acionada para busca do trabalhador

    Scenario: Um trabalhador teve irregulariedade baixa, recebe a multa e eh liberado
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens3.jpg de motoristas for capturada
        Then pelo menos um trabalhador deve ser reconhecido
        Then pelo menos um trabalhador deve ter seu perfil analisado no banco de dados
        When a probabilidade de estar irregular for 100 porcento
        When a probabilidade de ser uma irregulariedade alta eh 0 porcento
        Then o trabalhador recebera apenas a multa e sera liberado