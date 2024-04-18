import os
import shutil

def copy_files_recursively(src_dir, dest_dir):
    # Проверяем, существует ли исходная папка
    if not os.path.exists(src_dir):
        print(f"Исходная папка '{src_dir}' не найдена.")
        return

    # Проверяем, существует ли папка назначения
    if not os.path.exists(dest_dir):
        print(f"Папка назначения '{dest_dir}' не найдена, создаем ее.")
        os.makedirs(dest_dir)

    # Обрабатываем все элементы в исходной папке
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dest_item = os.path.join(dest_dir, item)

        # Если это папка, рекурсивно обрабатываем ее
        if os.path.isdir(src_item):
            print(f"Обрабатываем папку '{src_item}'...")
            copy_files_recursively(src_item, dest_dir)
        # Если это файл, копируем его
        elif os.path.isfile(src_item):
            print(f"Копируем файл '{src_item}'...")
            shutil.copy2(src_item, dest_dir)

if __name__ == "__main__":
    src_dir = input("Введите путь до исходной папки: ")
    dest_dir = input("Введите путь до папки назначения: ")

    copy_files_recursively(src_dir, dest_dir)
    print("Копирование завершено.")

# /home/specialist/Рабочий стол/Елань 1952 обработано
# /home/specialist/Рабочий стол/1952 Еланский колхозник - № с 1 по 105 (н.8) м