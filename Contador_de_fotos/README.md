# 📷 Análise de Fotos de Defeitos

Este script automatiza o processo de contagem e classificação de fotos de defeitos em bicos injetores. Ele lê uma estrutura de diretórios, agrupa os dados por tipo e defeito, e gera um relatório analítico detalhado em uma planilha Excel.

Este projeto foi desenvolvido com o objetivo de visualizar de maneira mais eficiente a quantidade de fotos tiradas para o dataset de aprendizado que será implementado pelo setor de Sistemas de Visão na área de automação da Bosch.

---

## 💡 Funcionalidades Principais

-   **Análise Inteligente de Pastas:** Navega por diferentes tipos de estruturas de diretórios, identificando corretamente as pastas de dados, mesmo que misturadas com outras.
-   **Agrupamento Flexível de Defeitos:** Identifica e agrupa defeitos pelo nome base, ignorando variações de ID no final do nome da pasta (ex: `_ID12345`).
-   **Descoberta Automática de Tipos:** Antes de processar, o script "aprende" quais são os tipos de peças válidos a partir de pastas que contêm data, garantindo que apenas pastas relevantes sejam analisadas.
-   **Relatório Multi-abas:** Gera um único arquivo Excel com três planilhas distintas para facilitar a análise:
    1.  `Todos os Defeitos`: Visão consolidada de todos os dados.
    2.  `Críticos`: Apenas os defeitos com menos de x fotos, para análise prioritária.
    3.  `Bons`: Os defeitos com x ou mais fotos.
-   **Visualização Rápida:** Aplica formatação condicional de cores (verde, amarelo e vermelho) nas planilhas, permitindo uma identificação visual imediata da criticidade de cada item.

---

## ⚙️ Instalação e Configuração

Para executar este projeto, você precisará do Python 3 instalado.

1.  **Clone o repositório principal (se ainda não o fez):**
    ```bash
    git clone 
    ```

2.  **Navegue até a pasta deste projeto:**
    ```bash
    cd Projetos/Contador_de_fotos
    ```

3.  **Instale as dependências necessárias:**
    ```bash
    pip install xlsxwriter
    ```

---

## ▶️ Como Executar

### 1. Estrutura das Pastas de Entrada

O script foi projetado para ler as informações de uma pasta chamada `Info`, que está populada com alguns exemplos de defeitos para fins de teste.

### 2. Execute o Script

Estando na pasta `Projetos\Contador_de_fotos\Program\main.py`, execute o seguinte comando no seu terminal:

```bash
python main.py
```

### 3. Analise o Resultado

Um arquivo chamado Fotos_Completo.xlsx será gerado dentro da pasta projeto_analise_fotos. Abra-o para ver o relatório completo nas três abas.