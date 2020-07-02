# Grupa: 231   Nume: Cirstea Natasa Alexandra
import copy
import time
from math import sqrt


class Configuratie:
    def __init__(self, info):
        # info -> pozitie start(x,y), cizme (culoare, purtari), in desaga (culoare, purtari), cu/fara piatra(1/0), afisare
        # info[0] = x, info[1] = y | info[2] = culoare, info[3] = purtari | info[4] = culoare, info[5] = purtari | info[6] = cu/fara piatra | info[7] = afisare
        self.info = info
        self.h = self.number_to_euristica(
            Stare.date_problema.numar_euristica_folosita)

    def get_e1(self):
        return self.euristica_1()

    def get_e2(self):
        return self.euristica_2()

    def get_e3(self):
        return self.euristica_3()

    def number_to_euristica(self, euristica):
        switcher = {
            1: self.get_e1,
            2: self.get_e2,
            3: self.get_e3
        }
        # Get the function from switcher dictionary
        func = switcher.get(euristica, lambda: 1)
        # Execute the function
        return func()

    def euristica_1(self):
        '''
        Cum tabla este impartita in parcele/patratele de dimensiuni egale, putem folosi distanta Manhattan.
        Aceasta ofera cel mai scurt drum de la o coordonata (x_start, y_start) la o coordonata (x_final, y_final).
        Cum cel mai eficient drum pe care il poate urma vrajitorul este cel mai scurt drum de la o pozitie de start la o pozitie finala
        (vrajitorul poate fi nevoit sa urmeze un drum in care exista mai multe ocoliri pentru a lua una sau mai multe perechi de cizme necesare pe viitor), 
        distanta Manhattan nu va supraestima niciodata valoarea efectiva h, deci euristica este admisibila.
        '''
        h = 0

        # calculam distanta Manhattan fata de stop/start
        if self.info[6] == 0:
            # daca nu am gasit piatra, adaugam la distanta Manhattan fata de piatra si distanta Manhattan fata de iesire
            x_piatra = Stare.date_problema.pozitie_piatra[0]
            y_piatra = Stare.date_problema.pozitie_piatra[1]

            x_stop = Stare.date_problema.pozitie_start[0]
            y_stop = Stare.date_problema.pozitie_start[1]

            # distanta pana la piatra
            h = abs(x_piatra - self.info[0]) + abs(y_piatra - self.info[1])
            # distanta de la piatra la iesire
            h += abs(x_piatra - x_stop) + abs(y_piatra - y_stop)
        else:
            # daca am gasit piatra, calculam distanta Manhattan fata de iesire
            x_stop = Stare.date_problema.pozitie_start[0]
            y_stop = Stare.date_problema.pozitie_start[1]

            # distanta pana la iesire
            h = abs(self.info[0] - x_stop) + abs(self.info[1] - y_stop)
        return h

    def euristica_2(self):
        '''
        Pentru aceasta euristica vom folosi distanta de la un punct de start (x_start, y_start) la un punct destinatie (x_final, y_final).
        Cum cel mai eficient drum pe care il poate urma vrajitorul este cel mai scurt drum de la o pozitie de start la o pozitie finala
        si luand in calcul miscarea pe diagonale, mai eficienta decat miscarea in stilul distantelor Manhattan,
        (vrajitorul poate fi nevoit sa urmeze un drum in care exista mai multe ocoliri pentru a lua una sau mai multe perechi de cizme necesare pe viitor), 
        distanta astfel calculata nu va supraestima niciodata valoarea efectiva h, deci euristica este admisibila.
        '''
        h = 0

        # calculam distanta Manhattan fata de stop/start
        if self.info[6] == 0:
            # daca nu am gasit piatra, adaugam la distanta fata de piatra si distanta fata de iesire
            x_piatra = Stare.date_problema.pozitie_piatra[0]
            y_piatra = Stare.date_problema.pozitie_piatra[1]

            x_stop = Stare.date_problema.pozitie_start[0]
            y_stop = Stare.date_problema.pozitie_start[1]

            # distanta pana la piatra
            c1 = abs(x_piatra - self.info[0])
            c2 = abs(y_piatra - self.info[1])
            h = sqrt(c1 * c1 + c2 * c2)

            # distanta de la piatra la iesire
            c1 = abs(x_piatra - x_stop)
            c2 = abs(y_piatra - y_stop)
            h += sqrt(c1 * c1 + c2 * c2)
        else:
            # daca am gasit piatra, calculam distanta fata de iesire
            x_stop = Stare.date_problema.pozitie_start[0]
            y_stop = Stare.date_problema.pozitie_start[1]

            c1 = abs(x_stop - self.info[0])
            c2 = abs(y_stop - self.info[1])

            # distanta pana la iesire
            h = sqrt(c1 * c1 + c2 * c2)
        return h

    def euristica_3(self):
        '''
        Pentru aceasta euristica vom folosi drept distanta aria patrulaterului dat de punctul de start (x_start, y_start) si punctul destinatie (x_final, y_final).
        Cel mai scurt drum de la o coordonata (x_start, y_start) la o coordonata (x_final, y_final), in conditiile problemei noastre, este oferita de distanta Manhattan.
        Pentru o configuratie ca cea din fisieul 'input4.txt', se evidentiaza doua drumuri: 
          1. (cel mai eficient) in care trebuie sa ne indepartam de piatra ca apoi sa ne aproipiem treptat
          2. (mai putin eficient) in care intai ne apropiem de piatra dupa care oscileaza apropierile si departarile 
             (departari care au insa arii mult mai mici decat aria data de prima departare a drumului 1)
        In acest caz, algoritmul va alege initial drumul 2 si va continua pe acesta intrucat valoarea f a drumului 1 obtinuta dupa un pas
        va fi mai mare decat valorile f ale drumului 2 obtinute in pasii intermediari.
        In acest caz, euristica va supraestima valoarea efectiva h, deci nu este admisibila.
        Euristica va supraestima valoarea efectiva h ori de cate ori drumul nu va urma in intregime dreptunghiul pentru care se face aria.
        '''
        h = 0

        if self.info[6] == 0:
            # daca nu am gasit piatra, adaugam la distanta fata de piatra si distanta fata de iesire
            x_piatra = Stare.date_problema.pozitie_piatra[0]
            y_piatra = Stare.date_problema.pozitie_piatra[1]

            x_stop = Stare.date_problema.pozitie_start[0]
            y_stop = Stare.date_problema.pozitie_start[1]

            # distanta pana la piatra
            l1 = abs(x_piatra - self.info[0]) + 1
            l2 = abs(y_piatra - self.info[1]) + 1
            h = l1 * l2

            # distanta de la piatra la iesire
            l1 = abs(x_piatra - x_stop) + 1
            l2 = abs(y_piatra - y_stop) + 1
            h += l1 * l2
        else:
            # daca am gasit piatra, calculam distanta fata de iesire
            x_stop = Stare.date_problema.pozitie_start[0]
            y_stop = Stare.date_problema.pozitie_start[1]

            l1 = abs(x_stop - self.info[0]) + 1
            l2 = abs(y_stop - self.info[1]) + 1

            # distanta pana la iesire
            h = l1 * l2
        return h

    def __str__(self):
        return f"({self.info[0]}, {self.info[1]}, {self.info[2]}, {self.info[3]}, {self.info[4]}, {self.info[5]}, {self.info[6]})"

    def __repr__(self):
        return f"({self.info[0]}, {self.info[1]}, {self.info[2]}, {self.info[3]}, {self.info[4]}, {self.info[5]}, {self.info[6]})"


class Problema:
    def __init__(self, linii, coloane, matrice_culori, matrice_obiecte, numar_euristica):
        self.linii = linii
        self.coloane = coloane
        self.matrice_culori = matrice_culori
        self.matrice_obiecte = matrice_obiecte
        self.simbol_piatra = '@'
        self.simbol_start = '*'
        self.simbol_gol = '0'
        self.directii = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.numar_euristica_folosita = numar_euristica

        gasit_unul = False
        for i in range(linii):
            for j in range(coloane):
                if matrice_obiecte[i][j] == self.simbol_start:
                    # pozitie start/final(x,y)
                    self.pozitie_start = (i, j)
                    if gasit_unul:
                        break
                    else:
                        gasit_unul = True
                if matrice_obiecte[i][j] == self.simbol_piatra:
                    # pozitie piatra(x,y)
                    self.pozitie_piatra = (i, j)
                    if gasit_unul:
                        break
                    else:
                        gasit_unul = True


# O clasa care cuprinde informatiile asociate unei stari din listele opened/closed
class Stare:
    date_problema = None

    def __init__(self, configuratie, parinte=None, g=0, f=None):
        self.configuratie = configuratie
        self.parinte = parinte
        self.g = g
        if f is None:
            self.f = self.g + self.configuratie.h
        else:
            self.f = f

    def drum_miscari(self):
        # Functie care calculeaza drumul asociat unei stari din arborele de cautare.
        # Functia merge din parinte in parinte pana ajunge la configuratia starii de start
        stare = self
        nr_pasi = 0
        ordine = [stare]
        while stare.parinte is not None:
            ordine = [stare.parinte] + ordine
            nr_pasi += 1
            stare = stare.parinte
        return [nr_pasi, ordine]

    # compara tuplul info[0] = x, info[1] = y | info[2] = culoare, info[3] = purtari | info[4] = culoare, info[5] = purtari | info[6] = cu/fara piatra | info[7] = afisare
    # al starii curente cu tuplul unei alte stari
    def configuratiiEgale(self, tuplu_de_comparat):
        tuplu_curent = self.configuratie.info
        if tuplu_curent[0] == tuplu_de_comparat[0] and tuplu_curent[1] == tuplu_de_comparat[1] and tuplu_curent[2] == tuplu_de_comparat[2] and \
           tuplu_curent[3] == tuplu_de_comparat[3] and tuplu_curent[4] == tuplu_de_comparat[4] and tuplu_curent[5] == tuplu_de_comparat[5] and \
           tuplu_curent[6] == tuplu_de_comparat[6]:
            return True
        return False

    def contine_in_drum(self, configuratie):
        # verifica daca "configuratie" se afla in drumul dintre configuratia de start si configuratia curenta (self)
        # self -> Stare, configuratie -> Configuratie
        stare_curenta = self
        while stare_curenta.parinte is not None:
            if stare_curenta.configuratiiEgale(configuratie.info):
                return True
            stare_curenta = stare_curenta.parinte
        return False

    def expandeaza(self):
        # functia creeaza o lista de succesori de tip Configuratie
        # alegand toate combinatiile valide pentru tupluri

        # info[0] = x, info[1] = y | info[2] = culoare, info[3] = purtari | info[4] = culoare, info[5] = purtari | info[6] = cu/fara piatra | info[7] = afisare
        l_succesori = []
        tocit = ""

        # ne asiguram ca, in orice moment, vrajitorul nu are cizme tocite in picioare sau in desaga
        # daca cizmele sunt tocite, le arunca si le incalta pe cele din desaga. config reprezinta configuratia curenta
        if self.configuratie.info[3] == 3:
            aux = copy.deepcopy(self.configuratie.info)
            config = (aux[0], aux[1], aux[4], aux[5], '-', 0, aux[6], aux[7])
            tocit += f"I s-au tocit cizmele {self.configuratie.info[2]}. Schimba cizmele din picioare cu cele din desaga. "
        else:
            config = copy.deepcopy(self.configuratie.info)

        # stabilim directiile in care poate merge vrajitorul, precum si pozitia curenta
        directii = self.date_problema.directii
        x_curent = self.configuratie.info[0]
        y_curent = self.configuratie.info[1]

        for i in range(len(directii)):
            # (x, y) = (pozitia in care urmeaza sa mergem)
            x = x_curent + directii[i][0]
            y = y_curent + directii[i][1]

            # pozitia nou obtinuta trebuie sa se afle in pestera (dreptunghi)
            if 0 <= x and x < self.date_problema.linii and 0 <= y and y < self.date_problema.coloane:
                text = tocit
                text2 = tocit

                piatra = 0
                # daca piatra se afla in pozitia curenta sau stim ca am luat piatra, marcam piatra ca fiind luata
                if self.date_problema.matrice_obiecte[x_curent][y_curent] == self.date_problema.simbol_piatra or config[6] == 1:
                    piatra = 1

                if self.date_problema.matrice_obiecte[x_curent][y_curent] == self.date_problema.simbol_piatra:
                    text += "Ia piatra. "
                    text2 += "Ia piatra. "

                # daca in pozitia curenta avem o pereche de cizme
                if self.date_problema.matrice_obiecte[x_curent][y_curent] not in [self.date_problema.simbol_piatra, self.date_problema.simbol_start, self.date_problema.simbol_gol]:
                    culoare_cizme_schimb = self.date_problema.matrice_obiecte[x_curent][y_curent]
                    text += f"A gasit cizme de culoare {culoare_cizme_schimb}. "

                    # cand culoarea cizmelor gasite se potriveste cu culoarea patratelului in care va merge vrajitorul,
                    # are optiunea de a schimba cizmele din picioare cu cizmele gasite
                    if self.date_problema.matrice_culori[x][y] == culoare_cizme_schimb:
                        # daca cizmele din desaga difera de cizmele din picioare prin culoare sau prin purtari
                        # schimb cizmele din picioare si le pastrez pe cele din picioare in desaga
                        if config[2] != config[4] or config[5] == '-' or config[3] >= config[5]:
                            text_auxiliar = text + \
                                "Pune cizmele din picioare in desaga, incalta cizmele din patratel si porneste la drum. "
                            info = (x, y, culoare_cizme_schimb, 1,
                                    config[2], config[3], piatra, text_auxiliar)
                            succesor = Configuratie(info)
                            l_succesori.append(succesor)

                        # schimb cizmele din picioare cu cele din patratel si le arunc pe cele pe care le aveam in picioare
                        text_auxiliar = text + \
                            "Schimba cizmele din picioare cu cele din patratel si porneste la drum. "
                        # schimb cizmele din picioare si le arunc pe cele din picioare
                        info = (x, y, culoare_cizme_schimb, 1,
                                config[4], config[5], piatra, text_auxiliar)
                        succesor = Configuratie(info)
                        l_succesori.append(succesor)

                    # cand culoarea cizmelor din picioare se potriveste cu culoarea patratelului in care va merge vrajitorul,
                    # are optiunea de a schimba cizmele din desaga cu cizmele gasite
                    if self.date_problema.matrice_culori[x][y] == config[2]:
                        # pastrez cizmele pe care le am in picioare si, daca in desaga nu am aceleasi cizme cu aceleasi purtari, le schimb
                        if config[4] != culoare_cizme_schimb or (config[4] == culoare_cizme_schimb and config[5] != 0):
                            text_auxiliar = text + "Pune cizmele din patratel in desaga si porneste la drum. "
                            info = (x, y, config[2], config[3] + 1,
                                    culoare_cizme_schimb, 0, piatra, text_auxiliar)
                            succesor = Configuratie(info)
                            l_succesori.append(succesor)

                    # cand culoarea cizmelor din desaga se potriveste cu culoarea patratelului in care va merge vrajitorul,
                    # are optiunea de a schimba cizmele din picioare cu cele din desaga si de a pune cizmele gasite in desaga
                    if self.date_problema.matrice_culori[x][y] == config[4]:
                        # incaltam cizmele din desaga si le punem in desaga pe cele de schimb
                        text_auxiliar = text + \
                            "Incalta cizmele din desaga, pune cizmele din patratel in desaga si porneste la drum. "
                        info = (x, y, config[4], config[5] + 1,
                                culoare_cizme_schimb, 0, piatra, text_auxiliar)
                        succesor = Configuratie(info)
                        l_succesori.append(succesor)

                # cu sau fara cizme de schimb
                # cand culoarea cizmelor din picioare se potriveste cu culoarea patratelului in care va merge vrajitorul,
                # continua sa mearga cu cizmele din picioare
                if self.date_problema.matrice_culori[x][y] == config[2]:
                    info = (x, y, config[2], config[3] + 1,
                            config[4], config[5], piatra, text2)
                    succesor = Configuratie(info)
                    l_succesori.append(succesor)

                # cand culoarea cizmelor din desaga se potriveste cu culoarea patratelului in care va merge vrajitorul,
                # va schimba cizmele din picioare cu cele din desaga si le va pune pe cele din picioare in desaga
                if self.date_problema.matrice_culori[x][y] == config[4]:
                    text_auxiliar = text2 + \
                        "Incalta cizmele din desaga, pune cizmele din picioare in desaga si porneste la drum. "
                    info = (x, y, config[4], config[5] + 1,
                            config[2], config[3], piatra, text_auxiliar)
                    succesor = Configuratie(info)
                    l_succesori.append(succesor)

        return l_succesori

    def test_scop(self):
        if self.configuratie.info[0] == Stare.date_problema.pozitie_start[0] and self.configuratie.info[1] == Stare.date_problema.pozitie_start[1] and self.configuratie.info[6] == 1:
            return True
        return False

    def __str__(self):
        info = self.parinte if self.parinte is None else self.parinte.configuratie.info
        parinte = ""
        if info is not None:
            parinte = f"({info[0]}, {info[1]}, {info[2]}, {info[3]}, {info[4]}, {info[5]}, {info[6]})"
        else:
            parinte = "None"
        return f"( {self.configuratie}, " + '{0: <32}'.format(f"parinte = {parinte},") + '{0: <11}'.format(f" f = {self.f:.2f},") + '{0: <8}'.format(f" g = {self.g},") + '{0: <7}'.format(f" h = {self.configuratie.h:.2f}") + ")"


# """ Algoritmul A* """


def str_info_configuratii(lista_stari):
    sir = "\n[\n"
    for x in lista_stari:
        sir += "    " + str(x) + "  \n"
    sir += "]\n"
    return sir


def str_info_poveste(lista_stari):
    sir = "\n"
    for index in range(len(lista_stari)):
        stramos = lista_stari[index -
                              1].configuratie.info if index - 1 >= 0 else None
        info = lista_stari[index].configuratie.info

        sir += '{0: <9}'.format(f"\nPas {index}: ")
        sir += info[7]

        if stramos is not None:
            sir += f"Paseste din ({stramos[0]},{stramos[1]}) in ({info[0]},{info[1]})."
        else:
            sir += f"Incepe drumul cu cizme de culoare {info[2]} din ({info[0]},{info[1]})."

        sir += f" Incaltat: {info[2]} (purtari: {info[3]}). Desaga: "
        if info[4] != '-':
            sir += f"{info[4]} (purtari: {info[5]})."
        else:
            sir += "nimic."

        if info[6] == 1:
            sir += f" Cu piatra."
        else:
            sir += " Fara piatra."

        sir += "\n"

    sir += "\nA iesit din pestera. \n"

    return sir


def in_lista(lista_stari, configuratie):
    # lista_stari -> obiecte de tip Stare, configuratie -> Configuratie
    for i in range(len(lista_stari)):
        if lista_stari[i].configuratiiEgale(configuratie.info):
            return lista_stari[i]
    return None


def a_star(nume_fisier_iesire):
    x = Stare.date_problema.pozitie_start[0]
    y = Stare.date_problema.pozitie_start[1]
    culoare = Stare.date_problema.matrice_culori[x][y]
    conf = Configuratie((x, y, culoare, 1, '-', 0, 0, ""))

    stare_start = Stare(conf)
    # opened va contine elemente de tip Stare
    opened = [stare_start]
    closed = []                       # closed va contine elemente de tip Stare

    while len(opened) > 0:
        ''' 
        Putem afisa lista open pentru a vedea ce pasi au fost facuti
        print(str_info_configuratii(opened)) 
        '''

        # scoatem primul element din lista opened
        stare_curenta = opened.pop(0)
        # si il adaugam la finalul listei closed
        closed.append(stare_curenta)

        if stare_curenta.test_scop():  # cand starea curenta este egala cu starea scop, ne oprim
            break

        # lista succesorilor contine elemente de tip Configuratie
        l_succesori = stare_curenta.expandeaza()

        for config_succesor in l_succesori:
            # (tata): stare_curenta   -> Stare,
            # (fiu) : config_succesor -> Configuratie

            # nu se creeaza un circuit, fiul nu e in drumul start-tata
            if (not stare_curenta.contine_in_drum(config_succesor)):

                # g-ul tatalui + [cost miscare(tata, fiu) = 1]
                g_succesor = stare_curenta.g + 1
                f_succesor = g_succesor + config_succesor.h  # g-ul fiului + h-ul fiului

                # verific daca "config_succesor" se afla in closed
                stare_veche = in_lista(closed, config_succesor)
                stare_noua = None

                # config_succesor se afla in closed
                if stare_veche is not None:
                    # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                    #       f-ul pentru drumul gasit anterior (f-ul starii aflate in lista closed)
                    # atunci actualizez parintele, g si f, si apoi adaug "stare_noua" in lista opened

                    if (f_succesor < stare_veche.f):
                        # scot configuratia din lista closed
                        closed.remove(stare_veche)
                        stare_veche.parinte = stare_curenta  # actualizez parintele
                        stare_veche.g = g_succesor                  # actualizez g
                        stare_veche.f = f_succesor                  # actualizez f
                        # setez "stare_noua", care va fi adaugat apoi in opened
                        stare_noua = stare_veche

                else:
                    # verific daca "config_succesor" se afla in opened
                    stare_veche = in_lista(opened, config_succesor)

                    # config_succesor se afla in opened
                    if stare_veche is not None:
                        # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                        #       f-ul pentru drumul gasit anterior (f-ul starii aflate in lista opened)
                        # atunci scot nodul din lista opened (pentru ca modificarea valorilor f si g imi va strica sortarea listei opened)
                        #       actualizez parintele, g si f, si apoi adaug "stare_noua" in lista opened (la noua pozitie corecta in sortare)

                        if (f_succesor < stare_veche.f):
                            opened.remove(stare_veche)
                            stare_veche.parinte = stare_curenta
                            stare_veche.g = g_succesor
                            stare_veche.f = f_succesor
                            stare_noua = stare_veche

                    else:  # cand "config_succesor" nu e nici in closed, nici in opened
                        stare_noua = Stare(
                            configuratie=config_succesor, parinte=stare_curenta, g=g_succesor, f=f_succesor)
                        # se calculeaza f automat in constructor

                if stare_noua is not None:
                    # inserare in lista sortata crescator dupa f (si pentru f-uri egale descrescator dupa g)
                    i = 0
                    while i < len(opened):
                        if opened[i].f < stare_noua.f:
                            i += 1
                        else:
                            while i < len(opened) and opened[i].f == stare_noua.f and opened[i].g > stare_noua.g:
                                i += 1
                            break

                    opened.insert(i, stare_noua)

    g = open(nume_fisier_iesire, 'w')
    # print("\n--------------------------------------------- Concluzie --------------------------------------------\n")
    if len(opened) == 0:
        # print(
        #     "Lista opened e vida, nu avem drum de la configuratia start la configuratia scop")

        g.write(
            "Lista opened e vida, nu avem drum de la configuratia start la configuratia scop")

    else:
        drum = (stare_curenta.drum_miscari())
        # print(f"Drum de cost minim in {drum[0]} pasi: " +
        #       str_info_configuratii(drum[1]))

        # print(f"\n\nDrum de cost minim in {drum[0]} pasi: " +
        #       str_info_poveste(drum[1]))

        g.write(f"Drum de cost minim in {drum[0]} pasi: " +
                str_info_configuratii(drum[1]))
        g.write(f"\n\nDrum de cost minim in {drum[0]} pasi: " +
                str_info_poveste(drum[1]))
    g.close()


if __name__ == "__main__":
    # Luam euristica de la consola pentru a nu fi nevoiti sa modificam toate cele 3 fisiere de intrare
    raspuns_valid = False
    # by default, euristica este 1
    euristica = 1
    while not raspuns_valid:
        n = input(
            "\nExista 3 euristici disponibile: 1, 2 sunt admisibile, iar 3 nu este admisibila.\nAlegeti euristica dorita: ")
        if n.isdigit():
            euristica = int(n)
            if 1 <= euristica and euristica <= 3:
                raspuns_valid = True
            else:
                print("\nTrebuie sa introduceti un numar cuprins intre 1 si 3.")
        else:
            print("\nTrebuie sa introduceti un numar cuprins intre 1 si 3.")

    print(
        f"\nTimpul pentru euristica {euristica}:")

    # Cum toate fisierele sunt de forma 'inputX.txt' sau 'outputX.txt', am creat numele fiserului in for si nu am mai folosit o lista pentru a le stoca, eficientizand astfel folosirea memoriei
    for index in range(1, 5):
        nume_fisier_intrare = 'vrajitor_input' + \
            str(index) + '.txt'
        nume_fisier_iesire = 'vrajitor_output' + \
            str(index) + '.txt'

        f = open(nume_fisier_intrare, 'r')

        matrice_culori = []
        matrice_obiecte = []

        # Pentru fiecare dintre cele 3 fisiere de intrare citim datele si le salvam corespunzator
        if f.mode == 'r':
            lines = f.readlines()

            info = lines[0].split()
            linii, coloane = int(info[0]), int(info[1])

            for index in range(2, 2 + linii):
                aux = []
                info = lines[index].split()
                for elem in info:
                    aux.append(elem)
                matrice_culori.append(aux)

            for index in range(2 + linii + 1, 2 + linii + 1 + linii):
                aux = []
                info = lines[index].split()
                for elem in info:
                    aux.append(elem)
                matrice_obiecte.append(aux)

        f.close()

        # stabilim datele problemei si apelam algoritmul a*
        problema_vrajitor = Problema(
            linii, coloane, matrice_culori, matrice_obiecte, euristica)
        Stare.date_problema = problema_vrajitor

        # preiau timpul in milisecunde inainte de mutare
        t_inainte = int(round(time.time() * 1000))

        a_star(nume_fisier_iesire)

        # preiau timpul in milisecunde de dupa mutare
        t_dupa = int(round(time.time() * 1000))

        print(
            f"{nume_fisier_intrare}: {str(t_dupa-t_inainte)} milisecunde.")

'''
OBSERVATII:

FISIERE I/O

1. Nu se poate construi un fisier de intrare care da o stare initiala care este si finala,
   intrucat nu putem plasa atat intrarea, cat si piatra pe aceeasi placuta 
   (locul de pornire marcat cu un caracter * si locul unde se gaseste piatra marcat cu un @ nu pot fi unul si acelasi)

2. Fisierele I/O au umatoarea structura:
   1. fisier de input care nu are solutii
   2. fisier de input cu un drum de cost minim de lungime 3-5
   3. fisier de input cu un drum de cost minim de lungime mai mare decat 5 care contine chiar exemplul dat pentru problema in laborator
   4. fisier de input cu un drum de cost minim de lungime mai mare decat 5 pentru care algoritmul A* da 
      drumul de cost minim pentru euristicile admisibile si un drum care nu e de cost minim pentru acea euristica neadmisibila

EURISTICI

1.  ADMISIBILITATE:
    Cum tabla este impartita in parcele/patratele de dimensiuni egale, putem folosi distanta Manhattan.
    Aceasta ofera cel mai scurt drum de la o coordonata (x_start, y_start) la o coordonata (s_final, y_final).
    Cum cel mai eficient drum pe care il poate urma vrajitorul este cel mai scurt drum de la o pozitie de start la o pozitie finala
    (vrajitorul poate fi nevoit sa urmeze un drum in care exista mai multe ocoliri pentru a lua una sau mai multe perechi de cizme necesare pe viitor), 
    distanta Manhattan nu va supraestima niciodata valoarea efectiva h, deci euristica este admisibila.

    CONSISTENTA:
    h(tata) <= cost_muchie(tata, fiu) + h(fiu)
    cost_muchie(tata, fiu) = 1 (consideram ca fiecare pas efectuat are un cost de 1 unitate)
    Cum calculam h-ul folosind distanta Manhattan si costul unui pas ca fiind de 1 unitate, iar vrajitorul efectueaza cate un pas odata,
    avem ca h(fiu) creste sau descreste cu o unitate fata de h(tata). 
    Daca h(fiu) creste, conditia este indeplinita.
    Daca h(fiu) scade, avem h(fiu) = h(tata) - 1 <=> h(tata) = 1 + h(fiu), deci conditia este respectata.
    Euristica este, prin urmare, consistenta.     

2.  ADMISIBILITATE:
    Pentru aceasta euristiva vom folosi distanta de la un punct de start (x_start, y_start) la un punct destinatie (x_final, y_final).
    Cum cel mai eficient drum pe care il poate urma vrajitorul este cel mai scurt drum de la o pozitie de start la o pozitie finala
    si luand in calcul miscarea pe diagonale, mai eficienta/scurta decat miscarea in stilul distantelor Manhattan,
    (vrajitorul poate fi nevoit sa urmeze un drum in care exista mai multe ocoliri pentru a lua una sau mai multe perechi de cizme necesare pe viitor), 
    distanta astfel calculata nu va supraestima niciodata valoarea efectiva h, deci euristica este admisibila.

    CONSISTENTA:
    h(tata) <= cost_muchie(tata, fiu) + h(fiu)
    cost_muchie(tata, fiu) = 1 (consideram ca fiecare pas efectuat are un cost de 1 unitate)
    Calculam h-ul folosind distanta directa(diagonala), adica radical(cateta_1^2 + cateta_2^2), unde cateta_1 = distanta de la (x_1, y_1) la (x_2, y_2).
    Considerand costul unui pas ca fiind de 1 unitate si ca vrajitorul efectueaza cate un pas odata, 
    avem ca la fiecare miscare (cateta_1 creste sau descreste cu o unitate) sau (cateta_2 creste sau descreste cu o unitate)
    Daca una dintre catete scade, conditia este indeplinita.
    Daca una dintre catete creste, trebuie sa verificam relatia:
    [radical((c1-1)^2 + (c2)^2)) <= 1 + radical((c1)^2 + (c2)^2)] sau relatia [radical((c1)^2 + (c2-1)^2)) <= 1 + radical((c1)^2 + (c2)^2)]
    Cum ambele se rezolva analog, o vom dezvolta pe prima. Prin ridicare la patrat si simplificare obtinem: 2*c1 <= 2*radical((c1)^2 + (c2)^2)
    Ridicand inca o data la patrat si simplificand, obtinem: 0 <= c2^2, evident adevarat, deci conditia este respectata.
    Euristica este, prin urmare, consistenta.  

3.  ADMISIBILITATE:
    Pentru aceasta euristica vom folosi drept distanta aria patrulaterului dat de punctul de start (x_start, y_start) si punctul destinatie (x_final, y_final).
    Cel mai scurt drum de la o coordonata (x_start, y_start) la o coordonata (x_final, y_final), in conditiile problemei noastre, este oferita de distanta Manhattan.
    Pentru o configuratie ca cea din fisieul 'input4.txt', se evidentiaza doua drumuri: 
        1. (cel mai eficient) in care trebuie sa ne indepartam de piatra ca apoi sa ne aproipiem treptat
        2. (mai putin eficient) in care intai ne apropiem de piatra dupa care oscileaza apropierile si departarile 
            (departari care au insa arii mult mai mici decat aria data de prima departare a drumului 1)
    In acest caz, algoritmul va alege initial drumul 2 si va continua pe acesta intrucat valoarea f a drumului 1 obtinuta dupa un pas
    va fi mai mare decat valorile f ale drumului 2 obtinute in pasii intermediari.
    In acest caz, euristica va supraestima valoarea efectiva h, deci nu este admisibila.
    Euristica va supraestima valoarea efectiva h ori de cate ori drumul nu va urma in intregime dreptunghiul pentru care se face aria.
'''
