import csv
import requests
import tkinter as tk

from tkinter import filedialog
from bs4 import BeautifulSoup


def read_from_source(mode='file'):
    if mode == 'file':
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r') as f:
            file_text = f.read().replace('\n', '')
        return file_text
    elif mode == 'url':
        resp = requests.get('http://127.0.0.1:5500/index.html')
        return resp.text


def parsing_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')

    print(soup.prettify(formatter="html5"))

    exclude_strings = ["foot", "MENU", "XEVO"]

    key_dict = dict()
    key_list = list()

    for ml_element in soup.find_all('ml'):
        key_k = ml_element.get('key')
        if any(es in key_k for es in exclude_strings):
            continue
        else:
            key_v = ml_element.get_text()
            # print(key_k, ':', key_v.encode("utf-8"))
            key_dict.update({key_k: key_v})

    for kd_k, kd_v in key_dict.items():
        key_list.append({'Key': kd_k, 'ENG': kd_v, 'ENG2': kd_v})

    return key_list


def output_file(output_list):

    with open('output.csv', 'w', newline='') as csvfile:
        # 定義欄位
        fieldnames = ['Key', 'ENG', 'ENG2']

        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入第一列的欄位名稱
        writer.writeheader()

        # 寫入資料
        for kl in output_list:
            writer.writerow(kl)


if __name__ == "__main__":
    h_string = read_from_source()
    parse_res = parsing_html(h_string)
    output_file(parse_res)
