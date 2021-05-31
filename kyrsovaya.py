import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import Radiobutton
from tkinter import messagebox
import hashlib


# Канонизация текста
def canonize(txt):
    stop_symbols = "@^&*$#№%«»©.,!?:;-\n\r()"

    stop_words = ('это', 'как', 'так', 'и', 'в', 'над',
                  'к', 'до', 'не', 'на', 'но', 'за',
                  'то', 'с', 'ли', 'а', 'во', 'от',
                  'со', 'для', 'о', 'же', 'ну', 'вы',
                  'бы', 'что', 'кто', 'он', 'она', 'у',
                  'под', 'по', '<doctype>', '<!-->', '<a>',
                  '<abbr>', '<acronym>', '<base>', '<basefont>',
                  '<big>', '<blockquote>', '<body>', '<br>',
                  '<caption>', '<code>', '<col>', '<colgroup>',
                  '<dd>', '<div>', '<em>', '<font>', '<form>',
                  '<h>', '<head>', '<hr>', '<html>', '<img>',
                  '<input>', '<kbd>', '<li>', '<link>', '<meta>',
                  '<marquee>', '<nobr>', '<ol>', '<option>', '<p>',
                  '<pre>', '<q>', '<samp>', '<select>', '<small>',
                  '<span>', '<strike>', '<strong>', '<style>', '<sub>',
                  '<sup>', '<table>', '<tbody>', '<td>', '<textarea>',
                  '<tfoot>', '<th>', '<thead>', '<title>', '<tr>',
                  '<ul>', '<wbr>', '<u>')

    result = ''
    for x in [y.rstrip('.').strip(stop_symbols) for y in txt.lower().split()]:
        if x and (x not in stop_words):
            result += x + ' '

    return result[:len(result) - 1]


# Вывод канонизированного текста №1
def print_canonize_1():
    txt_1 = txt_entry1.get("1.0", END)
    txt_entry1.delete("1.0", END)
    txt_entry1.insert(END, canonize(txt_1))


# Вывод канонизированного текста №2
def print_canonize_2():
    txt_2 = txt_entry2.get("1.0", END)
    txt_entry2.delete("1.0", END)
    txt_entry2.insert(END, canonize(txt_2))


# Получение длины шингла
def shinglelen():
    shingle_len = int(number.get())
    return shingle_len


# Деление на шинглы с выбором шага(слово или символ)
def step(txt):
    result = []
    k = 0
    le_n = shinglelen()
    if var.get() == 1:
        symbols = [i for i in list(txt) if i != ' ']
        count = len(symbols) / le_n
        if len(symbols) % le_n != 0:
            count += 1
        for i in range(int(count)):
            result.append('')
            for j in range(k, k + le_n):
                if j >= len(symbols):
                    break
                result[i] += symbols[j]
            k += le_n
    if var.get() == 2:
        words = txt.split()
        count = len(words)
        if len(words) % le_n != 0:
            count += 1
        for i in range(int(count)):
            result.append('')
            for j in range(k, k + le_n):
                if j >= len(words):
                    break
                result[i] += words[j]
                if j != k + le_n - 1:
                    result[i] += ' '
            k += 1
    return result


# Вывод шинглов и хешей первого текста
def print_shingle_1():
    txt_1 = txt_entry1.get("1.0", END)
    txt_insert_shingle_1.delete("1.0", END)
    txt_insert_hash_1.delete("1.0", END)
    for i in step(canonize(txt_1)):
        txt_insert_shingle_1.insert(END, i)
        txt_insert_shingle_1.insert(END, '\n')
        # Вывод хешей первого текста
        txt_hash_1 = hashlib.md5(i.encode())
        txt_insert_hash_1.insert(END, txt_hash_1.hexdigest())
        txt_insert_hash_1.insert(END, " ")
        txt_insert_hash_1.insert(END, '\n')


# Вывод шинглов и хешей второго текста
def print_shingle_2():
    txt_2 = txt_entry2.get("1.0", END)
    txt_insert_shingle_2.delete("1.0", END)
    txt_insert_hash_2.delete("1.0", END)
    for i in step(canonize(txt_2)):
        txt_insert_shingle_2.insert(END, i)
        txt_insert_shingle_2.insert(END, '\n')
        # Вывод хешей второго текста
        txt_hash_2 = hashlib.md5(i.encode())
        txt_insert_hash_2.insert(END, txt_hash_2.hexdigest())
        txt_insert_hash_2.insert(END, " ")
        txt_insert_hash_2.insert(END, '\n')


# Рассчёт процента совпадения текстов
def compaire(txt_1, txt_2):
    same = 0
    for i in range(len(txt_1)):
        if txt_1[i] in txt_2:
            same += 1
    percent = same*2 / float(len(txt_1) + len(txt_2)) * 100
    return percent


# Вывод процента совпадения текстов
def payment():
    txt_1 = txt_entry1.get("1.0", END)
    txt_2 = txt_entry2.get("1.0", END)
    txt_encode_1 = hashlib.md5(txt_1.encode("UTF-8"))
    txt_encode_2 = hashlib.md5(txt_2.encode("UTF-8"))
    cmp1 = txt_encode_1.hexdigest()
    cmp2 = txt_encode_2.hexdigest()
    answer = compaire(cmp1, cmp2)
    answer_insert = 'Доля совпадения = {}%'.format(answer)
    messagebox.showinfo(title="Ответ", message=answer_insert)


# Открывает файл №1 для редактирования
def open_file1():
    """Открывает файл для редактирования"""
    txt_entry1.delete("1.0", END)
    filepath = askopenfilename(filetypes=[('Текстовые файлы', '*.txt'), ('All Files', '*.*')], defaultextension='*.txt')
    if not filepath:
        return
    with open(filepath, 'r') as input_file:
        text = input_file.read()
        txt_entry1.insert(tk.END, text)
    window.title(f'Поиск дубликатов текста - {filepath}')


# Открывает файл №2 для редактирования
def open_file2():
    txt_entry2.delete("1.0", END)
    filepath = askopenfilename(filetypes=[('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')], defaultextension='*.txt')
    if not filepath:
        return
    with open(filepath, 'r') as input_file:
        text = input_file.read()
        txt_entry2.insert(tk.END, text)
    window.title(f'Поиск дубликатов текста - {filepath}')


# Сохранение файла №1
def save_file1():
    """Сохраняем текущий файл как новый файл."""
    filepath = asksaveasfilename(
        defaultextension='.txt',
        filetypes=[('Текстовые файлы', '*.txt'), ('Все файлы', '*.*')],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_entry1.get("1.0", tk.END)
        output_file.write(text)
    window.title(f'Поиск дубликатов текста - {filepath}')


# Сохранение файла №2
def save_file2():
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_entry2.get("1.0", tk.END)
        output_file.write(text)
    window.title(f'Поиск дубликатов текста - {filepath}')


# Настройки окна
window = Tk()
window['bg'] = 'light grey'
window.title('Поиск дубликатов текста')
window.geometry('1500x720')
window.wm_attributes('-alpha', 10)
window.resizable(width=False, height=False)
fr = Frame(window, width=500, height=100, bg='black')

# Канонизация
btn_clean1 = tk.Button(text='Канонизация', width=15, command=print_canonize_1)
btn_clean1.place(x=570, y=40)
btn_clean2 = tk.Button(text='Канонизация', width=15, command=print_canonize_2)
btn_clean2.place(x=570, y=400)

# Хеширование
btn_hash = tk.Button(text='Хеширование', width=15, command=print_shingle_1)
btn_hash.place(x=570, y=75)
btn_hash = tk.Button(text='Хеширование', width=15, command=print_shingle_2)
btn_hash.place(x=570, y=435)

# Выбор размера Шага
var = IntVar()
var.set(0)
step1 = Radiobutton(window, text='Символ', variable=var, value=1, cursor="hand2")
step2 = Radiobutton(window, text='Слово', variable=var, value=2, cursor="hand2")
step2.invoke()
step_text = Label(window, text='Ед. кодирования', font=('Times new roman', 12), fg='white', bg='grey')
step_text.place(x=35, y=260)
step1.place(x=35, y=290)
step2.place(x=35, y=315)
number_text = Label(window, text='Количество', font=('Times new roman', 12), fg='white', bg='grey')
number_text.place(x=35, y=350)
number = Spinbox(window, from_=1, to=50, width=8, command=shinglelen)
number.place(x=35, y=380)

# Кнопки("Сохранить как..." и "окрыть...")
btn_open1 = tk.Button(text='Текст 1\n(открыть...)', command=open_file1, fg='black')
btn_save1 = tk.Button(text='Текст 1\n(сохранить как...)', command=save_file1, fg='black')
btn_open2 = tk.Button(text='Текст 2\n(открыть...)', command=open_file2, fg='black')
btn_save2 = tk.Button(text='Текст 2\n(сохранить как...)', command=save_file2, fg='black')
btn_open1.place(x=35, y=45)
btn_open2.place(x=35, y=96)
btn_save1.place(x=12, y=147)
btn_save2.place(x=12, y=198)

# Окна ввода
label = Label(window, text='Текст №1:', font=('Times new roman', 12), fg='white', bg='grey')
label.place(x=330, y=10)
label = Label(window, text='Текст №2:', font=('Times new roman', 12), fg='white', bg='grey')
label.place(x=330, y=370)
txt_entry1 = scrolledtext.ScrolledText(window)
txt_entry2 = scrolledtext.ScrolledText(window)
txt_entry1.place(width=340, height=300, x=200, y=40)
txt_entry2.place(width=340, height=300, x=200, y=400)

# Окна вывода шинглов
label_1 = Label(window, text='Шинглы:', font=('Times new roman', 12), fg='white', bg='grey')
label_2 = Label(window, text='Шинглы:', font=('Times new roman', 12), fg='white', bg='grey')
txt_insert_shingle_1 = scrolledtext.ScrolledText(window, bg='#757575', bd=2)
txt_insert_shingle_2 = scrolledtext.ScrolledText(window, bg='#757575', bd=2)
txt_insert_shingle_1.place(width=460, height=300, x=745, y=40)
txt_insert_shingle_2.place(width=460, height=300, x=745, y=400)
label_1.place(x=940, y=10)
label_2.place(x=940, y=370)

# Окна вывода хешей
label_1 = Label(window, text='Хеши:', font=('Times new roman', 12), fg='white', bg='grey')
label_2 = Label(window, text='Хеши:', font=('Times new roman', 12), fg='white', bg='grey')
txt_insert_hash_1 = scrolledtext.ScrolledText(window, bg='#757575', bd=2)
txt_insert_hash_2 = scrolledtext.ScrolledText(window, bg='#757575', bd=2)
txt_insert_hash_1.place(width=285, height=300, x=1210, y=40)
txt_insert_hash_2.place(width=285, height=300, x=1210, y=400)
label_1.place(x=1325, y=10)
label_2.place(x=1325, y=370)

# Другое...
label = Label(window, text='ПАРАМЕТРЫ:', font=('Times new roman', 12), fg='white', bg='grey')
label.place(x=35, y=15)
btn_ans = tk.Button(text='РАССЧИТАТЬ', width=18, height=3, bg='green2', command=payment)
btn_ans.place(x=15, y=500)

window.mainloop()
