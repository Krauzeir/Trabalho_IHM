Feature: analisando se o trabalhador possui alguma irregulariedade (baixa ou alta)

    Scenario: um trabalhador analisado pode possuir irregulariedade ou nao
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens3.jpg de motoristas for capturada
        Then pelo menos um trabalhador deve ser reconhecido
        Then pelo menos um trabalhador deve ter seu perfil analisado no banco de dados
        When a probabilidade de estar irregular for 100 porcento
        Then pelo menos um trabalhador deve receber multa
        

    Scenario: nenhum trabalhador reconhecido possui irregulariedade
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens3.jpg de motoristas for capturada
        Then pelo menos um trabalhador deve ser reconhecido
        Then pelo menos um trabalhador deve ter seu perfil analisado no banco de dados
        When a probabilidade de estar irregular for 0 porcento
        Then nenhum trabalhador recebera multa