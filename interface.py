import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from functions import ler_xml

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Conferência de Mercadorias')
        self.state('zoomed')
        self.resizable(True, True)

        # Dados da nota fiscal e bipagem
        self.produtos_nota = []
        self.scanned_data = {}  # Armazena as quantidades bipadas (valor float)
        self.produtos_nao_encontrados = []

        self.criar_widgets()

    def criar_widgets(self):
        frame_top = ttk.Frame(self)
        frame_top.pack(pady=10, fill=tk.X)

        self.btn_carregar = ttk.Button(frame_top, text="Carregar XML", command=self.carregar_xml)
        self.btn_carregar.pack(side=tk.LEFT, padx=10)

        self.btn_excluir = ttk.Button(frame_top, text="Excluir Quantidade", command=self.excluir_quantidade, state=tk.DISABLED)
        self.btn_excluir.pack(side=tk.LEFT, padx=10)

        frame_bipagem = ttk.LabelFrame(self, text="Bipagem de Produtos")
        frame_bipagem.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        self.lbl_instrucao = ttk.Label(frame_bipagem, text="Bipe o código de barras e pressione Enter")
        self.lbl_instrucao.pack(pady=5)

        self.entry_codigo = ttk.Entry(frame_bipagem, width=30)
        self.entry_codigo.pack(pady=5)
        self.entry_codigo.bind("<Return>", self.processar_bipagem)

        self.tree = ttk.Treeview(self, columns=("codigo", "descricao", "esperado", "bipado", "diferenca", "status"), show="headings")
        for col in ["codigo", "descricao", "esperado", "bipado", "diferenca", "status"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        self.btn_critica = ttk.Button(self, text="Criticar", command=self.fazer_critica, state=tk.DISABLED)
        self.btn_critica.pack(pady=10)

        self.text_area = tk.Text(self, wrap="word", state="disabled")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def carregar_xml(self):
        filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filepath:
            try:
                # Usa a função ler_xml que já agrega produtos iguais
                self.produtos_nota = ler_xml(filepath)

                if self.produtos_nota:
                    self.btn_critica["state"] = tk.NORMAL
                    self.btn_excluir["state"] = tk.NORMAL
                    messagebox.showinfo("Sucesso", "XML carregado com sucesso!")
                    self.atualizar_tabela()
                else:
                    messagebox.showwarning("Aviso", "Nenhum produto encontrado no XML!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler XML: {str(e)}")

    def processar_bipagem(self, event):
        """
        Cada vez que o código de barras é digitado e confirmado, a quantidade é
        incrementada automaticamente em 1.
        """
        codigo = self.entry_codigo.get().strip()
        self.entry_codigo.delete(0, tk.END)

        if not codigo:
            return

        # Procura o produto na lista carregada
        produto = next((p for p in self.produtos_nota if p['codigo'] == codigo), None)

        if produto:
            self.scanned_data[codigo] = self.scanned_data.get(codigo, 0.0) + 1.0
            self.atualizar_tabela()
        else:
            self.produtos_nao_encontrados.append(codigo)
            # Adiciona imediatamente na tabela com um iid exclusivo
            iid = f"nf_{codigo}"
            self.tree.insert("", "end", iid=iid, values=(
                codigo, "Produto Não Incluído", "-", "-", "-", "❌ Não Encontrado"
            ))

    def atualizar_tabela(self):
        # Limpa todos os itens da tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Preenche a tabela com os produtos carregados e os respectivos dados de bipagem.
        # Aqui definimos o iid de cada item como o próprio código do produto.
        for produto in self.produtos_nota:
            codigo = produto['codigo']
            bipado = self.scanned_data.get(codigo, 0.0)
            diferenca = bipado - produto['quantidade']
            status = "✅ OK" if abs(diferenca) < 1e-6 else "❌ Divergência"
            self.tree.insert("", "end", iid=codigo, values=(
                codigo,
                produto['descricao'],
                f"{produto['quantidade']:.2f}",
                f"{bipado:.2f}",
                f"{diferenca:+.2f}",
                status
            ))

        # Insere os produtos que não foram encontrados na nota fiscal.
        # Para estes, usamos um iid com prefixo "nf_" para diferenciá-los.
        for codigo in self.produtos_nao_encontrados:
            iid = f"nf_{codigo}"
            self.tree.insert("", "end", iid=iid, values=(
                codigo, "Produto Não Incluído", "-", "-", "-", "❌ Não Encontrado"
            ))

    def excluir_quantidade(self):
        selecionados = self.tree.selection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela!")
            return

        # Usamos o iid do item selecionado; assim, para produtos válidos, o iid é exatamente o código.
        selected_id = selecionados[0]

        # Se o iid indicar um produto "não incluído" (prefixado com 'nf_'), não permitimos a exclusão.
        if selected_id.startswith("nf_"):
            messagebox.showwarning("Aviso", "Este produto não foi bipado ainda!")
            return

        codigo = selected_id

        if codigo not in self.scanned_data or self.scanned_data[codigo] <= 0:
            messagebox.showwarning("Aviso", "Este produto não foi bipado ainda!")
            return

        # Solicita a quantidade a remover usando um diálogo simples.
        qtd_remover = simpledialog.askfloat("Excluir Quantidade", "Quantidade a remover:")
        if qtd_remover is None:
            return  # Usuário cancelou

        if qtd_remover <= 0:
            messagebox.showwarning("Aviso", "Digite um valor positivo!")
            return
        if qtd_remover > self.scanned_data[codigo]:
            messagebox.showwarning("Aviso", "A quantidade a remover é maior do que a quantidade bipada!")
            return

        self.scanned_data[codigo] -= qtd_remover
        if abs(self.scanned_data[codigo]) < 1e-6:
            del self.scanned_data[codigo]

        self.atualizar_tabela()

    def fazer_critica(self):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)

        relatorio = "**Relatório de Divergências**\n\n"
        divergencias = False

        for produto in self.produtos_nota:
            codigo = produto['codigo']
            bipado = self.scanned_data.get(codigo, 0.0)
            if abs(bipado - produto['quantidade']) > 1e-6:
                relatorio += (
                    f"Código: {codigo} | "
                    f"Descrição: {produto['descricao']} | "
                    f"Esperado: {produto['quantidade']:.2f} | "
                    f"Bipado: {bipado:.2f} | "
                    f"Diferença: {bipado - produto['quantidade']:+.2f}\n"
                )
                divergencias = True

        if self.produtos_nao_encontrados:
            relatorio += "\n**Produtos Bipados Não Encontrados na Nota:**\n"
            for codigo in self.produtos_nao_encontrados:
                relatorio += f"Código: {codigo}\n"
            divergencias = True

        if not divergencias:
            relatorio += "Oba! Sem divergências!\n"

        self.text_area.insert("1.0", relatorio)
        self.text_area.config(state="disabled")
