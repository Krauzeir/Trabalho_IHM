Feature: verificando se existem trabalhadores para serem liberados das analises

    Scenario: um trabalhador que foi liberado da analise
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens3.jpg de motoristas for capturada
        Then pelo menos um trabalhador deve ser reconhecido
        Then pelo menos um trabalhador deve ter seu perfil analisado no banco de dados
        When a probabilidade de liberacao pelo sistema eh 100 porcento
        Then pelo menos um trabalhador deve ser liberado

    Scenario: nao existem trabalhadores para serem liberados
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens3.jpg de motoristas for capturada
        Then pelo menos um trabalhador deve ser reconhecido
        Then pelo menos um trabalhador deve ter seu perfil analisado no banco de dados
        When a probabilidade de liberacao pelo sistema eh 0 porcento
        Then nenhum trabalhador sera liberado