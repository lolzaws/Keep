#Database configs
db_dir = ""
dbname = ".keep"

# Table ids
# db_id, id, name, username, chat_with, message

default_tables = "db_id INTEGER PRIMARY KEY AUTOINCREMENT, json TEXT NOT NULL"
MAIN = 'main'

table_layouts = {
    MAIN: default_tables
}
check_data_table = "SELECT {} FROM {} WHERE"
init_table = "CREATE TABLE IF NOT EXISTS '{}' ({})"
insert_data = "INSERT INTO '{}' VALUES (NULL, {})"
update_data = "UPDATE '{}' SET {} WHERE {}"
fetch_data_condition = "SELECT {} FROM {} WHERE {};"
fetch_data = "SELECT {} FROM '{}'"
delete_data = "DELETE FROM '{}' WHERE {}"
drop_table = "DROP TABLE '{}'"

APP_TITLE = "Keep - Suas notas. Encriptadas."
title = "Título"
content = "Conteúdo"
save = "Salvar"
cancel = "Cancelar"
delete = "Apagar"
notebook = "Bloco de notas"
readnote = "Notas"
newnote = "Nova nota"

