# Importa a biblioteca Tkinter
import tkinter as tk

# Importa o messagebox para exibir mensagens e confirmações
from tkinter import messagebox


# ============================================================
# JANELA PRINCIPAL
# ============================================================

# Cria a janela principal da aplicação
janela = tk.Tk()

# Define o título da janela
janela.title("TechBairro — Cadastro de Cliente")

# Define o tamanho da janela
janela.geometry("480x460")

# Impede que a janela seja redimensionada
janela.resizable(False, False)


# ============================================================
# CLASSE CLIENTE
# ============================================================

# A classe Cliente representa um cliente dentro do sistema
class Cliente:

    # Método construtor
    def __init__(self, nome, telefone, email, endereco):

        # Armazena os dados do cliente
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

    # Retorna os dados do cliente em uma única String
    def resumo(self):
        return f"{self.nome} | {self.telefone} | {self.email} | {self.endereco}"

    # Retorna as iniciais do nome
    #
    # Exemplo:
    # "João Victor Mendes" -> "JVM"
    def iniciais(self):

        # Divide o nome em partes
        partes = self.nome.split()

        # Pega a primeira letra de cada parte
        return "".join(
            parte[0].upper()
            for parte in partes
            if parte
        )


# ============================================================
# CLASSE GERENCIADOR DE CLIENTES
# ============================================================

# Classe responsável por armazenar e manipular os clientes
class GerenciadorClientes:

    def __init__(self):

        # Lista que armazenará os objetos Cliente
        self.clientes = []


    # ========================================================
    # CREATE
    # ========================================================

    # Adiciona um novo cliente à lista
    def adicionar(self, cliente):

        self.clientes.append(cliente)


    # ========================================================
    # READ
    # ========================================================

    # Retorna todos os clientes cadastrados
    def listar(self):

        return self.clientes


    # ========================================================
    # UPDATE
    # ========================================================

    # Atualiza um cliente existente
    def atualizar(self, indice, novo_cliente):

        # Verifica se o índice existe
        if 0 <= indice < len(self.clientes):

            # Substitui o cliente antigo pelo novo
            self.clientes[indice] = novo_cliente

            return True

        return False


    # ========================================================
    # DELETE
    # ========================================================

    # Remove um cliente existente
    def remover(self, indice):

        # Verifica se o índice existe
        if 0 <= indice < len(self.clientes):

            # Remove o cliente da posição indicada
            self.clientes.pop(indice)

            return True

        return False


    # Retorna a quantidade de clientes cadastrados
    def total(self):

        return len(self.clientes)


# ============================================================
# OBJETO GERENCIADOR
# ============================================================

# Cria o objeto responsável por gerenciar os clientes
gerenciador = GerenciadorClientes()


# Guarda o índice do cliente que está sendo editado.
#
# None significa que estamos cadastrando um cliente novo.
indice_em_edicao = None


# ============================================================
# CABEÇALHO DA INTERFACE
# ============================================================

# Cria um Frame para funcionar como cabeçalho
cabecalho = tk.Frame(
    janela,
    bg="#2c3e50"
)

cabecalho.pack(
    side="top",
    fill="x"
)


# Cria o título do sistema
tk.Label(
    cabecalho,
    text="Cadastro de Cliente",
    fg="white",
    bg="#2c3e50",
    font=("Arial", 14, "bold"),
    pady=12
).pack()


# ============================================================
# FORMULÁRIO
# ============================================================

# Cria um Frame para organizar os campos
form = tk.Frame(janela)

form.pack(
    pady=20
)


# Lista com os nomes dos campos
campos = [
    "Nome",
    "Telefone",
    "E-mail",
    "Endereço"
]


# Dicionário que armazenará os campos Entry
entradas = {}


# Percorre os campos para criar os Labels e Entrys
for i, campo in enumerate(campos):

    # Cria o Label
    tk.Label(
        form,
        text=f"{campo}:"
    ).grid(
        row=i,
        column=0,
        sticky="e",
        padx=5,
        pady=6
    )


    # Cria o campo de entrada
    entrada = tk.Entry(
        form,
        width=30
    )

    entrada.grid(
        row=i,
        column=1,
        padx=5,
        pady=6
    )


    # Guarda o Entry no dicionário
    entradas[campo] = entrada


# ============================================================
# STATUS
# ============================================================

# Label utilizada para mostrar mensagens ao usuário
status = tk.Label(
    janela,
    text="Nenhum cliente cadastrado ainda",
    fg="gray",
    wraplength=440,
    justify="left"
)

status.pack(
    pady=(0, 5)
)


# Mostra a quantidade de clientes cadastrados
contador = tk.Label(
    janela,
    text="Clientes cadastrados: 0"
)

contador.pack()


# ============================================================
# LIMPAR CAMPOS
# ============================================================

def limpar_campos():

    global indice_em_edicao

    # Percorre todos os campos
    for entrada in entradas.values():

        # Apaga o conteúdo do campo
        entrada.delete(
            0,
            tk.END
        )

    # Sai do modo de edição
    indice_em_edicao = None


# ============================================================
# VALIDAÇÃO DE E-MAIL
# ============================================================

def email_parece_valido(email):

    # Verifica se existe @ no e-mail
    if "@" not in email:

        return False


    # Divide o e-mail em usuário e domínio
    usuario, _, dominio = email.partition("@")


    # Verifica se existe usuário e ponto no domínio
    if usuario == "" or "." not in dominio:

        return False


    return True


# ============================================================
# SALVAR
# ============================================================

def salvar():

    global indice_em_edicao


    # Pega os valores digitados nos campos
    valores = {
        campo: entradas[campo].get().strip()
        for campo in campos
    }


    # Cria uma lista contendo os campos vazios
    vazios = [
        campo
        for campo in campos
        if valores[campo] == ""
    ]


    # Se houver algum campo vazio
    if vazios:

        status.config(
            text=f"Preencha o(s) campo(s): {', '.join(vazios)}",
            fg="red"
        )

        return


    # Verifica se o telefone possui somente números
    if not valores["Telefone"].isdigit():

        status.config(
            text="Telefone inválido: use somente números.",
            fg="red"
        )

        return


    # Verifica se o e-mail parece válido
    if not email_parece_valido(
        valores["E-mail"]
    ):

        status.config(
            text="E-mail inválido: use o formato nome@dominio.com",
            fg="red"
        )

        return


    # Cria um novo objeto Cliente
    cliente = Cliente(
        valores["Nome"],
        valores["Telefone"],
        valores["E-mail"],
        valores["Endereço"]
    )


    # ========================================================
    # CADASTRAR OU ATUALIZAR?
    # ========================================================

    # Se não existe um índice em edição,
    # significa que estamos cadastrando um novo cliente.
    if indice_em_edicao is None:

        gerenciador.adicionar(cliente)

        status.config(
            text=f"Cliente '{cliente.nome}' salvo com sucesso!",
            fg="green"
        )


    # Caso contrário, estamos editando um cliente existente.
    else:

        gerenciador.atualizar(
            indice_em_edicao,
            cliente
        )

        status.config(
            text=f"Cliente '{cliente.nome}' atualizado com sucesso!",
            fg="green"
        )


    # Atualiza o contador
    contador.config(
        text=f"Clientes cadastrados: {gerenciador.total()}"
    )


    # Limpa o formulário
    limpar_campos()


# ============================================================
# CANCELAR
# ============================================================

def cancelar():

    # Limpa os campos
    limpar_campos()

    # Atualiza a mensagem de status
    status.config(
        text="Formulário limpo",
        fg="gray"
    )


# ============================================================
# CONSULTA DE CLIENTES
# ============================================================

def abrir_consulta():

    # Cria uma nova janela
    consulta = tk.Toplevel(janela)

    consulta.title(
        "Consulta de Clientes"
    )

    # Define um tamanho fixo para que os botões
    # fiquem sempre visíveis
    consulta.geometry(
        "500x380"
    )

    # Impede o redimensionamento
    consulta.resizable(
        False,
        False
    )


    # ========================================================
    # LISTBOX
    # ========================================================

    # Cria a lista de clientes
    lista = tk.Listbox(
        consulta,
        width=65,
        height=12
    )

    # Não utilizamos expand=True ou fill="both".
    # Dessa forma, a Listbox não ocupa todo o espaço
    # e os botões permanecem visíveis.
    lista.pack(
        padx=10,
        pady=10
    )


    # ========================================================
    # BARRA DE ROLAGEM
    # ========================================================

    # Cria a barra de rolagem
    scrollbar = tk.Scrollbar(
        consulta
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10
    )


    # Liga a Listbox à barra de rolagem
    lista.config(
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(
        command=lista.yview
    )


    # ========================================================
    # ATUALIZAR LISTA
    # ========================================================

    def atualizar_lista():

        # Remove todos os itens da Listbox
        lista.delete(
            0,
            tk.END
        )


        # Busca os clientes cadastrados
        clientes_cadastrados = gerenciador.listar()


        # Verifica se existem clientes
        if not clientes_cadastrados:

            lista.insert(
                tk.END,
                "Nenhum cliente cadastrado"
            )

            return


        # Percorre os clientes
        for cliente in clientes_cadastrados:

            # Adiciona o resumo do cliente na Listbox
            lista.insert(
                tk.END,
                cliente.resumo()
            )


    # ========================================================
    # EDITAR CLIENTE
    # ========================================================

    def editar_cliente():

        global indice_em_edicao


        # Descobre qual cliente foi selecionado
        selecionado = lista.curselection()


        # Verifica se algum cliente foi selecionado
        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um cliente antes de editar."
            )

            return


        # Pega o índice selecionado
        #
        # Exemplo:
        # se o segundo cliente for selecionado:
        # selecionado = (1,)
        #
        # então:
        # indice_em_edicao = 1
        indice_em_edicao = selecionado[0]


        # Busca o cliente pelo índice
        cliente = gerenciador.listar()[
            indice_em_edicao
        ]


        # ====================================================
        # COLOCA OS DADOS NO FORMULÁRIO
        # ====================================================

        # Nome
        entradas["Nome"].delete(
            0,
            tk.END
        )

        entradas["Nome"].insert(
            0,
            cliente.nome
        )


        # Telefone
        entradas["Telefone"].delete(
            0,
            tk.END
        )

        entradas["Telefone"].insert(
            0,
            cliente.telefone
        )


        # E-mail
        entradas["E-mail"].delete(
            0,
            tk.END
        )

        entradas["E-mail"].insert(
            0,
            cliente.email
        )


        # Endereço
        entradas["Endereço"].delete(
            0,
            tk.END
        )

        entradas["Endereço"].insert(
            0,
            cliente.endereco
        )


        # Informa que estamos editando
        status.config(
            text=f"Editando cliente: {cliente.nome}",
            fg="blue"
        )


        # Fecha a janela de consulta
        consulta.destroy()


    # ========================================================
    # EXCLUIR CLIENTE
    # ========================================================

    def excluir_cliente():

        # Descobre qual cliente foi selecionado
        selecionado = lista.curselection()


        # Verifica se algum cliente foi selecionado
        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um cliente antes de excluir."
            )

            return


        # Pega o índice selecionado
        indice = selecionado[0]


        # Busca o cliente pelo índice
        cliente = gerenciador.listar()[indice]


        # ====================================================
        # CONFIRMAÇÃO
        # ====================================================

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",

            f"Tem certeza que deseja excluir o cadastro de "
            f"{cliente.nome}?\n\n"
            f"Essa ação não pode ser desfeita."
        )


        # Se o usuário confirmou
        if confirmar:

            # Remove o cliente
            gerenciador.remover(
                indice
            )


            # Atualiza a lista
            atualizar_lista()


            # Atualiza o contador da janela principal
            contador.config(
                text=f"Clientes cadastrados: {gerenciador.total()}"
            )


            # Atualiza o status
            status.config(
                text=f"Cliente '{cliente.nome}' excluído com sucesso!",
                fg="green"
            )


    # ========================================================
    # BOTÕES DA CONSULTA
    # ========================================================

    # Frame para organizar os botões
    botoes_consulta = tk.Frame(
        consulta
    )

    botoes_consulta.pack(
        pady=10
    )


    # Botão Editar
    tk.Button(
        botoes_consulta,
        text="Editar selecionado",
        width=18,
        command=editar_cliente
    ).grid(
        row=0,
        column=0,
        padx=5
    )


    # Botão Excluir
    tk.Button(
        botoes_consulta,
        text="Excluir selecionado",
        width=18,
        command=excluir_cliente
    ).grid(
        row=0,
        column=1,
        padx=5
    )


    # Preenche a Listbox
    atualizar_lista()


# ============================================================
# BOTÕES DA JANELA PRINCIPAL
# ============================================================

botoes = tk.Frame(
    janela
)

botoes.pack(
    pady=10
)


# Botão Salvar
tk.Button(
    botoes,
    text="Salvar",
    width=12,
    command=salvar
).grid(
    row=0,
    column=0,
    padx=5
)


# Botão Cancelar
tk.Button(
    botoes,
    text="Cancelar",
    width=12,
    command=cancelar
).grid(
    row=0,
    column=1,
    padx=5
)


# Botão Consultar
#
# A edição e a exclusão ficam dentro
# da tela de consulta.
tk.Button(
    botoes,
    text="Consultar",
    width=12,
    command=abrir_consulta
).grid(
    row=0,
    column=2,
    padx=5
)


# ============================================================
# VERSÃO
# ============================================================

# Exibe a versão do sistema no canto inferior direito
tk.Label(
    janela,
    text="v2.0",
    fg="gray"
).place(
    relx=0.97,
    rely=0.97,
    anchor="se"
)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

# Mantém a aplicação aberta
janela.mainloop()
