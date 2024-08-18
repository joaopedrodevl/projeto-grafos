import os
import pandas as pd # type: ignore
import networkx as nx # type: ignore

## Pega o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

## Define o diretório dos dados
DATA_DIR = os.path.join(BASE_DIR, 'data')

## Define os arquivos de dados .csv
DATA_FILES = {
    'EMENDAS': os.path.join(DATA_DIR, 'emendas.csv'),
    'CONTRATO': os.path.join(DATA_DIR, 'contrato.csv'),
    'LICITACOES': os.path.join(DATA_DIR, 'licitacoes.csv'),
}

def main():
    ## Carrega os dados
    contratos = pd.read_csv(DATA_FILES['CONTRATO'], sep=';')
    emendas = pd.read_csv(DATA_FILES['EMENDAS'], sep=';')
    licitacoes = pd.read_csv(DATA_FILES['LICITACOES'], sep=';')
    
    ## Cria um grafo com subgrafo de emendas
    G = nx.Graph()
    G.add_node("Emendas")
    
    coluna_estado = emendas["Localidade do gasto (Regionalização)"]
    for i in range(len(coluna_estado)):
        if (coluna_estado[i] == "PARAÍBA (UF)" or coluna_estado[i].endswith("PB")):
            G.add_node("PB")
            if not G.has_edge("Emendas", "PB"):
                G.add_edge("Emendas", "PB")
            G.add_edge(emendas["Autor da emenda"][i], "PB")
            G.add_edge(emendas["Autor da emenda"][i], emendas["Função"][i], weight=float(emendas["Valor empenhado"][i].replace('.', '').replace(',', '.'))/1000000)
            
    
    gexf_file_path = os.path.join(DATA_DIR, 'grafo.gexf')
    nx.write_gexf(G, gexf_file_path)
    
if __name__ == '__main__':
    main()