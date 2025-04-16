# functions.py
import xml.etree.ElementTree as ET
from tkinter import messagebox

def ler_xml(caminho_xml):
    """
    Lê um arquivo XML de NFe e extrai informações dos produtos,
    retornando uma lista de dicionários com código, descrição, quantidade e unidade.
    """
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        produtos = {}
        
        namespaces = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    
        for det in root.findall('.//nfe:det', namespaces):
            # Obter código de barras (tenta cEAN e cBarra)
            codigo_elem = det.find('.//nfe:cEAN', namespaces)
            if codigo_elem is None:
                codigo_elem = det.find('.//nfe:cBarra', namespaces)
            codigo = codigo_elem.text.strip() if codigo_elem is not None and codigo_elem.text else "SEM_CODIGO"
    
            # Obter descrição
            desc_elem = det.find('.//nfe:xProd', namespaces)
            descricao = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else "Sem Descrição"
    
            # Obter quantidade e converter para inteiro
            qtd_elem = det.find('.//nfe:qCom', namespaces)
            try:
                quantidade = int(float(qtd_elem.text.strip())) if qtd_elem is not None and qtd_elem.text else 0
            except Exception:
                quantidade = 0
            
            # Obter unidade
            unidade_elem = det.find('.//nfe:uCom', namespaces)
            unidade = unidade_elem.text.strip() if unidade_elem is not None and unidade_elem.text else "UN"
    
            # Agregar produtos com mesmo código
            if codigo in produtos:
                produtos[codigo]['quantidade'] += quantidade
            else:
                produtos[codigo] = {
                    'codigo': codigo,
                    'descricao': descricao,
                    'quantidade': quantidade,
                    'unidade': unidade
                }
    
        return list(produtos.values())
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler XML: {e}")
        return []
