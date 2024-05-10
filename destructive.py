import sys

# Sostituisci 'vecchia_stringa' con la stringa fornita come argomento da linea di comando nel file 'nome_file.txt'

# Controlla se l'argomento è stato fornito
if len(sys.argv) != 2:
    print("Uso: python script.py nuova_stringa")
    sys.exit(1)

# Definisci la stringa da cercare
vecchia_stringa = "your_secret_token"
nuova_stringa = sys.argv[1]  # Prende la nuova stringa dall'argomento da linea di comando

# Apri il file in modalità lettura e leggi il contenuto
with open('/ctf/DestructiveFarm/server/config.py', 'r') as file:
    file_contents = file.read()

# Sostituisci la vecchia stringa con la nuova
file_contents = file_contents.replace(vecchia_stringa, nuova_stringa)

# Apri il file in modalità scrittura e sovrascrivi il contenuto modificato
with open('/ctf/DestructiveFarm/server/config.py', 'w') as file:
    file.write(file_contents)

print("Sostituzione completata.")
