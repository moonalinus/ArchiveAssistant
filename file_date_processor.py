import os
import datetime
import random

# Запрашиваем путь до папки
folder_path = input("Введите путь до папки: ")

# Преобразуем начальную дату и время в формат timestamp
start_date = datetime.datetime(2014, 12, 9, 1, 57, 20).timestamp()

# Обходим все папки и файлы в указанной папке
for root, dirs, files in os.walk(folder_path):
    # Сохраняем время последнего изменения предыдущего файла
    prev_time = start_date
    for file in files:
        # Получаем полный путь до файла
        file_path = os.path.join(root, file)
        # Генерируем рандомное количество секунд в диапазоне от 20 до 50
        random_seconds = random.randint(20, 50)
        # Вычисляем новое время последнего изменения файла
        new_time = prev_time + random_seconds
        # Изменяем время последнего изменения файла
        os.utime(file_path, (new_time, new_time))
        # Сохраняем время последнего изменения текущего файла для расчета времени следующего файла
        prev_time = new_time
    # Сохраняем время последнего изменения последнего файла в текущей папке для расчета времени первого файла в следующей папке
    start_date = prev_time

# /home/specialist/Рабочий стол/Елань описи и папки/Елань 1957 обработано/9 декабря