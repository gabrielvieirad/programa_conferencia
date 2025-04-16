import xml.etree.ElementTree as ET
from tkinter import messagebox

def parse_xml(file_path):
    """
    Lê e processa um arquivo XML e retorna uma lista de produtos.
    Cada produto é um dicionário contendo 'codigo', 'descricao', 'quantidade' e 'unidade'.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        produtos = []

        # Procura elementos <det> – se necessário, ajuste o caminho ou namespace conforme o XML utilizado
        for item in root.findall(".//det"):
            codigo_elem = item.find(".//cEAN")
            codigo = codigo_elem.text.strip() if (codigo_elem is not None and codigo_elem.text) else "SEM_CODIGO"

            descricao_elem = item.find(".//xProd")
            descricao = descricao_elem.text.strip() if (descricao_elem is not None and descricao_elem.text) else "DESCONHECIDO"

            quantidade_elem = item.find(".//qCom")
            try:
                quantidade = float(quantidade_elem.text.strip()) if (quantidade_elem is not None and quantidade_elem.text) else 0.0
            except ValueError:
                quantidade = 0.0

            unidade_elem = item.find(".//uCom")
            unidade = unidade_elem.text.strip() if (unidade_elem is not None and unidade_elem.text) else "UN"

            produtos.append({
                "codigo": codigo,
                "descricao": descricao,
                "quantidade": quantidade,
                "unidade": unidade
            })

        return produtos
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler XML: {e}")
        return []
