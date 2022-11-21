Feature: reconhecimento de trabalhadores de empresas

    Scenario: um trabalhador deve ser reconhecido entre os motoristas nas estradas a partir de video ou foto
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens1.jpg de motoristas for capturada
        Then pelo menos um trabalhador deve ser reconhecido
        Then pelo menos um trabalhador deve ter seu perfil analisado no banco de dados

    Scenario: nao deve reconhecer nenhum trabalhador quando na foto existe apenas motoristas casuais
        Given que o ambiente e dispositivos esteja preparado com sucesso
        When a foto faces/personagens5.jpg de motoristas for capturada
        Then nenhum trabalhador deve ser reconhecido

    