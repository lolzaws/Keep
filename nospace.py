"""
Programa que le um arquivo e converte tabs em espaços.

Utilizado para corrigir o erro de tabs e espaços coexistindo na identação.
"""
input_file = "app.py"
output_file = "output.py"

out = open(output_file, 'w')

with open(input_file, "r") as fil:
   for line in fil:
      # se existe tabs, transforma em espaços
      if "\t" in line:
          line = line.replace("\t", "    ")
      out.write(line)

out.close()