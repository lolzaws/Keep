from customtkinter import CTk, CTkFrame, \
CTkButton, CTkLabel, CTkTextbox, CTkTabview,\
 CTkEntry, CTkScrollbar, set_appearance_mode,\
  set_default_color_theme, CTkFont, set_widget_scaling
from pathlib import Path
from json import dumps, loads
from time import time
from os import path
from config import notebook, readnote, newnote, title, content, save, delete, cancel, title, content, APP_TITLE

import datetime


# Coloração do tema
set_appearance_mode('dark')
set_default_color_theme("blue")

# TODO: Implementar o escalonamento dinâmico
#set_widget_scaling()

# Datapath é onde as notas normais estão.
DATAPATH = '.keep'
# Bookpath é onde o texto escrito na aba Bloco de Notas está.
BOOKPATH = '.book'

# As notas são salvas em um arquivo json por enquanto. Essas são
# as respectivas variaveis-chaves de título, conteúdo e data, respectivamente.
json_data_title_key = 'title'
json_data_content_key = 'content'
json_data_date_key = 'date'

"""
 Gambiarra temporária que virou feature: uma função que interopera com
 Arquivos json e txt.
os modos são:
w - "write", escreve no arquivo json
r - "read", le o arquivo json
rs - "read string", le arquivo .txt
ws - "write string", escreve arquivo de texto

Parâmetros:
data - os dados a serem escritos, tipo dict ou string
mode - modo de operação, padrão escrever, "w"

retorna dicionario se o modo for de leitura "r"/"rs" ou None nada
"""
def json_files_op(path: str, data: dict|str = {}, mode='w') -> dict|None:
    def check(path: str, data = None, target=None):
        if Path(path).exists():
            return True
        return False

    if check(path) == False:
        with open(path, 'w') as f:
            f.write("{}")
            f.close()

    if mode == "w":
        with open(path, "w") as f:
            f.write(dumps(data))

    elif mode == 'r':
        with open(path, "r") as f:
            return loads(f.read())

    elif mode == 'rs': # read string
        with open(path, "r") as f:
            return f.read()

    elif mode == 'ws': # write string
        with open(path, 'w') as f:
            f.write(data)
    else:
        print("Mode {mode} does not exist. Check.")

    return


# Classe principal
class Main(CTk):
    def __init__(self):
        self.database: dict = {}
        self.notebook: str = ""

        # active_note: variavel que identifica a nota selecionada na aba
        # "read notes", para ser possivel apagar e editar, por padrão nenhuma nota está selecionada.
        self.active_note: str | None = None
        # TODO: Implementar reversão de historico com CRTL-Z e CRTL-Y
        self.history = [] #

        self.database = json_files_op(DATAPATH, mode='r')
        self.notebook = json_files_op(BOOKPATH, mode='rs')
        # Mero esteticismo
        if "{" in self.notebook:
            self.notebook = ""

        # Chama o construtor da classe mãe CTk
        super().__init__()
        # Título
        self.title(APP_TITLE)
        # Tamanho base da janela, o correto é um calculo matemático determinando N x e N y da tela.
        # Mas por enquanto vai ficar assim.
        self.geometry("585x375")
        self.iconbitmap("ico.ico")
        # Fonte, Ubuntu tamanho 18
        self.cfont = CTkFont(family="Ubuntu", size=18)

        # Exit Protocols - protocolos de saída(do programa)
        # janela sendo fechada(x), salva bloco de notas
        self.protocol("WM_DELETE_WINDOW", self.on_notebook_change)
        # ESC pressioada, salva Bloco de Notas
        self.protocol("Esc", self.on_notebook_change)
        # Alt + F4, salva bloco de notas e fecha programa
        self.protocol("Alt F4", self.on_notebook_change)


        # This tab rules everything - tabview, contem todas as 3 tabs
        self.tab = CTkTabview(self)
        # Adding frames to tab
        self.tab.add(notebook)
        self.tab.add(readnote)
        self.tab.add(newnote)

        # tab padrão: Bloco de Notas
        self.tab.set(notebook)
        self.tab.pack(side='left', fill='both', expand=1)

        # Two frames for two tabs
        FrameCreateNote = CTkFrame(self.tab.tab(newnote))
        self.FrameViewNotes = CTkFrame(self.tab.tab(readnote))

        # Show text here when clicked
        self.FrameViewText = CTkFrame(self.tab.tab(readnote), bg_color="transparent")
        self.FrameViewDateTitle = CTkFrame(self.FrameViewText, bg_color="transparent")
        self.FrameViewButtons = CTkFrame(self.tab.tab(readnote))# Where the buttons are located


        # Layout Bloco de Notas
        self.FrameNotebook = CTkFrame(self.tab.tab(notebook))
        self.EntryNotebook = CTkTextbox(self.FrameNotebook,  corner_radius=1, font=self.cfont)
        self.FrameNotebook.pack(expand=1, fill='both')
        self.EntryNotebook.pack(expand=1, fill='both')
        #self.EntryNotebook.bind("<<Modified>>", self.on_notebook_change)
        if self.notebook != 0:
            self.EntryNotebook.insert("1.0", self.notebook.strip("\n"))

        FrameLabelTitle = CTkFrame(self.tab.tab(newnote))
        #FrameLabelTitle.pack(fill='x')

        FrameEntryTitle = CTkFrame(self.tab.tab(newnote))
        FrameEntryTitle.pack(fill='x')

        FrameLabelContent = CTkFrame(self.tab.tab(newnote))
        FrameLabelContent.pack(fill='x')

        FrameEntryContent = CTkFrame(self.tab.tab(newnote))
        FrameEntryContent.pack(fill='both', expand=True)

        FrameSaveButton = CTkFrame(self.tab.tab(newnote))
        FrameSaveButton.pack(fill='x')

        # Labels - Textos
        labelTitle = CTkLabel(FrameLabelTitle, text=title, font=self.cfont)
        labelTitle.pack(side='left')
        labelContent = CTkLabel(FrameLabelContent, text=content, font=self.cfont)
        labelContent.pack(side='left', fill='x')

        # Inputs - Entradas de texto
        # Entrada de título
        self.entryTitle = CTkEntry(FrameEntryTitle, placeholder_text=title, font=self.cfont)
        self.entryTitle.pack(fill='x', expand=True)

        # Entrada de conteúdo
        contentscroll = CTkScrollbar(FrameEntryContent)
        self.entryContent = CTkTextbox(FrameEntryContent, font=self.cfont)
        self.entryContent.pack(fill='both', expand=True)

        # Botões salvar e cancelar
        btnSave = CTkButton(FrameSaveButton, text=save, command=self.save_note, font=self.cfont)
        btnSave.pack(side='left', expand=1, fill='x', padx=2)
        btnCancel = CTkButton(FrameSaveButton, text=cancel, command=self.cancel, font=self.cfont)
        btnCancel.pack(side='left', expand=1, fill='x', padx=2)


        # layout das notas salvas
        self.FrameViewText.pack(side='right', fill='both', expand=1)
        self.FrameViewDateTitle.pack(fill='x', expand=0)

        self.FrameViewTitle = CTkFrame(self.FrameViewDateTitle, height=30, corner_radius=0)
        self.LabelTitle = CTkLabel(self.FrameViewTitle, text="", font=self.cfont)
        self.FrameViewTitle.pack(side='left', expand=1, fill='x')

        self.FrameViewDate = CTkFrame(self.FrameViewDateTitle, height=30, corner_radius=0)
        self.LabelDate = CTkLabel(self.FrameViewDate, font=self.cfont, text="")
        self.FrameViewDate.pack(side='right')

        self.view_text = CTkTextbox(self.FrameViewText, corner_radius=0, font=self.cfont)
        self.view_text.pack(expand=1, fill='both')
        self.FrameViewEdit = CTkFrame(self.FrameViewText, height=30)
        self.FrameViewEdit.pack(fill='x', side="bottom")

        # Botão editar
        self.BtnEditSave = CTkButton(self.FrameViewEdit, text=save, command=self.edit, font=self.cfont)
        # Botão deletar
        self.BtnEditDelete = CTkButton(self.FrameViewEdit, text=delete, command=self.delete, font=self.cfont)

        self.BtnEditSave.pack(side='left', fill='both', expand=1, padx=2)
        self.BtnEditDelete.pack(side='left', fill='both', expand=1, padx=2)

        # Os botões para cada nota estão aqui, se nenhuma nota houver, mostra um texto "Sem notas."
        self.LabelNoNotes = CTkLabel(self.tab.tab(readnote), text="Sem notas.", font=self.cfont)


        self.update() # atualiza a base de dados na ram, para as notas aparecerem.

        # Pack tab
        self.mainloop()


    def update(self):
        if len(self.database) != 0:
            if self.LabelNoNotes != None:
                self.LabelNoNotes.destroy()
            self.FrameViewButtons.destroy()
            self.FrameViewButtons = CTkFrame(self.tab.tab(readnote))# Where the buttons are located
            self.FrameViewButtons.pack(padx=10)

            for key in self.database:
                text = self.database[key][json_data_title_key]
                if len(text) > 12:
                # Adiciona 3 pontos no botão da nota caso seja muito grande o título.
                    text = text[:12] + '...'
                CTkButton(self.FrameViewButtons, text=text, command=lambda x=key:self.read(x), font=self.cfont)\
                .pack(expand=1, pady=2, fill='x')

        else:
            if self.FrameViewButtons != None:
                self.FrameViewButtons.destroy()
                self.LabelNoNotes = CTkLabel(self.tab.tab(readnote), text="Sem notas.", font=self.cfont)# Where the buttons are located
            self.LabelNoNotes.pack(side='top', expand=1, fill='x', padx=25)


    def save_note(self, edited: bool = False):
        if self.entryTitle.get() != "" or edited:
            index = len(self.database) + 1
            self.database[index] = {
                    json_data_title_key: self.entryTitle.get(),
                    json_data_content_key: self.entryContent.get("1.0", 'end').strip('\n'),
                    json_data_date_key: time()
                }
            json_files_op(DATAPATH, self.database)
            self.entryContent.delete("1.0", 'end')
            self.entryTitle.delete(0, 'end')

        self.update()


    # Limpa as entradas
    def cancel(self):
        self.entryContent.delete(0, 'end')
        self.entryTitle.delete(0, 'end')


    # Chamada no evento de mudança no texto na entrada de texto da aba
    # Bloco de Notas e salva os textos
    def on_notebook_change(self, event = None):
        self.notebook = self.EntryNotebook.get("1.0", 'end').strip('\n')
        json_files_op(BOOKPATH, self.notebook, mode='ws')
        self.EntryNotebook.edit_modified(False)
        self.destroy()

    # Escreve nota na entrada de texto self.FrameViewText e a data de criação
    # no widget de self.LabelDate
    def read(self, key):
        self.view_text.delete("1.0", 'end')
        date = datetime.datetime.fromtimestamp(int(self.database[key][json_data_date_key])).date()
        self.active_note = key

        if self.LabelDate != None:
            self.LabelDate.destroy()
            self.LabelTitle.destroy()

        self.LabelTitle = CTkLabel(self.FrameViewTitle, font=self.cfont, text=self.database[key][json_data_title_key], corner_radius=0)
        self.LabelTitle.pack(side="left", fill='x')
        self.LabelDate = CTkLabel(self.FrameViewDate, font=self.cfont, text=date, corner_radius=0)
        self.LabelDate.pack(side="right", fill='x')
        self.view_text.insert("1.0", self.database[key][json_data_content_key])

    # Chamada no evento de clique no botão editar
    def edit(self):
        self.database[self.active_note][json_data_content_key] = self.view_text.get("1.0", 'end').strip("\n")
        self.save()

    # Chamada no evento de clique no botão deletar
    def delete(self):
        self.LabelDate.destroy()
        self.LabelTitle.destroy()
        self.view_text.delete("1.0", "end")
        del self.database[self.active_note]
        self.active_note = None
        self.save()
        self.update()

    # TODO finish these methods
    # Funções de encriptação, ainda sem desenvolvimento
    def encrypt(self):
        ...

    def decrypt(self):
        ...

    # Destroi os conteineres de widgets de texto, entrada para atualizar a tela
    def destroy_widgets(self, widget_group_id):
        groups = {
            "n": [],
            "cn": [],
            'rn': [self.LabelDate, self.LabelTitle]
        }
        if widget_group_id in groups:
            [widget.destoy() for widget in groups[widget_group_id]]

    # A ser removido por desuso.
    def save(self): # Deprecated
        json_files_op(DATAPATH, self.database)

Main()
