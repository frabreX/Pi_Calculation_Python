import time
from tqdm import tqdm
from decimal import Decimal, getcontext
from side_functions import  *
import multiprocessing as mp
from multiprocessing import Pool
import csv




def Archimede1():
    r = Decimal(1)
    n = int(input("Inserisci il numero di iterazioni quadrato inscritto: "))
    a = r * Decimal(2).sqrt()

    start_time = time.time()

    for i in tqdm(range(n)):
        a = ((r - (r ** 2 - (a / 2) ** 2).sqrt()) ** 2 + (a / 2) ** 2).sqrt()
    l = Decimal(2) ** (n + 2)
    circ = l * a
    pi_approx = circ / (2 * r)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} seconds")


    return pi_approx


def ArctanTaylor():
    n = int(input("Inserisci il numero di termini: "))
    sqrt3 = Decimal(3).sqrt()
    x = sqrt3 / Decimal(3)
    arctan_approx = 0

    start_time = time.time()

    for n in tqdm(range(n)):
        term = ((-1)**n * x**(2*n + 1)) / (2*n + 1)
        arctan_approx += term

    pi_approx = arctan_approx * Decimal(6)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} seconds")



    return pi_approx


def Circonferenza():

    step = Decimal(input("Inserisci lo step: "))

    r = Decimal(1)
    y0 = r
    x0 = Decimal(0)
    x = Decimal(0)
    quartocirc = Decimal(0)

    start_time = time.time()

    total_steps = int(r / step)
    pbar = tqdm(total=total_steps)

    while x < r:
        y = (Decimal(1) - x ** 2).sqrt()
        a = ((x - x0) ** 2 + (y - y0) ** 2).sqrt()

        x0 = x
        y0 = y
        quartocirc += a
        x += step
        pbar.update(1)

    pbar.close()


    pi_approx = quartocirc * 2 / r

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} seconds")

    return pi_approx

def Archimede2():

    r = Decimal(1)

    # Lato iniziale del esagono circoscritto

    a = r * Decimal(3).sqrt() * 2 / 3

    # Iterazioni richieste dall'utente
    n = int(input("Inserisci il numero di iterazioni esagono circoscritto: "))

    start_time = time.time()

    for i in tqdm(range(n)):

        a_half_sq = (a/2)**2

        a = 2 * (a_half_sq - ((a_half_sq + r ** 2).sqrt() - r)**2 ) / a

    l = 6 * (2 ** n)

    circ = a * l

    pi_approx = circ / (2 * r)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time:.6f} seconds")



    return pi_approx

def Archimede():

    pi_sup = Archimede1()
    pi_inf = Archimede2()

    # Converte entrambi i valori in stringa e confronta
    sup_str = str(pi_sup)
    inf_str = str(pi_inf)

    pi_true = load_pi_from_file("C:/Users/frabr/Documents/pi/rv_pi/pi.txt")
    true_str = str(pi_true)

    matching_digits_sup = count_matching_digits(sup_str, true_str)
    matching_digits_inf = count_matching_digits(inf_str, true_str)


    print(f"Cifre corrette: {matching_digits_sup - 1}")
    print(f"Cifre corrette: {matching_digits_inf - 1}")

    pi_approx = (pi_sup + pi_inf) / 2


    return pi_approx


def init_worker(prec):
    global GLOBAL_PREC
    GLOBAL_PREC = prec

def arctan_term(n_x):
    n, x = n_x
    getcontext().prec = GLOBAL_PREC
    x = Decimal(x)
    return Decimal((-1) ** n * x ** (2 * n + 1)) / Decimal(2 * n + 1)

def ArctanTaylor_parallel(prec):
    global GLOBAL_PREC
    GLOBAL_PREC = prec  # anche nel processo principale
    getcontext().prec = prec

    n_terms = int(input("Inserisci il numero di termini: "))
    sqrt3 = Decimal(3).sqrt()
    x = sqrt3 / Decimal(3)

    args = [(n, x) for n in range(n_terms)]

    start_time = time.time()

    with mp.Pool(processes=6, initializer=init_worker, initargs=(prec,)) as pool:
        terms = []
        for term in tqdm(pool.imap_unordered(arctan_term, args), total=n_terms):
            terms.append(term)

    arctan_approx = sum(terms)
    pi_approx = arctan_approx * Decimal(6)

    elapsed_time = time.time() - start_time
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")

    return pi_approx

def chudnovsky():
    n = int(input("Inserisci il numero di termini: "))



    def binary_split(a, b):
        if b == a + 1:
            Pab = -(6 * a - 5) * (2 * a - 1) * (6 * a - 1)
            Qab = 10939058860032000 * a ** 3
            Rab = Pab * (545140134 * a + 13591409)
        else:
            m = (a + b) // 2
            Pam, Qam, Ram = binary_split(a, m)
            Pmb, Qmb, Rmb = binary_split(m, b)

            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Rab = Qmb * Ram + Pam * Rmb


        pbar.update(1)
        return Pab, Qab, Rab

    def chudnovsky_inner(n):
        #progress bar per il calcolo
        global pbar
        pbar = tqdm(total=n, desc="Calcolo di Chudnovsky", unit="termine", ncols=100)

        P1n, Q1n, R1n = binary_split(1, n)
        pi_approx = (426880 * Decimal(10005).sqrt() * Q1n) / (13591409 * Q1n + R1n)

        pbar.close()  # Chiudiamo la progress bar quando il calcolo è terminato
        return pi_approx

    start_time = time.time()


    pi_approx = chudnovsky_inner(n)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} seconds")

    return pi_approx


def binary_split_range(args):
    a, b = args
    getcontext().prec = GLOBAL_PREC

    if b == a + 1:
        Pab = Decimal(-(Decimal(6) * Decimal(a) - Decimal(5)) * (Decimal(2) * Decimal(a) - Decimal(1)) * (Decimal(6) * Decimal(a) - Decimal((1))))
        Qab = Decimal(10939058860032000) * Decimal(a) ** 3
        Rab = Pab * (Decimal(545140134) * Decimal(a) + Decimal(13591409))
    else:
        m = (a + b) // 2
        Pam, Qam, Ram = binary_split_range((a, m))
        Pmb, Qmb, Rmb = binary_split_range((m, b))
        Pab = Decimal(Pam) * Decimal(Pmb)
        Qab = Decimal(Qam) * Decimal(Qmb)
        Rab = Decimal(Qmb) * Decimal(Ram) + Decimal(Pam) * Decimal(Rmb)

    return Decimal(Pab), Decimal(Qab), Decimal(Rab)


# Funzione combinatrice per unire i risultati
def combine_results(results):
    getcontext().prec = GLOBAL_PREC
    while len(results) > 1:
        new_results = []
        for i in range(0, len(results), 2):
            if i + 1 < len(results):
                P1, Q1, R1 = results[i]
                P2, Q2, R2 = results[i + 1]
                P = Decimal(P1) * Decimal(P2)
                Q = Decimal(Q1) * Decimal(Q2)
                R = Decimal(Q2) * Decimal(R1) + Decimal(P1) * Decimal(R2)
                new_results.append((P, Q, R))
            else:
                new_results.append(results[i])
        results = new_results
    return results[0]



def chudnovsky_parallel(prec):
    global GLOBAL_PREC
    n = int(input("Inserisci il numero di termini: "))
    GLOBAL_PREC = prec
    getcontext().prec = GLOBAL_PREC

    # Suddividiamo l'intervallo in 6 sottointervalli per 6 core
    num_processes = 6
    ranges = []
    step = n // num_processes
    for i in range(num_processes):
        a = i * step + 1
        b = (i + 1) * step + 1 if i < num_processes - 1 else n
        ranges.append((a, b))


    start_time = time.time()

    #with Pool(processes=num_processes, initializer=init_worker) as pool:
    with mp.Pool(processes=6, initializer=init_worker, initargs=(prec,)) as pool:
        results = list(
            tqdm(pool.imap(binary_split_range, ranges), total=len(ranges), desc="Calcolo in parallelo", ncols=100))
    P, Q, R = combine_results(results)

    pi_approx = (Decimal(426880) * Decimal(10005).sqrt() * Decimal(Q)) / (Decimal(13591409) * Decimal(Q) + Decimal(R))

    end_time = time.time()
    print(f"Elapsed Time: {end_time - start_time:.2f} seconds")
    return pi_approx

















def MonteCarlo1():
    rr = int(input("Inserisci il raggio: "))

    points_in = 0
    r = Decimal(rr)

    for x in range(rr):
        x = Decimal(x)
        ymax = (r ** 2 - x ** 2).sqrt()
        points_in += int(ymax)  # numero di y interi sotto la curva

    total_points = r * r  # punti totali nel quadrante

    pi_approx = Decimal(points_in) / Decimal(total_points) * Decimal(4)
    return pi_approx





def MonteCarlo2():
    r = int(input("Inserisci il raggio: "))

    points_in = 0
    r_squared = Decimal(r) ** 2

    for x in tqdm(range(-r, r)):
        x_dec = Decimal(x)
        for y in range(-r, r):
            y_dec = Decimal(y)
            if x_dec ** 2 + y_dec ** 2 < r_squared:
                points_in += 1

    total_points = (2 * r) ** 2
    pi_approx = Decimal(points_in) / Decimal(total_points) * Decimal(4)
    return pi_approx



def Cerchio():
    step = Decimal(input("Inserisci lo step: "))
    r = Decimal(1)
    x = -r
    area_totale = Decimal(0)

    total_steps = int(r / step)
    pbar = tqdm(total=total_steps)

    while x < Decimal(1):
        y = (r ** 2 - x**2).sqrt()
        base = step * Decimal(2)
        area = base * y
        area_totale += area
        x += base
        pbar.update(1)

    pbar.close()
    pi_approx = area_totale * 2
    return pi_approx







