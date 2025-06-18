import os

comeco_caminho = "Projetos\Contador_de_fotos\Info" # Pasta com as fotos
datas = os.listdir(comeco_caminho)  # Lista todas as pastas de datas

# Função que agrupa nomes de defeitos ignorando o ID final
def agrupar_defeitos(caminho):
    lista = os.listdir(caminho)
    for i in range(len(lista)):
        lista[i] = "_".join(lista[i].split("_")[:-1])  # Tira o ID
    defeitos = {}
    for item in lista:
        if item not in defeitos:
            defeitos[item] = lista.count(item)  # Conta quantas vezes cada defeito aparece
    return defeitos

qnt_defeitos = []

# Pegar todos os tipos nas datas
for data in datas:
    caminho_data = os.path.join(comeco_caminho, data)
    if not os.path.isdir(caminho_data):  # Ignora se não for pasta
        continue
    tipos = os.listdir(caminho_data)  # Lista os tipos de bico

# Dicionário final: chave = tipo/defeito, valor = total de fotos
fotos_por_defeito = {}

# Percorre todas as datas e tipos
for data in datas:
    caminho_data = os.path.join(comeco_caminho, data)
    if not os.path.isdir(caminho_data):
        continue
    tipos = os.listdir(caminho_data)
    for tipo in tipos:
        caminho = os.path.join(caminho_data, tipo)
        if not os.path.isdir(caminho):
            continue

        qnt_defeitos = agrupar_defeitos(caminho)  # Agrupa os defeitos ignorando IDs
        lista = os.listdir(caminho)  # Lista todas as pastas de defeitos com ID

        fotos = 0  # Contador de fotos
        cont = 1  # Contador de pastas lidas
        valor = 0  # Índice atual da lista de quantidades
        valores = list(qnt_defeitos.values()) 
        for i in lista:
            caminho_pasta = os.path.join(caminho, i)
            if not os.path.isdir(caminho_pasta):
                continue
            pasta_fotos = os.listdir(caminho_pasta)  # Lista fotos da pasta
            for f in pasta_fotos:
                fotos += 1
            cont += 1
            if cont == valores[valor] + 1:
                nome_defeito = "_".join(i.split("_")[:-1])  # Remove ID final da pasta
                chave = f"{tipo}/{nome_defeito}"  # Junta tipo + nome do defeito
                if chave not in fotos_por_defeito:
                    fotos_por_defeito[chave] = 0
                
                fotos_por_defeito[chave] = [fotos,qnt_defeitos[nome_defeito]]  # Soma total de fotos para esse tipo/defeito
                print(f"{chave}: {fotos}, {qnt_defeitos[nome_defeito]}")
                fotos = 0
                cont = 1
                valor += 1

# Gera o arquivo de saída com os totais
with open("fotos.txt", "w", encoding="utf-8") as arquivo:
    for chave, (fotos, bicos) in fotos_por_defeito.items():
        linha = f"{chave}: {fotos} fotos, {bicos} bicos\n"
        arquivo.write(linha)
