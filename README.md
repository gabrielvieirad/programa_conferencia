# 📦 Conferência de Mercadorias

Aplicação desktop desenvolvida em **Python** com **Tkinter** para conferência de mercadorias com base em arquivos **XML de Nota Fiscal**.  
Permite bipagem automática dos produtos, verificação de divergências e correção manual das contagens.

---

## 📌 Funcionalidades

✅ Leitura de arquivos XML de notas fiscais com suporte a namespace NFe  
✅ Bipagem automática (1 unidade por código escaneado)  
✅ Detecção de divergências entre esperado e bipado  
✅ Exclusão de quantidade incorreta com validação  
✅ Relatório textual de divergências  
✅ Interface gráfica intuitiva com **Tkinter**

---

## 💻 Tecnologias Utilizadas

- Python 3.x  
- Tkinter (GUI)  
- xml.etree.ElementTree (leitura de XML)

---

## 🚀 Instalação

1. Instale o Python 3: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/conferencia-mercadorias.git
cd conferencia-mercadorias
```
3. Execute o programa:
```bash
python main.py

Obs: o tkinter já vem com a maioria das distribuições do Python. Caso necessário:

- "Linux: sudo apt install python3-tk"

- "Windows/macOS: já incluso"
```
---

## 🧭 Como Usar

1. Carregar XML
- Clique em "Carregar XML"
- Selecione o arquivo XML da nota fiscal
- O sistema irá agrupar os produtos pelo código de barras

2. Bipagem de Produtos
- Digite ou escaneie o código de barras no campo e pressione Enter
- A cada bip, a contagem é incrementada em 1
- Produtos desconhecidos serão adicionados à lista como "Produto Não Incluído"

3. Excluir Quantidade
- Selecione o item na tabela
- Clique em "Excluir Quantidade"
- Digite a quantidade a ser removida
- O sistema valida para evitar remoção maior que a quantidade registrada

4.  Gerar Relatório
- Clique em "Criticar"
- Será exibido um relatório das divergências entre o XML e os produtos bipados
---

## 📂 Estrutura do Projeto
```bash
conferencia-mercadorias/
├── build/                # (gerado pelo empacotador, se usado)
├── dist/                 # (distribuição executável, opcional)
├── functions.py          # Função principal para leitura e parsing do XML
├── interface.py          # Interface gráfica e lógica da aplicação
├── main.py               # Ponto de entrada do programa
├── utils.py              # Funções auxiliares para XML (opcional)
└── README.md             # Este arquivo
```
---

## 📈 Fluxo de Funcionamento

- **Carregamento XML:** Lê e agrupa produtos do arquivo XML da NFe  
- **Bipagem Automática:** A cada código inserido, adiciona 1 à contagem  
- **Exclusão de Contagem:** Corrige erros de bipagem com caixa de diálogo  
- **Relatório:** Compara esperado x bipado e exibe divergências  

---

## 🤝 Contribuindo

1. Faça um fork  
2. Crie uma branch:  
```bash
git checkout -b minha-feature
```
3. Commit suas alterações:
```bash
git commit -m 'Minha contribuição'
```
4. Envie para o GitHub:
```bash
git push origin minha-feature
```
3. Crie um Pull Request 🚀

---

## ⚖️ Licença
Distribuído sob a licença MIT.
Sinta-se livre para usar, modificar e compartilhar.
