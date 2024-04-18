import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re
from craft_text_detector import Craft
import json
import labelbox

client = labelbox.Client(api_key='<your API key>')
params = {
	"data_row_details": True,
	"metadata_fields": True,
	"attachments": True,
	"project_details": True,
	"performance_details": True,
	"label_details": True,
	"interpolated_frames": True
}

project = client.get_project('clul1v27m00ur073d1v4s61vo')
export_task = project.export_v2(params=params)

export_task.wait_till_done()
if export_task.errors:
	print(export_task.errors)
export_json = export_task.result
print(export_json)

# Загрузка модели CRAFT для детекции текста
craft = Craft(output_dir=None, crop_type="poly", cuda=False)


# Функция для извлечения сущностей из текста с помощью регулярных выражений
def extract_entities(text, boxes):
    # Ищем название газеты в верхней части страницы
    newspaper_name = ''
    for box, line in zip(boxes, text.split('\n')):
        if box[1] < 100:  # Предполагаем, что название газеты находится в верхних 100 пикселях
            newspaper_name = line.strip()
            break

    # Ищем дату выпуска
    date = re.findall(r'\d{1,2}\s+\w+\s+\d{4}\s+г', text)

    # Ищем номер выпуска
    issue_numbers = re.findall(r'№\s+(\d+)\s+\((\d+)\)', text)
    issue_number = issue_numbers[0][0] if issue_numbers else ''
    total_issue_number = issue_numbers[0][1] if issue_numbers else ''

    # Ищем номер страницы в верхнем левом или правом углу
    page_number = ''
    for box, line in zip(boxes, text.split('\n')):
        if (box[0] < 100 or box[2] > image.shape[1] - 100) and box[1] < 100:
            page_numbers = re.findall(r'\d+', line)
            if page_numbers:
                page_number = page_numbers[0]
                break

    special_issue = 'Специальный выпуск' if 'специальный выпуск' in text.lower() else ''

    return newspaper_name, date[0] if date else '', issue_number, total_issue_number, page_number, special_issue


# Путь к изображению
image_path = 'path/to/your/image.jpg'

# Загрузка изображения
image = cv2.imread(image_path)

# Детекция текстовых регионов
prediction_result = craft.detect_text(image)

# Словарь для хранения результатов
results = {}

all_boxes = []
all_texts = []

for region in prediction_result["boxes"]:
    # Получаем координаты региона
    x, y, w, h = region
    all_boxes.append(region)

    # Обрезаем регион из изображения
    cropped_image = image[y:y + h, x:x + w]

    # Распознаем текст в регионе
    text = pytesseract.image_to_string(cropped_image, lang='rus')
    all_texts.append(text)

# Объединяем весь текст в один
full_text = '\n'.join(all_texts)

# Извлекаем сущности из текста
entities = extract_entities(full_text, all_boxes)

# Сохраняем результаты
results = {
    'newspaper_name': entities[0],
    'date': entities[1],
    'issue_number': entities[2],
    'total_issue_number': entities[3],
    'page_number': entities[4],
    'special_issue': entities[5]
}

# Выводим результаты
print(f"Newspaper name: {results['newspaper_name']}")
print(f"Date: {results['date']}")
print(f"Issue number: {results['issue_number']}")
print(f"Total issue number: {results['total_issue_number']}")
print(f"Special issue: {data['special_issue']}\n")