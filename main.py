from decimal import Decimal, getcontext
from tqdm import tqdm
from formule import *
from side_functions import *
from mpmath import mp
import time


if __name__ == "__main__":
    # Imposta la precisione desiderata
    prec = int(input("Inserisci la precisione delle cifre: "))
    getcontext().prec = prec
    global GLOBAL_PREC
    GLOBAL_PREC = prec
    getcontext().prec = GLOBAL_PREC

    # Dizionario delle funzioni disponibili
    funzioni_disponibili = {
        "ArctanTaylor": ArctanTaylor,
        "Archimede1": Archimede1,
        "Circonferenza": Circonferenza,
        "Archimede2": Archimede2,
        "Archimede": Archimede,
        "ArctanTaylor_parallel": ArctanTaylor_parallel,
        "chudnovsky": chudnovsky,
        "chudnovsky_parallel": chudnovsky_parallel,
        "MonteCarlo1": MonteCarlo1,
        "MonteCarlo2": MonteCarlo2,
        "Cerchio": Cerchio,
    }

    # Menu numerato
    print("Funzioni disponibili:")
    funzioni_list = list(funzioni_disponibili.keys())
    for idx, nome_funzione in enumerate(funzioni_list, 1):
        print(f"{idx}. {nome_funzione}")

    try:
        scelta_numero = int(input("Scegli il numero corrispondente alla formula da usare: "))
        if 1 <= scelta_numero <= len(funzioni_list):
            scelta = funzioni_disponibili[funzioni_list[scelta_numero - 1]]
        else:
            print("Scelta fuori intervallo.")
            exit()
    except ValueError:
        print("Input non valido. Inserisci un numero.")
        exit()



    # it is possible to load pi from a local file or with the built-in function mp
    #pi_true = load_pi_from_file("C:/Users/frabr/Documents/pi/rv_pi/pi.txt")

    if scelta.__name__ == "ArctanTaylor_parallel":
        pi_approx = scelta(prec)
    elif scelta.__name__ == "chudnovsky_parallel":
        pi_approx = scelta(prec)
    else:
        pi_approx = scelta()

    # it is possible to load pi from a local file or with the built-in function mp
    # pi_true = load_pi_from_file("C:/Users/frabr/Documents/pi/rv_pi/pi.txt")

    mp.dps = prec
    pi_true = mp.pi

    approx_str = str(pi_approx)
    true_str = str(pi_true)

    matching_digits = count_matching_digits(approx_str, true_str)

    print(f"\nValore approssimato di π ({scelta}): {approx_str[:10]}")
    print(f"Valore reale di π:                  {true_str[:10]}...")
    print(f"Cifre corrette: {matching_digits - 1}")