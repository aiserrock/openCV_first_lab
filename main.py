from PIL import Image, ImageDraw
import numpy as np
import cv2


def brightness_correction(image_name, gamma):
    image = cv2.imread(image_name)
    invariantGamma = 1.0 / gamma
    # формируем таблицу яркостей
    table = np.array([((i / 255.0) ** invariantGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    # пересчитываем значение яркости каждого пикселя согласно таблице
    dst = cv2.LUT(image, table)
    res_name = 'result/light.jpeg'
    cv2.imwrite(res_name, dst)
    return res_name


def main():
    # 1. осветляем изображение
    light = brightness_correction('images/robo1.jpeg', gamma=1.3)


if __name__ == "__main__":
    main()
