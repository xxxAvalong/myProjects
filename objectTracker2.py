from pickle import TRUE
import cv2
import numpy as np
"""
Tato apka je pokrocilou verziou aplikacie, ktora pouzivala dva rezimy funkcnosti,
avsak nevediela poskitnut interface pre realtime vytvorenie masky sledovanie farebneho objektu.
Okrem toho minula verzia bola o dost "robustnejsia" ca ma aj posunulo k vytvoreniu tejto verzie.

Prave preto bola vyvinuta tato aplikacia, jej ucelom je poskytnut uzivatelu interface 
pre sledovanie farebneho objektu v raelnom case, s pouzitim HSV masky ktora sa ale tiez nastavuje realtime.

Tak isto ako aj v minulej verzie - GRO danej appky je pouzitie momentov binarneho obrazku 
na zistovanie koordinat poziadovaneho farebneho objektu.

Mozno v buducnosti budu poskitnute aj ine moznosti vytvorenie binarneho obrazku pre zistovanie koord.
"""
 
########################################################################################################################
# Sekcia obsahujucu veci ktore sa tykaju obrazovky z trackbarmi nastavenia HSV masky.

# Nakolko fungujeme z HSV farebnym modelom oznacenie mame track barov mame take:
trackbar_vals = ['H1', 'H2', 'S1', 'S2', 'V1', 'V2']  # Kde H - odtien, S - sytost, V - svetlost. Index 1 urcuje hornu hranicu, 2 - dolnu.

val = False  # Premena ktora sa pouziva na ulozenie hodnot HSV masky aktualneho cyklu aby ich potom porovnat z 
# aktualnymi hodnotami v dalsom cykle. V pripade nezhody(v novom cykle maska bola zmenena) nova aktualna maska bude uvedena v konzole.

# Vytvorime okno v ktorom budu umestnene trackbary:
cv2.namedWindow('SetUp Mask')


def nothing(*arg):
    """
    Funkcia ktora nic ne robi)
    """
    pass
 

 # Vytvirime trackbary vo vopred nachystanomm okne:
for e,bar in enumerate(trackbar_vals):

    # Nech trackbary spodnych hodnot(parne) povodne maju hodnotu 0:
    if e%2 == 0:  
        cv2.createTrackbar(f'{bar}', 'SetUp Mask', 0, 255, nothing)

    # Nech trackbary hornych hodnot(neparne) povodne maju hodnotu 255:
    else: 
        cv2.createTrackbar(f'{bar}', 'SetUp Mask', 255, 255, nothing)
 

def tb_val(name):
    """
    Funkcia urcena na zistovanie aktualneho stavu(hodnoty) 
    jednotlivych trackbarov podlaich ich nazvy.
    """
    return cv2.getTrackbarPos(name, 'SetUp Mask')
 

def get_tb_values():
    """
    Funkcia urcena na odrziavania okamzitych hodnot trackbarov.
    Okrem toho funkcia porovnava hodnoty trackbarov v aktualnom a 
    predoslom cykle - ak su rozne tak do konzoly budu uvedne
    aktualne stavy trackbarov(vpodtate masky HSV).
    """
    global val, trackbar_vals
    trackbar_values_cantainer = {}  # Slovnik do ktoreho budu zapisane aktualne hodnoty trackbarov,
    # s tym ze keys - nazvy jednotlivych trackbarov, values - ich hodnoty.

    for bar in trackbar_vals:  # Naplnime slovnik(nazov: aktualna_hodnota):
        trackbar_values_cantainer[bar] = tb_val(bar)

    # Porovname aktualne hodnoty barov z ich hodnotamy v predoslom volani danej funkcie:
    if trackbar_values_cantainer != val:
        print(f"\nActual HSV MASK values:\n"
                  f"low_values = ({trackbar_values_cantainer['H1']}, "
                  f"{trackbar_values_cantainer['S1']}, "
                  f"{trackbar_values_cantainer['V1']})\n"
                  f"high_values = ({trackbar_values_cantainer['H2']}, "
                  f"{trackbar_values_cantainer['S2']}, "
                  f"{trackbar_values_cantainer['V2']})")

    val = trackbar_values_cantainer;  # Zapiseme aktalne hodnoty do globalnej premennej, 

    # Vratime zistene okamzite hodnoty barov:
    return trackbar_values_cantainer; 

########################################################################################################################


def main():
    # Odrzime obraz:
    cap = cv2.VideoCapture(0)  # V mojom pripade som vyuzival webcameru notebooku preto mam parameeter 0.

    while TRUE:

        # Precitame obraz:
        scr_ok, scr = cap.read()

        if scr_ok:  # Ak obraz je korektny.

            scr = cv2.flip(scr, 1)  # V mojom pripade obraz som otocil z toho dvovodu ze som ho mal zrkadlovy.
            scr = cv2.resize(scr, (640, 480))  # Vyuzijeme najbeznejsie rozlisenie obycajnych kamier. 

            # Pre spracovanie vytvorime kopiu aktualneho obrazu:
            img = scr.copy()  

            # Nakonfigurujeme trackbary i tym padom vytvorime masku, 
            # ktora bude obsahovat len poziadovany farebny objekt:
            masked_img = hsv_mask_use(img)

            # Zistime koordinaty centroidu binarneho obrazku poziadovaneho objektu:
            centroid_coords = get_coords(masked_img)
            x = centroid_coords['x']
            y = centroid_coords['y']

            # Znazornime centroid objektu, a jeho koordinaty na povodnom obrazku:
            draw_centroid(scr, x, y)

            # Zdelame okna:

            # Pridame navod na uzavretie appky na maskovany obrazok(pomocne okno):
            cv2.putText(masked_img, 'Press "Q" to exit.', (5, 470), cv2.FONT_HERSHEY_DUPLEX, 1, (255), 1)
            cv2.imshow('Option', masked_img)  # Pomocne, ktore obsahuje obrazok maskovany pomocou aktualnej konfiguracie tracjbarov.

            cv2.imshow('Screen', scr)  # Hlavne, ktore obsahuje povodny obrazok, z uvedenym 'taziskom' pozadovaneho objektu 
            # a jeho koordinatmy.


            # Na uzavretie appky budeme pouzivat tlacitko 'q':
            if cv2.waitKey(30) == ord('q'): 
                    break


    cap.release()
    cv2.destroyAllWindows()
 

def hsv_mask_use(img):
    """
    Funkcia urcena na pouzitie aktualnej kofiguracie HSV masky
    k vstupnemu do nej obrazku.

    Funkcia vraca maskovany, BINARNY, obrazok.
    """

    # Z dvovodu efektivity fungovat budeme HSV farebnym modelom:
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Zistime okamzity stav(konfiguraciu) trackbarov:
    mask_values = get_tb_values()  # Kontainer(slovnik) z hodnotami.

    global trackbar_vals  # Pre zjednodusenie pouzijeme globalnu premennu obsahujucu nazvy jednotlivych barov:

    # "Rozbalime" kontainer:
    h1,h2, s1,s2, v1,v2 = [mask_values[value_name] for value_name in trackbar_vals]

    # Pouzijeme zistene okamzite hodnoty trackbarov ako spodne a vrchne hodnoty farebnej masky:
    binary_img = cv2.inRange(hsv_img, (h1, s1, v1), (h2, s2, v2), )

    # Vratime bonarny, maskovany obrazok(vpodstate masku):
    return binary_img
 

def get_coords(binary_img):
    """
    Funkcia urcena na zistovanie koordinat "taziska"
    (centroidu) binarneho obrazku. 
    Vyuzivaju sa na to momenty obrazku prveho a druheho radu.
    """

    # Zistime momenty vstupneho obrazku:
    moments = cv2.moments(binary_img, True)

    # Najdeme koordinaty centroida. Dal som to do Try preto,
    # lebo pri vstupe uplne cierneho obrazku bude nam vyskutovat
    # delenie na nulu - co sposobuje chyby(!):
    try:
        centroid_x = round(moments['m10'] / moments['m00'])
        centroid_y = round(moments['m01'] / moments['m00'])
    except:
        centroid_x = 1
        centroid_y = 1

    # Vratime koordinaty zisteneho centroidu:
    return {'x': centroid_x, 'y': centroid_y}
 

def draw_centroid(img, x, y):
    """
    Funkcia urcena na znazornenie "taziska" pozadovaneho
    farebnoho objektu z ohladom na aktualnej stav masky,
    ktora bola nakonfigurovana v 'SetUp Mask' okne.

    Okrem toho dana funkcia podporuje aj uvedenie na obrazku 
    akeho kolvek textu, z ohladom na jeho rozmery. 
    V mojom pripade to su samotne koordinaty "taziska".
    """

    # Znazornime samotny centroid objektu:
    cv2.circle(img, (x, y), 6, (200, 60, 160), -1)

    # Zistime rozmery textu ktory chcme znazornit:
    text_size = cv2.getTextSize(f'({x}, {y})', cv2.FONT_HERSHEY_TRIPLEX, 1.2, 3)[0]

    # Spravime korekcie koordinat centroidu z ohladom na rozmery textu na uvedenie:

    # K stedu koordinat textu pridame vyhovujuce nam offsety:
    x_text = round((x - text_size[0] / 2 ) + 100)  
    y_text = round((y + text_size[1] / 2) + 25)

    # Z ohladom na korekciu koordinat zavesime text na obrazovke:
    cv2.putText(img, f'({x}, {y})',(x_text, y_text), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)

 
if __name__ == "__main__":
    main()