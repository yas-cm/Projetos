import os

comeco_caminho = "./Info"
datas = os.listdir(comeco_caminho)

def agrupar_defeitos(caminho):
    lista = os.listdir(caminho)
    for i in range(len(lista)):
        lista[i] = "_".join(lista[i].split("_")[:-1])
    defeitos = {}
    for item in lista:
        if item not in defeitos:
            defeitos[item] = lista.count(item)
    return defeitos

fotos_por_defeito = {}

for data in datas:
    caminho_data = os.path.join(comeco_caminho, data)
    if not os.path.isdir(caminho_data):
        continue
    tipos = os.listdir(caminho_data)
    for tipo in tipos:
        caminho = os.path.join(caminho_data, tipo)
        if not os.path.isdir(caminho):
            continue

        qnt_defeitos = agrupar_defeitos(caminho)
        
        for nome_defeito_base, quantidade_pastas in qnt_defeitos.items():
            chave = f"{tipo}/{nome_defeito_base}"
            if chave not in fotos_por_defeito:
                fotos_por_defeito[chave] = 0
            fotos_por_defeito[chave] += quantidade_pastas

for chave, total in fotos_por_defeito.items():
    print(f"{chave}: {total}")

with open("fotos.txt", "w", encoding="utf-8") as arquivo:
    for chave, total in fotos_por_defeito.items():
        linha = f"{chave}: {total} fotos\n"
        arquivo.write(linha)