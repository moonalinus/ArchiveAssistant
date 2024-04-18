import os
import shutil
import re

def sort_files(source_folder, destination_folder):
    # Проверяем, существует ли исходная папка
    if not os.path.exists(source_folder):
        print(f"Исходная папка '{source_folder}' не найдена.")
        return

    # Проверяем, существует ли папка назначения
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Создана папка назначения '{destination_folder}'.")

    # Словарь для хранения списка файлов для каждой газеты
    newspaper_files = {}

    # Перебираем все файлы в исходной папке
    for filename in os.listdir(source_folder):
        # Проверяем, является ли файл изображением в нужном формате
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')) and '.' in filename[:-4]:
            # Извлекаем номер газеты и страницы из названия файла
            newspaper_number, page_number = filename.split('.')[:2]

            # Добавляем файл в список файлов для газеты
            if newspaper_number not in newspaper_files:
                newspaper_files[newspaper_number] = []
            newspaper_files[newspaper_number].append(filename)

    # Копируем файлы в папки газет
    for newspaper_number, files in newspaper_files.items():
        # Создаем папку для газеты, если она еще не существует
        newspaper_folder = os.path.join(destination_folder, f"№ {newspaper_number}")
        if not os.path.exists(newspaper_folder):
            os.makedirs(newspaper_folder)
            print(f"Создана папка для газеты '{newspaper_folder}'.")

        # Перебираем файлы для текущей газеты
        for filename in files:
            # Копируем файл в папку газеты
            source_file_path = os.path.join(source_folder, filename)
            destination_file_path = os.path.join(newspaper_folder, filename)
            shutil.copy(source_file_path, destination_file_path)

    # Переименовываем файлы в папках газет
    # Получаем список папок газет
    newspaper_folders = [folder for folder in os.listdir(destination_folder) if folder.startswith('№ ')]
    # Сортируем папки газет по номеру газеты
    newspaper_folders = sorted(newspaper_folders, key=lambda x: int(re.search(r'№ (\d+)', x).group(1)))

    # Инициализируем счетчик файлов
    file_counter = 1

    # Перебираем папки газет
    for newspaper_folder in newspaper_folders:
        # Получаем путь к папке газеты
        newspaper_folder_path = os.path.join(destination_folder, newspaper_folder)

        # Получаем список файлов в папке газеты
        files = os.listdir(newspaper_folder_path)
        # Сортируем файлы по номеру газеты и страницы
        files = sorted(files,key=lambda x: (int(re.search(r'(\d+)\.', x).group(1)), int(re.search(r'\.(\d+)\.', x).group(1))))

        # Перебираем отсортированные файлы
        for filename in files:
            # Извлекаем номер газеты и страницы из названия файла
            newspaper_number, page_number = filename.split('.')[:2]

            # Формируем новое имя файла
            new_filename = f"{file_counter} - №{newspaper_number}-{page_number}.{filename.split('.')[-1]}"

            # Переименовываем файл
            source_file_path = os.path.join(newspaper_folder_path, filename)
            destination_file_path = os.path.join(newspaper_folder_path, new_filename)
            os.rename(source_file_path, destination_file_path)
            print(f"Файл '{filename}' переименован в '{new_filename}'.")

            # Увеличиваем счетчик файлов
            file_counter += 1

    print("Операция завершена.")

# Запрашиваем путь к исходной папке
source_folder = input("Введите путь к папке с файлами: ")

# Запрашиваем путь к папке назначения
destination_folder = input("Введите путь к папке, где будут создаваться новые папки: ")

# Вызываем функцию сортировки файлов
sort_files(source_folder, destination_folder)

# /home/specialist/Рабочий стол/Еланский колхозник 1957

# /home/specialist/Рабочий стол/Елань описи и папки/Елань 1957 обработано