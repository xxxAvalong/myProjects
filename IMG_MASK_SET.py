import cv2
import numpy as np


def hsv_convert(img):
    """
    funkcia na konvertaciu obrazku do HSV formatu
    :param img: obrazok vo formate BRG
    :return: obrazok vo formate HSV
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def nothing(*arg):
    pass



# Vytvaram GUI okno, kde budu umestnene samotne trackbary HSV nastaveni
cv2.namedWindow('Set1', cv2.WINDOW_KEEPRATIO)
# Trackbar regulacie dtieni
cv2.createTrackbar('H1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('H2', 'Set1', 255, 255, nothing)
# Trackbar regulacie sytosti
cv2.createTrackbar('S1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('S2', 'Set1', 255, 255, nothing)
# Trackbar regulacie jasu
cv2.createTrackbar('V1', 'Set1', 0, 255, nothing)
cv2.createTrackbar('V2', 'Set1', 255, 255, nothing)


def main():
    img = cv2.imread('YOUR_IMG.jpeg')
    img = cv2.resize(img, (700, 700))
    blured_img = cv2.GaussianBlur(img.copy(), (7, 7), cv2.BORDER_DEFAULT)
    hsv_img = cv2.cvtColor(blured_img, cv2.COLOR_BGR2HSV)
    new_values = False  # Premenna, ktora pomaha pri vypisovany aktualnych hodnot masky
    while True:
        value_container1 = {}  # Kontainer z hodnotami masky
        #######################################################
        h1 = cv2.getTrackbarPos('H1', 'Set1')  # Dolna hranica odtieny v ramci HSV masky
        value_container1['H1'] = h1  # Zapisujeme H1 do kontaineru
        h2 = cv2.getTrackbarPos('H2', 'Set1')  # Horna hranica odtieny v ramci HSV masky
        value_container1['H2'] = h2  # Zapisujeme H2 do kontaineru

        s1 = cv2.getTrackbarPos('S1', 'Set1')  # Horna hranica sytosti v ramci HSV masky
        value_container1['S1'] = s1  # Zapisujeme S1 do kontaineru
        s2 = cv2.getTrackbarPos('S2', 'Set1')  # Horna hranica sytosti v ramci HSV masky
        value_container1['S2'] = s2  # Zapisujeme S2 do kontaineru

        v1 = cv2.getTrackbarPos('V1', 'Set1')  # Horna hranica jasu v ramci HSV masky
        value_container1['V1'] = v1  # Zapisujeme V1 do kontaineru
        v2 = cv2.getTrackbarPos('V2', 'Set1')  # Horna hranica jasu v ramci HSV masky
        value_container1['V2'] = v2  # Zapisujeme V2 do kontaineru
        #######################################################
        if value_container1 != new_values:  # Ak hodnoty v tomto kontainere odlisuju sa od
            # hodnot kontainera z predosloho cyklu, - tak vypiseme do kozoly
            print(f"\nActual MASK:\n"
                  f"low_clr = ({value_container1['H1']}, "
                  f"{value_container1['S1']}, "
                  f"{value_container1['V1']})\n"
                  f"high_clr = ({value_container1['H2']}, "
                  f"{value_container1['S2']}, "
                  f"{value_container1['V2']})")
        new_values = value_container1  # Skopirujem aktualne hodnoty do vonkajsej premennej
        #######################################################
        h_min = (h1, s1, v1)  # Dolne hodnoty farebnej masky
        h_max = (h2, s2, v2)  # Horne hodnoty farebnej masky
        masked_image = cv2.inRange(hsv_img, h_min, h_max)  # Maskovany obrazk

        result_scr_h = img.shape[1]
        result_scr_w = img.shape[0]
        result_scr = cv2.resize(masked_image, (result_scr_h, result_scr_w))

        cv2.imshow('result', result_scr)

        cv2.waitKey(30)


if __name__ == "__main__":
    main()