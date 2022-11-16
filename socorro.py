import face_recognition as reconhecedor
import colored
import secrets
import random
import simpy
import json

FOTOS_VISITANTES = [
    "faces/personagens1.jpeg",
    "faces/personagens2.jpeg",
    "faces/personagens3.jpeg",
    "faces/personagens4.jpeg"
]

ARQUIVO_DE_CONFIGURACAO = "configuracao.json"

TOTAL_DE_LEITOS_DE_UTI = 10

PROBABILIDADE_DE_LIBERACAO = 30
PROBABILIDADE_DE_SER_EMERGENCIA = 10
PROBABILIDADE_DE_ENVIO_PARA_UTI = 10
PROBABILIDADE_DE_LIBERACAO_DA_UTI = 40

TEMPO_MEDIO_DE_PERMANENCIA = 80
TEMPO_MEDIO_DE_PERMANENCIA_EM_UTI = 60

TEMPO_DE_DETECCAO_DE_PACIENTES = 40
TEMPO_DE_LIBERACAO_DE_PACIENTES = 60
TEMPO_DE_DETECCAO_DE_EMERGENCIAS = 20
TEMPO_DE_DETECCAO_DE_ENVIO_PARA_UTI = 40
TEMPO_DE_DETECCAO_DE_LIBERACAO_DA_UTI = 100

# ler configuracoes e preparar estruturas de dados


def preparar():
    global configuracao

    configuracao = None
    try:
        with open(ARQUIVO_DE_CONFIGURACAO, "r") as arquivo:
            configuracao = json.load(arquivo)
            if configuracao:
                print("arquivo de configuracao carregado")
            arquivo.close()
    except Exception as e:
        print(f"erro lendo configuração: {str(e)}")

    global pacientes_reconhecidos
    pacientes_reconhecidos = {}


def simular_visitas():
    foto = random.choice(FOTOS_VISITANTES)
    print(f"foto de visitantes: {foto}")

    visitantes = {
        "foto": foto,
        "pacientes": None
    }

    return visitantes


def paciente_reconhecido_previamente(paciente):
    global pacientes_reconhecidos

    reconhecido_previamente = False
    for reconhecido in pacientes_reconhecidos.values():
        if paciente["codigo"] == reconhecido["codigo"]:
            reconhecido_previamente = True

            break

    return reconhecido_previamente


def reconhecer_pacientes(visitantes):
    global configuracao

    print("realizando reconhecimento de pacientes...")
    foto_visitantes = reconhecedor.load_image_file(visitantes["foto"])
    caracteristicas_dos_visitantes = reconhecedor.face_encodings(
        foto_visitantes)

    pacientes = []
    for paciente in configuracao["pacientes"]:
        if not paciente_reconhecido_previamente(paciente):
            fotos = paciente["fotos"]
            total_de_reconhecimentos = 0

            for foto in fotos:
                foto = reconhecedor.load_image_file(foto)
                caracteristicas = reconhecedor.face_encodings(foto)[0]

                reconhecimentos = reconhecedor.compare_faces(
                    caracteristicas_dos_visitantes, caracteristicas)
                if True in reconhecimentos:
                    total_de_reconhecimentos += 1

            if total_de_reconhecimentos/len(fotos) >= 0.6:
                pacientes.append(paciente)
        else:
            print("paciente reconhecido previamente")

    return (len(pacientes) > 0), pacientes


def imprimir_dados_do_paciente(paciente):
    print(colored.fg('black'), colored.bg(
        'yellow'), f"paciente reconhecido em {ambiente_de_simulacao.now}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"nome: {paciente['nome']}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"idade: {paciente['idade']}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"endereço: {paciente['endereco']}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"tipo sanguíneo: {paciente['sangue']}", colored.attr('reset'))

# captura uma foto de visitantes e reconhece se tem pacientes
# entre eles


def reconhecer_visitantes(ambiente_de_simulacao):
    global pacientes_reconhecidos

    while True:
        print(
            f"tentando reconhecer um paciente entre visitantes em {ambiente_de_simulacao.now}")

        visitantes = simular_visitas()
        ocorreram_reconhecimentos, pacientes = reconhecer_pacientes(visitantes)
        if ocorreram_reconhecimentos:
            for paciente in pacientes:
                paciente["tempo_para_liberacao"] = ambiente_de_simulacao.now + \
                    TEMPO_MEDIO_DE_PERMANENCIA
                paciente["em_emergencia"] = False
                paciente["em_uti"] = False

                id_atendimento = secrets.token_hex(nbytes=16).upper()
                pacientes_reconhecidos[id_atendimento] = paciente

                imprimir_dados_do_paciente(paciente)

        yield ambiente_de_simulacao.timeout(TEMPO_DE_DETECCAO_DE_PACIENTES)


# identifica pacientes que podem ser liberados
# nao pode liberar quem estah em uti

# def liberar_paciente(ambiente_de_simulacao):
#     global pacientes_reconhecidos

#     while True:
#         print(
#             f"tentando liberar um paciente em {ambiente_de_simulacao.now}")

#         if len(pacientes_reconhecidos):
#             for id_atendimento, paciente in list(pacientes_reconhecidos.items()):
#                 if not paciente["em_uti"] and ambiente_de_simulacao.now >= paciente["tempo_para_liberacao"]:
#                     paciente_liberado = (random.randint(
#                         1, 100)) <= PROBABILIDADE_DE_LIBERACAO
#                     if paciente_liberado:
#                         pacientes_reconhecidos.pop(id_atendimento)
#                         print(colored.fg('white'), colored.bg('green'),
#                               f"liberando {paciente['nome']} em {ambiente_de_simulacao.now}", colored.attr('reset'))

#         yield ambiente_de_simulacao.timeout(TEMPO_DE_LIBERACAO_DE_PACIENTES)

# elege entre os pacientes aqueles q estao em situacao critica


# def identificar_emergencia(ambiente_de_simulacao):
#     global pacientes_reconhecidos

#     while True:
#         print(
#             f"tentando identificar uma emergência em {ambiente_de_simulacao.now}")

#         if len(pacientes_reconhecidos):
#             for id_atendimento, paciente in list(pacientes_reconhecidos.items()):
#                 if not paciente["em_emergencia"]:
#                     emergencia_reconhecida = (random.randint(
#                         1, 100) <= PROBABILIDADE_DE_SER_EMERGENCIA)
#                     if emergencia_reconhecida:
#                         pacientes_reconhecidos[id_atendimento]["em_emergencia"] = True
#                         print(colored.fg('white'), colored.bg('blue'),
#                               f"paciente {paciente['nome']} em situação de emergência em {ambiente_de_simulacao.now}", colored.attr('reset'))

#         yield ambiente_de_simulacao.timeout(TEMPO_DE_DETECCAO_DE_EMERGENCIAS)


# def contar_pacientes_em_uti():
#     global pacientes_reconhecidos

#     pacientes_em_uti = 0
#     for paciente in pacientes_reconhecidos.values():
#         if paciente["em_uti"]:
#             pacientes_em_uti += 1

#     return pacientes_em_uti

# # se paciente estiver em situacao de emergencia, identifica se
# # ele precisa ser transferido para a uti
# # nao pode enviar paciente se a capacidade maxima for extrapolada


# def reservar_uti(ambiente_de_simulacao):
#     global pacientes_reconhecidos

#     while True:
#         print(
#             f"tentando identificar uma transferência para a UTI em {ambiente_de_simulacao.now}")

#         if len(pacientes_reconhecidos) and contar_pacientes_em_uti() >= TOTAL_DE_LEITOS_DE_UTI:
#             print(
#                 f"capacidade maxima de uti ultrapassada em {ambiente_de_simulacao.now}")
#         else:
#             for paciente in pacientes_reconhecidos.values():
#                 if paciente["em_emergencia"] and not paciente["em_uti"]:
#                     enviar_para_uti = (random.randint(
#                         1, 100)) <= PROBABILIDADE_DE_ENVIO_PARA_UTI
#                     if enviar_para_uti:
#                         paciente["tempo_para_liberacao_da_uti"] = ambiente_de_simulacao.now + \
#                             TEMPO_MEDIO_DE_PERMANENCIA_EM_UTI
#                         paciente["em_uti"] = True
#                         print(colored.fg('white'), colored.bg(
#                             'red'), f"paciente {paciente['nome']} enviado para a uti em {ambiente_de_simulacao.now}", colored.attr('reset'))

#         yield ambiente_de_simulacao.timeout(TEMPO_DE_DETECCAO_DE_ENVIO_PARA_UTI)

# # libera um paciente que ocupa um leito de uti


# def liberar_leito_da_uti(ambiente_de_simulacao):
#     global pacientes_reconhecidos

#     while True:
#         print(
#             f"tentando identificar uma liberação de UTI em {ambiente_de_simulacao.now}")

#         if len(pacientes_reconhecidos):
#             for paciente in pacientes_reconhecidos.values():
#                 if paciente["em_uti"] and ambiente_de_simulacao.now >= paciente["tempo_para_liberacao_da_uti"]:
#                     paciente_liberado = (random.randint(
#                         1, 100)) <= PROBABILIDADE_DE_LIBERACAO_DA_UTI
#                     if paciente_liberado:
#                         paciente["em_uti"] = False
#                         print(colored.fg('white'), colored.bg(
#                             'green'), f"paciente {paciente['nome']} liberado da uti em {ambiente_de_simulacao.now}", colored.attr('reset'))

#         yield ambiente_de_simulacao.timeout(TEMPO_DE_DETECCAO_DE_LIBERACAO_DA_UTI)


if __name__ == "__main__":
    preparar()

    ambiente_de_simulacao = simpy.Environment()
    ambiente_de_simulacao.process(reconhecer_visitantes(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(liberar_paciente(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(identificar_emergencia(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(reservar_uti(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(liberar_leito_da_uti(ambiente_de_simulacao))
    ambiente_de_simulacao.run(until=1000)
