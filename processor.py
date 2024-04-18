import os
import glob
import re
import PyPDF2
import pandas as pd

def get_sorted_folders(path):
    folders = glob.glob(os.path.join(path, "[0-9]*"))
    folders.sort(key=lambda x: float(os.path.basename(x)))
    return folders

def get_sorted_files(folder):
    files = glob.glob(os.path.join(folder, "*.pdf"))
    files.sort(key=lambda x: int(re.search(r"-(\d+)\.pdf$|(\d+)\.pdf$", os.path.basename(x)).group(1) or re.search(r"-(\d+)\.pdf$|(\d+)\.pdf$", os.path.basename(x)).group(2)))
    return files

def extract_info_from_first_page(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page = pdf_reader.pages[0]
        text = page.extract_text()

        newspaper_name = re.search(r'Название газеты: (.+)', text)
        if newspaper_name:
            newspaper_name = newspaper_name.group(1)
        else:
            newspaper_name = ''

        date_match = re.search(r'(\d{1,2} [а-я]+ \d{4} года|[а-я]+ \d{4})', text)
        if date_match:
            date = date_match.group(1)
        else:
            date = ''

        issue_match = re.search(r'№ (\d+) \(\d+\)', text)
        if issue_match:
            issue = issue_match.group(1)
        else:
            issue = ''

        special_issue = 'специальный выпуск' in text or 'спецвыпуск' in text

        return {
            'newspaper_name': newspaper_name,
            'date': date,
            'issue': issue,
            'special_issue': special_issue,
            'page': 1
        }

def extract_page_number(text):
    page_number = re.search(r'(\d+)', text)
    if page_number:
        return int(page_number.group(1))
    else:
        return None

def process_folder(folder):
    files = get_sorted_files(folder)
    data = []
    for i, file in enumerate(files):
        if i == 0:
            info = extract_info_from_first_page(file)
            page = info['page']
        else:
            with open(file, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                page = extract_page_number(pdf_reader.pages[0].extract_text())
                if page is None:
                    continue

            info = {
                'newspaper_name': info['newspaper_name'],
                'date': info['date'],
                'issue': info['issue'],
                'special_issue': info['special_issue'],
                'page': page
            }

        data.append({
            'folder': os.path.basename(folder),
            'file': os.path.basename(file),
            'newspaper_name': info['newspaper_name'],
            'date': info['date'],
            'issue': info['issue'],
            'special_issue': info['special_issue'],
            'page': info['page'],
            'size': os.path.getsize(file)
        })

    return data

def main():
    path = input("Enter the path to the folder: ")
    folders = get_sorted_folders(path)

    data = []
    for folder in folders:
        folder_data = process_folder(folder)
        data.extend(folder_data)

    columns = ['folder', 'file', 'newspaper_name', 'date', 'issue', 'special_issue', 'page', 'size']
    df = pd.DataFrame(data, columns=columns)

    # save data to CSV file
    df.to_csv('output.csv', index=False)

    # print data to console
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
