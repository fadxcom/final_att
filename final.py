import re
import tkinter
import tkinter as tk
from tkinter import ttk
import random
import timeit
import tkinter.messagebox as mb


# Создаем класс
class AppTk(tk.Tk):
    # Инициализация класса
    def __init__(self):
        # Запускаем многоуровневое наследование
        super().__init__()

        # Меню выпадающего списка
        combobox_menu = ['Пузырьковая', 'Выборка', 'Вставка', 'Функция sort']
        # Переменная, опеределяющая количество создаваемых чисел в последовательности
        random_default_count = '100'
        # Максимальное число для генерации последовательности
        self.random_range = 100000
        # Функция вывода данных в поле ввода количества
        self.random_count_int = tk.StringVar()
        # Функция добавления переменной в статус бар, где отображается время выполнения
        self.update_sbar = tk.StringVar()

        # Указываем название окна и его размеры
        self.title("Итоговая аттестация. Сортировка с tkinter")
        self.geometry('600x520')

        # Создаем кнопки
        btn_run = tk.Button(self, text='Запустить', command=self.run_sort)
        btn_clear = tk.Button(self, text='Очистить', command=self.run_clear)
        btn_gen = tk.Button(self, text='Сгенерировать', command=self.gen_values)

        # Создаем текстовые метки
        self.lable_input = tk.Label(self, text="Введите последовательность чисел через запятую:", font=("Arial", 8))
        lable_check = tk.Label(self, text="Введите тип сортировки:", font=("Arial", 8))
        lable_random = tk.Label(self, text="Количество чисел:", font=("Arial", 8))
        lable_result = tk.Label(self, text="Рузельтат:", font=("Arial", 8))

        # Создаем поля дя ввода данных
        self.entry_input = tk.Entry(self)
        self.entry_random = tk.Entry(self, textvariable=self.random_count_int)

        # Передаем в поле ввода количества чисел значение по умолчанию
        self.random_count_int.set(random_default_count)

        # Создаем поле для вывода данных
        self.txt_out = tk.Text(self, borderwidth=2, font=("Arial", 10), wrap=tk.WORD)

        # Создаем статус бар, где будет выводится затраченное время
        self.lable_sbar = tk.Label(self, textvariable=self.update_sbar, relief=tkinter.SUNKEN, anchor="w")

        # Создаем выпадающий список, и выбираем для отображения по-умолчанию первую строку
        self.combobox = ttk.Combobox(self, values=combobox_menu, font=("Arial", 8), state='readonly')
        self.combobox.current(0)

        # С помощью метода place опеределяем место на форме для ранее созданных виджетов
        self.lable_input.place(height=25, width=270, x=10, y=10)
        lable_check.place(height=25, width=130, x=10, y=65)
        lable_random.place(height=25, width=130, x=235, y=65)
        lable_result.place(height=25, width=55, x=10, y=130)
        self.entry_input.place(height=25, width=580, x=10, y=35)
        btn_run.place(height=25, width=100, x=480, y=90)
        btn_clear.place(height=25, width=100, x=480, y=465)
        self.entry_random.place(height=25, width=100, x=250, y=90)
        btn_gen.place(height=25, width=100, x=360, y=90)
        self.txt_out.place(height=300, width=580, x=10, y=155)
        self.combobox.place(height=25, width=130, x=10, y=90)
        self.lable_sbar.place(height=25, width=600, x=0, y=495)

    # Функция для очистки поля вывода
    def run_clear(self):
        self.txt_out.delete(1.0, tkinter.END)

    # Функция для генерации последовательности
    def gen_values(self):
        # С помощью random.sample генерируем список с числами
        list_gen = random.sample(range(self.random_range), k=int(self.entry_random.get()))

        # Список был сделан с целыми числами (int), переводим их в строку
        str_gen = ','.join(str(x) for x in list_gen)

        # Удаляем старое значение из поля ввода последовательности, и вставляем новое значение str_gen
        self.entry_input.delete(0, tkinter.END)
        self.entry_input.insert(tkinter.END, str_gen)

    # Функция сортировки "Пузырьками"
    def run_sort_bubble(self):
        waint = True
        while waint:
            waint = False

            # Сравниваем значения первого и следующего числа в последовательности.
            # Если первое больше, то меняем оба местами
            for i in range(len(self.to_list) - 1):
                if self.to_list[i] > self.to_list[i + 1]:
                    self.to_list[i], self.to_list[i + 1] = self.to_list[i + 1], self.to_list[i]
                    waint = True

        # Выводим данные в поле вывода
        self.txt_out.insert(tkinter.END, self.to_list)

    # Функция сортировки, использующая встроенную функцию sorted()
    def run_sort_func_sort(self):
        new_list = sorted(self.to_list)
        self.txt_out.insert(tkinter.END, new_list)

    # Функция сортировки методом вставки
    def run_sort_insert(self):
        new_list = self.to_list
        # Делем список на 2 части. Если второй элемент списка больше первого, то отавляем его на место, иначе меняем
        # их местами. Перемещаем большие элементы во вторую часть списка.
        for i in range(1, len(new_list)):
            item = new_list[i]
            y = i - 1
            while y >= 0 and new_list[y] > item:
                new_list[y + 1] = new_list[y]
                y -= 1
            new_list[y + 1] = item

        # Выводим список в поле вывода
        self.txt_out.insert(tkinter.END, new_list)

    # Функция сортировки методом выборки
    def run_sort_query(self):
        new_list = self.to_list

        # Делим список на две части, если каждое следующее значение меньше пердыдущего,
        # то это значение переезжает в начало списка.
        for i in range(len(new_list)):
            index = i
            for j in range(i + 1, len(new_list)):
                if new_list[j] < new_list[index]:
                    index = j
            new_list[i], new_list[index] = new_list[index], new_list[i]
        self.txt_out.insert(tkinter.END, new_list)

    # Функция обработки при нажатии на кнопку Запустить
    def run_sort(self):
        # Присваеваем новому списку значения из поля ввода, в котором указана последовательность
        self.to_list = self.entry_input.get()
        check_entry_random = self.entry_random.get()

        # Проверяем, есть что то в списке
        if len(self.to_list) > 0 or len(check_entry_random) > 0:

            # Если есть, то с помощью регулярного выражения проверяем совпадает ли оно с введенной последовательностью
            if re.search(r'^[\d+,?]+[\d]+$', self.to_list):

                # Если собпадает, то преобразуем значения в списке из строковых в числовые
                self.to_list = list(map(int, self.to_list.split(',')))

                # Удаляем старые значения из поля вывода
                self.txt_out.delete(1.0, tkinter.END)

                # Запоминаем время начала сортировки
                start_time = timeit.default_timer()

                # В зависимости от выбранного значения в выпадающем списке срабатывает своя функция сортировки
                if self.combobox.get() == 'Пузырьковая':
                    self.run_sort_bubble()
                elif self.combobox.get() == 'Функция sort':
                    self.run_sort_func_sort()
                elif self.combobox.get() == 'Вставка':
                    self.run_sort_insert()
                elif self.combobox.get() == 'Выборка':
                    self.run_sort_query()

                # вычисляем время выполения
                run_time = timeit.default_timer() - start_time

                # Округляеем до 4х символов после запятой
                run_time = round(run_time, 4)

                # Подготавливаем строку с выполнением
                run_time = 'Выполненно за: ' + str(run_time)

                # Отправляем в статус бар
                self.update_sbar.set(run_time)

            else:

                # Если не вводимые данные не совпадают с регулярным выражением
                mess = 'Вводимые данные не подходят под условие. Должны быть целые числа, '
                mess = mess + 'введенные через запятую или используйте кнопку "Сгенерировать".'

                # Выводим окно с ошибкой
                mb.showwarning(title="Ошибка", message=mess)
        else:

            # Если в поле ввода нет данных
            mess = 'Поле ввода не может быть пустым. '
            mess = mess + 'Должны быть целые числа, введенные через запятую или используйте кнопку "Сгенерировать".'

            # Выводим окно с ошибкой
            mb.showwarning(title="Ошибка", message=mess)


# Запуск программы
my_app = AppTk()
my_app.mainloop()
