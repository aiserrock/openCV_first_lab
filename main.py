from PIL import Image, ImageDraw
import numpy as np
import cv2

OUTPUT_PATH = 'result/'
IMAGES_PATH = 'images/'

# величина, на которую искомый цвет должен преобладать над другими цветами
PRELEVANCE_VARIABLE = 5
GAMMA = 0.4


# Гамма-коррекция (пособие стр. 37)
def brightness_correction(image_path):
    image = cv2.imread(image_path)
    # формируем массив lut новых яркостей
    # (таблица переходов, новое значение яркости для пикселя по индексу)
    table = np.array([((i / 255.0) ** GAMMA) * 255 for i in range(0, 256)]).astype("uint8")

    # пересчитываем значение яркости каждого пикселя согласно таблице
    result = cv2.LUT(image, table)
    res_name = OUTPUT_PATH + 'first_step_brightness_correction.jpeg'
    cv2.imwrite(res_name, result)
    return res_name


# Бинаризация (пособие стр. 56)
def binarization(light):
    image = Image.open(light)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    # переменные для вычисления ядра (количество и сумма зеленых и красных
    # пикселей, в которых преобладает синий)
    count = 0
    sum = 0.0
    for i in range(width):
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]

            maximum = max(r, g, b)

            if maximum == b and b > g + PRELEVANCE_VARIABLE and b > r + PRELEVANCE_VARIABLE:
                count += 1
                sum += ((g + r) / 2)

    if count == 0:
        # велечина, показывающая силу преобладания синего цвета над другими
        epsilon = 0.0
    else:
        epsilon = sum / count
    print(epsilon)

    for i in range(width):
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]

            maximum = max(r, g, b)

            if maximum == b and (g + r) / 2 < epsilon:
                draw.point((i, j), (255, 255, 255))
            else:
                draw.point((i, j), (0, 0, 0))

    res_name = OUTPUT_PATH + "second_step_binarization.jpeg"
    image.save(res_name)
    return res_name


def remove_noise(binarized):
    img = cv2.imread(binarized)
    # получим примитив (двумерный массив 7х7 заполненный единицами)
    # таким образом получили структуризирующий элемент для след операции
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 9))
    # используется мофрологическая опперация ОТКРЫТИЕ (эррозия -> диллатация)
    # см. методичка стр.87
    result = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return result


def main():
    # 1. осветляем изображение
    light = brightness_correction(IMAGES_PATH + 'robo3.jpeg')
    # 2. бинаризация
    binarized = binarization(light)
    # 3. удаление шумов
    result = remove_noise(binarized)
    cv2.imwrite(OUTPUT_PATH + "third_step_remove_noise.jpeg", result)


if __name__ == "__main__":
    main()
