import cv2


def hsv_convert(img):
    """
    funkcia na konvertaciu obrazku do HSV formatu
    :param img: obrazok vo formate BRG
    :return: obrazok vo formate HSV
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def nothing(*arg):
    pass


def setting(img):
    """
    funkcia na nastavenie farebnej masky na okamzity obrazok
    pouziva opencv - GUI
    :param img: obrazok, vo formate BGR
    :return:
    """
    # Vytvaram GUI okno, kde budu umestnene samotne trackbary HSV nastaveni
    cv2.namedWindow('Set', cv2.WINDOW_KEEPRATIO)
    # Trackbar regulacie dtieni
    cv2.createTrackbar('H1', 'Set', 0, 255, nothing)
    cv2.createTrackbar('H2', 'Set', 255, 255, nothing)
    # Trackbar regulacie sytosti
    cv2.createTrackbar('S1', 'Set', 0, 255, nothing)
    cv2.createTrackbar('S2', 'Set', 255, 255, nothing)
    # Trackbar regulacie jasu
    cv2.createTrackbar('V1', 'Set', 0, 255, nothing)
    cv2.createTrackbar('V2', 'Set', 255, 255, nothing)

    hsv_img = hsv_convert(img)

    new_values = False  # Premenna, ktora pomaha pri vypisovany aktualnych hodnot masky
    while True:
        value_container = {}  # Kontainer z hodnotami masky
        #######################################################
        h1 = cv2.getTrackbarPos('H1', 'Set')  # Dolna hranica odtieny v ramci HSV masky
        value_container['H1'] = h1  # Zapisujeme H1 do kontaineru
        h2 = cv2.getTrackbarPos('H2', 'Set')  # Horna hranica odtieny v ramci HSV masky
        value_container['H2'] = h2  # Zapisujeme H2 do kontaineru

        s1 = cv2.getTrackbarPos('S1', 'Set')  # Horna hranica sytosti v ramci HSV masky
        value_container['S1'] = s1  # Zapisujeme S1 do kontaineru
        s2 = cv2.getTrackbarPos('S2', 'Set')  # Horna hranica sytosti v ramci HSV masky
        value_container['S2'] = s2  # Zapisujeme S2 do kontaineru

        v1 = cv2.getTrackbarPos('V1', 'Set')  # Horna hranica jasu v ramci HSV masky
        value_container['V1'] = v1  # Zapisujeme V1 do kontaineru
        v2 = cv2.getTrackbarPos('V2', 'Set')  # Horna hranica jasu v ramci HSV masky
        value_container['V2'] = v2  # Zapisujeme V2 do kontaineru
        #######################################################
        if value_container != new_values:  # Ak hodnoty v tomto kontainere odlisuju sa od
            # hodnot kontainera z predosloho cyklu, - tak vypiseme do kozoly
            print(f"\nActual MASK:\n"
                  f"low_clr = ({value_container['H1']}, "
                  f"{value_container['S1']}, "
                  f"{value_container['V1']})\n"
                  f"high_clr = ({value_container['H2']}, "
                  f"{value_container['S2']}, "
                  f"{value_container['V2']})")
        new_values = value_container  # Skopirujem aktualne hodnoty do vonkajsej premennej
        #######################################################
        h_min = (h1, s1, v1)  # Dolne hodnoty farebnej masky
        h_max = (h2, s2, v2)  # Horne hodnoty farebnej masky
        masked_image = cv2.inRange(hsv_img, h_min, h_max)  # Maskovany obrazk

        k = 2  # Koeficient zmensenia okna maskovaneho obrazku, ktore bude ukazane ako priklad pouzitia aktualnej masky
        result_scr_h = img.shape[1]//k  # Vyska okna
        result_scr_w = img.shape[0]//k  # Syrka okna
        result_scr = cv2.resize(masked_image, (result_scr_h, result_scr_w))

        cv2.imshow('result', result_scr)  # Zverejnovanie obrazku z pouzitiem akrualne masky

        key_press = cv2.waitKey(30)
        if key_press == ord('q'):  # Tlacitko 'q' sluzi na zatvaranie nastavovaceho okna a
            # okna z vyzledkom pouzitia masky
            cv2.destroyWindow('Set')
            cv2.destroyWindow('result')
            break


def main():
    cap = cv2.VideoCapture('YourVideo.mp4')  # Otvarame video

    while True:
        scr_ok, scr = cap.read()  # Citame aktualny frame
        if scr_ok:  # Ak je OK

            try:

                cv2.imshow('video', scr)  # Tak ho uverejnujeme
                key_press = cv2.waitKey(30)  # Cakame na stlacenie tlacidka

                if key_press == ord('q'):  # Ak stalcili 'q' - koncime
                    break
                if key_press == ord('p'):  # Ak stlacili 'p' - robime pauzu a spustame nastroje na vytvorenie masky
                    setting(scr)

            except Exception as ex:  # Vychytavame chyby
                print(ex)
                break

    cap.release()
    cv2.destroyAllWindows()  # Ukoncujeme script


if __name__ == "__main__":
    main()
