import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
Zakladom dannej aplikacie je dva rezimy: 
    Interaktivny - Pocas ktoreho user dokaze pomocou trackbarov nastavit si HSV masku tak aby oddelit potrebny objekt od ostatnych.
    Zdelavaci rezim - Pocas ktoreho na hlavnom scrine budu vypocitane koordinaty hladaneho objektu. 

Interface vytvorenej apky je predstaveny tromi oknami:

    Screen - okno obsahujuce hlavny, povodny obrazok, ktory sa meni v zavislosti od nastavenia trackbarov. 
        Sluzi na znazornenie procesu pouzitia masky na hladania klucoveho objektu.

    Screen s trackbarmi - okno obsahujuce trackbary, ktore sluzia na nastavenia maximalnej a minimalnej hodnot kazdej z komponent HSV masky.

    Option screen - pomocne okno na ktorom je znazornena aktualna HSV maska, ktora bola nastavena pomocou trackbarov.
        Okrem toho dane okno obsahuje minitext z popisom aktulne-zopnuteho rezimu, a kratku instrukciu. 


Na prepnutie rezimou pouzil som tlacitko "C".
"""

def hsv_to_bgr(img, mode=True):
    """
    funkcia na konvertaciu obrazku do HSV formatu
    :param img: obrazok vo formate BRG
    :param mode: Urcuje ulohu: Ak True - priama uloha, ak Else - obratena
    :return: obrazok vo formate HSV
    """
    return (cv2.cvtColor(img, cv2.COLOR_BGR2HSV) if mode
            else cv2.cvtColor(img, cv2.COLOR_HSV2BGR))


def nothing(*arg):
    pass


##########################################################################################
# Vytvaram GUI okno, kde budu umestnene samotne trackbary HSV nastaveni:
cv2.namedWindow('Set1', cv2.WINDOW_KEEPRATIO)

# Trackbar regulacie odtieni:
cv2.createTrackbar('H1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('H2', 'Set1', 255, 255, nothing)

# Trackbar regulacie sytosti:
cv2.createTrackbar('S1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('S2', 'Set1', 255, 255, nothing)

# Trackbar regulacie jasu:
cv2.createTrackbar('V1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('V2', 'Set1', 255, 255, nothing)
############################################################################################################


def shower(mask, img):
    """
    Funkcia ktora sluzi na naskovanie vstupneho obrazku, 
    pomocou masky ktora tiez je vstupnym argumentom funkcii.
    Okrem toho, uvedena funkcia aj zdiela maskovany obrazok.
    Vystupom uvedenej funkcii je tak isto maskovany obrazok.
    """
    masked_img = cv2.bitwise_or(0, img.copy(), mask=mask.copy())
    cv2.imshow('Screen', masked_img)
    
    return masked_img


def main():
    img = cv2.imread(rf'/home/volodymyr/Рабочий стол/Aplikovatelne_riesenia/CV/HSV_IMG_SET/shapes_sizes.png')  # Citame vstupny obrazok.
    img = cv2.resize(img, (760, 700))  # Z dvovodu zrucnosi zmenime rozmer vstupneho obrazku.

    blured_img = cv2.GaussianBlur(img.copy(), (7, 7), cv2.BORDER_DEFAULT)  # Na zrychlenie procesu pouzijme blur.
    hsv_img = cv2.cvtColor(blured_img, cv2.COLOR_BGR2HSV)  # Z dvovodu spresnenia hladanie objektu na obrazku konverujeme obrazok do HSV farebnej modely.

    new_values = False  # Premenna do ktorej budeme zapisovat stav masky i v dalsom cykle porovnavat z aktualnym stavom masky.

    while True:
        ############################################################################################################
        value_container1 = {}  # Kontainer do ktoreho budu zapisane hodnoty masky, urcene pomocou trackbarov.

        h1 = cv2.getTrackbarPos('H1', 'Set1')  # Dolna hranica odtieny v ramci HSV masky.
        value_container1['H1'] = h1  # Zapisujeme H1 do kontaineru.
        h2 = cv2.getTrackbarPos('H2', 'Set1')  # Horna hranica odtieny v ramci HSV masky.
        value_container1['H2'] = h2  # Zapisujeme H2 do kontaineru.

        s1 = cv2.getTrackbarPos('S1', 'Set1')  # Horna hranica sytosti v ramci HSV masky.
        value_container1['S1'] = s1  # Zapisujeme S1 do kontaineru.
        s2 = cv2.getTrackbarPos('S2', 'Set1')  # Horna hranica sytosti v ramci HSV masky.
        value_container1['S2'] = s2  # Zapisujeme S2 do kontaineru.

        v1 = cv2.getTrackbarPos('V1', 'Set1')  # Horna hranica jasu v ramci HSV masky.
        value_container1['V1'] = v1  # Zapisujeme V1 do kontaineru.
        v2 = cv2.getTrackbarPos('V2', 'Set1')  # Horna hranica jasu v ramci HSV masky.
        value_container1['V2'] = v2  # Zapisujeme V2 do kontaineru.
        ############################################################################################################

        # Porovnavame aktualnu masku s maskom ktora bola zapisana v predoslej iteracii,
        # ak sa budu odlisovat tak vypiseme ju do konzoly ako aktualny stav masky:
        if value_container1 != new_values:  
            print(f"\nActual HSV MASK values:\n"
                  f"low_values = ({value_container1['H1']}, "
                  f"{value_container1['S1']}, "
                  f"{value_container1['V1']})\n"
                  f"high_values = ({value_container1['H2']}, "
                  f"{value_container1['S2']}, "
                  f"{value_container1['V2']})")

        new_values = value_container1  # Zapiseme aktualny stav masky do premennej ktara je na to urcene, aby v dalsej iteracii porovnat hodnoty.
        ############################################################################################################
        
        h_min = (h1, s1, v1)  # Dolne hranicne hdnoty farebnej masky.
        h_max = (h2, s2, v2)  # Horne hranicne hodnoty farebnej masky.
        masked_scr = cv2.inRange(hsv_img, h_min, h_max)  # Maskovany obrazk. S pouzitim aktualnych hodnot masky.

        masked = shower(masked_scr.copy(), img)  # Vytvorime a zdelame  maskovany obrazok.

        # Pri stlaceni tlacitka "C" pocas zdelania zapneme "Zdelavaci rezim". Ak je tento mod zapnuty - na maskovanom obrazku sa objavia koordynaty(x,y) objekta na nom znazorneneho.
        if cv2.waitKey(20) & 0xFF == ord('c'):   
            find_object(masked, masked_scr)  # Podstatu zdelavacieho modu vytvara funkcia find_object().

        # Vo vsetkych inych pripadoch bude zopnuty "Interaktivny rezim" pocas ktoreho nastavujesa HSV maska:
        else:
            draw_text(masked_scr, mode='I')  # Uvedieme to, ze mame zopnuty Interaktivny rezim v pomocnom okne(Option screen).

        cv2.imshow('Option', masked_scr)  # Nezavisle od toho aky rezim je zopnuty zdelame pomocne okno.


def find_object(masked_image, mask):
    """
    Funkcia obsahujuca skoro vsetko pre urcenie a zdelania koordinat taziska.

    Koordinaty taziska budu urcene na binarnom obrazku objecta, 
    pomocou momentov nulteho a prveho radov.

    Nasledovne zistene koordinaty budu zavasene na originalny obrazok(Screen),
    obsahujuci len object.
    """
    

    def get_position_to_draw(text, point, font_face, font_scale, thickness):
        """
        Funkcia ktora sluzi na zistovanie korektnych koordinat textu ktory chcme uvediet,
        z ohladom na dlzku textu a pozadovanyn offsetom umestnenia.

        Dalo by sa tuto funkciu preniest aj do glabalnej oblasti, ale zatial,
        kym sa vyuziva iba v jednom mieste nechal som ju tu, aby vsetko co sa tyka pozicie taziska bolo pokope:0
        """
        text_size = cv2.getTextSize(text, font_face, font_scale, thickness)[0]  # Zistime skutocne rozmery poziadovaneho na uvedenie textu(z ohladom na jeho parametry).

        # Najdeme stred textu:
        x_correct = point[0] - text_size[0] / 2  
        y_correct = point[1] + text_size[1] / 2

        # Urcime pre kazdu OS aktualny pre nas offset:
        x_offset = 30 
        y_offset = 25

        # Vratime korektne, z ohladom na vyssie uvede podmienky, koordynaty:
        return round(x_correct + x_offset), round(y_correct + y_offset)

    # Na zistovanie "pixeloveho taziska" objektu pouzil som momenty:
    moments = cv2.moments(mask.copy(), True)  # Momenty vypocitavaju sa pre binarny obrazok.

    # Najdeme koordynaty(x, y) "taziska" objekta pomocou momentov nultoveho a prveho riadu:
    x_centroid = round(moments['m10'] / moments['m00'])
    y_centroid = round(moments['m01'] / moments['m00'])

    print(f'\nCentre of object is: ({x_centroid},{y_centroid})')

    # Znazornime tazisko pomocou plneho bodu:
    cv2.circle(masked_image, (x_centroid, y_centroid), 6, (200, 60, 160), -1)

    # Najdeme vyhovujece pre nas koordynaty na umstnenie textu, ktory bude obsahovat samotne koordynaty "taziska" objekta:
    (x, y) = get_position_to_draw(f'{x_centroid},{y_centroid}',(x_centroid, y_centroid), cv2.FONT_HERSHEY_TRIPLEX, 1.2, 3)
    # Znazornime koordynaty taziska na 'hlavnov' screene:
    cv2.putText(masked_image, f'({x_centroid}, {y_centroid})',(x, y), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)

    # Zmenime uz zdelane hlavne okno. Zdelame ho este raz, len ze na rozdiel od prveho zdelania, 
        # dane okno bude obsahovat obraz z uvedenymi koordynatamy "taziska" objektu:
    cv2.imshow('Screen', masked_image)

    # 
    draw_text(mask, mode='S', coordinates=(x_centroid, y_centroid))  # Uvedieme to, ze mame zopnuty Zdelavaci rezim v pomocnom okne(Option screen).
    # Okrem toho, v tomto pripade na vstup funkcie davame aj zistene koordinaty "taziska" - ich tiez uvedieme v pomocnom okne()

    cv2.imshow('Option', mask)  # Po zeveseni textu na pomocnom okne zmenime joho stav, aby tam ten text uz bol uvedeny. 

    cv2.waitKey(0)  # Kym nebude zmeneny rezim - nechame obrazovky vysiet v aktualnom stave.


def draw_text(scr, mode='I', coordinates=(0, 0)):
    """
    Funkcia urcena na zdelanie stavu aplikacie a kratkej istrukcie k nej
    Text sa zdiela na pomocnu obrazovku.
    Pri zmene rezimu funkcnosti appky dana funkcia meni stav textu.
    """

    # Text ktory bude zavaseny v pomocnom okne zavisi na zopnutom rezime:
    if mode == 'I':  # Ak je zopnuty "Interaktivny rezim".
        text1 = "InteractiveMode.Set a mask to find the object."
        text2 = '''Press "C" to find object's coordinates.'''

    elif mode == 'S': # Ak je zopnuty "Zdelavaci rezim".
        text1 = f'Coordinates found: {coordinates}'
        text2 = 'Press "C" to start InteractiveMode'

    # Manualne urcime dve pozicie pre zavesenie textu na obrazovke. Text bude dvojradkovy - prave preto urcujeme dve pozicie:
    pos1 = (5, 660)
    pos2 = (5, 695)

    # Zdelame text na obrazovku:
    cv2.putText(scr, text1, pos1, cv2.FONT_HERSHEY_DUPLEX, 1, (255), 1)
    cv2.putText(scr, text2, pos2, cv2.FONT_HERSHEY_TRIPLEX, 1, (255), 1)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)
