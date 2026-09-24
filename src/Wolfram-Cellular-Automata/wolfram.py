import numpy as np
import matplotlib.pyplot as plt

def run_cellular_automaton(rule_number, steps=200, width=201, initial_state="single"):
    """
    rule_number: int tra 0 e 255 (es. 40, 56, 18, 30, 110)
    steps: numero di passi temporali (righe)
    width: larghezza della griglia spaziale (colonne)
    initial_state: "single" (un solo 1 al centro) o "random" (configurazione casuale)
    """
    # Converte il numero della regola in un array binario di 8 elementi
    # Es. Regola 30 -> 00011110_2

    # convertire la regola di Wolfram in un np array per poi settare la regola
    
    
    # represents the number rule in binary: 30 -> 0001 1110
    rule_bits = np.array([int(b) for b in np.binary_repr(rule_number, width=8)], dtype=int)
    
    # Inizializza la griglia spazio-temporale (steps x width)
    grid = np.zeros((steps, width), dtype=int)
    
    # Imposta la condizione iniziale (prima riga)
    if initial_state == "single":
        # riga zero e colonna modulo 2 va a 1
        grid[0, width // 2] = 1
    elif initial_state == "random":
        # prima riga facciamo random choice
        grid[0] = np.random.choice([0, 1], size=width)
    else:
        raise ValueError("initial_state deve essere 'single' o 'random'")
        
    # Evoluzione temporale
    for t in range(steps - 1):
        # Condizioni periodiche usando np.roll (scorrimento circolare)
        # np.roll prende l'array e lo sposta di tot posizioni in modo circolare
        # utile per selezionare gli elementi vicini

        # sono tutti vettori! si usa numpy col calcolo vettoriale

        left = np.roll(grid[t], 1)    # s_{i-1}
        center = grid[t]              # s_i
        right = np.roll(grid[t], -1)  # s_{i+1}
        
        # Converte la terzina binaria nel corrispondente indice decimale (da 0 a 7)
        # viene fatto PER OGNI CELLA
        pattern_indices = 7 - (4 * left + 2 * center + right)
        
        # Applica la regola di transizione
        # pattern indices è il numero associato alla tripletta, da 0 a 7,
        # fancy indecing, è un pò crazy.... no sense
        # rule_bits ha 8 elementi, pattern indices ne ha tanti quante sono le celle in orizzontale
        # dentro patter_indices ci sono numeri da 0 a 7, viene associato ad ogni elemento della regola il rispettivo indice
        # e viene aggiornata la griglia in questo modo
        grid[t + 1] = rule_bits[pattern_indices]
        
    return grid

# --- Esempio di utilizzo e plotting ---

regola = 110  # Puoi provare: 40 (Classe 1), 56 (Classe 2), 18 o 30 (Classe 3), 110 (Classe 4)
griglia = run_cellular_automaton(rule_number=regola, steps=200, width=400, initial_state="random")

plt.figure(figsize=(10, 7), dpi=150)
plt.imshow(griglia, cmap="binary", interpolation="nearest")
plt.title(f"Automa Cellulare di Wolfram - Regola {regola}", fontsize=14)
plt.xlabel("Spazio (Celle)")
plt.ylabel("Tempo (Passi)")
plt.savefig("automa_wolfram_classe4.png", dpi=300, bbox_inches="tight")
print("Immagine salvata con successo come automa_wolfram_110.png")