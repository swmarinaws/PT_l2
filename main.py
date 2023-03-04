import random
from russian_names import RussianNames
import pandas as pd
from collections import defaultdict
import timeit

list_faculties = ['Биологический', 'Богословский','Географический', 'Геологический', 'Журналистики', 'Информационный', 'Исторический', 'Кибернетики', 'Математический', 'Механический', 'Политологический', 'Психологический', 'Радиотехнический', 'Социологический', 'Управления', 'Физический', 'Филологический', 'Философский', 'Химический', 'Художественно-графический', 'Экономический', 'Юридический']
list_ranks = ['Доцент', 'Профессор']
list_degrees = ['Кандидат наук', 'Доктор наук']
sizes = [100, 250, 500, 1000, 5000, 10000, 100000]

"""Время поиска"""
time_linear = []
time_binary_sort = []
time_binary = []
time_key = []

def generate(n):
    """Генерирование n данных"""
    final_dict = {}
    names, surnames, patronymics, faculties, ranks, degrees = [], [], [], [], [], []
    for i in range(n):
        full_name = RussianNames().get_person().split()
        names.append(full_name[0])
        patronymics.append(full_name[1])
        surnames.append(full_name[2])
        faculties.append(random.choice(list_faculties))
        ranks.append(random.choice(list_ranks))
        degrees.append(random.choice(list_degrees))

    final_dict['Фамилия'] = surnames
    final_dict['Имя'] = names
    final_dict['Отчество'] = patronymics
    final_dict['Факультет'] = faculties
    final_dict['Учёная степень'] = ranks
    final_dict['Учёное звание'] = degrees
    return final_dict

def quick_sort(l, fst, lst):
    """Быстрая сортировка"""
    if fst >= lst: return

    i, j = fst, lst
    pivot = l[fst + (lst - fst) // 2]

    while i <= j:
        while l[i] < pivot: i += 1
        while l[j] > pivot: j -= 1
        if i <= j:
            l[i], l[j] = l[j], l[i]
            i += 1
            j -= 1

    quick_sort(l, fst, j)
    quick_sort(l, i, lst)

def linear_search(l, key):
    """Прямой поиск"""
    for i in range(len(l)):
        if l[i] == key:
            return i
    return -1

def binary_search(l, start, end, key):
    """Бинарный поиск"""
    if start > end: return -1

    middle = start + (end - start) // 2

    if l[middle] == key:
        return middle
    elif l[middle] > key:
        return binary_search(l, start, middle - 1, key)
    return binary_search(l, middle + 1, end, key)

class Teacher:
    """Класс для описания объекта преподавателя"""
    """Объект включает в себя: фамилию, имя, отчество, факультет, учёное звание, учёную степень"""
    def __init__(self, surname, name, patronymic, faculty, rank, degree):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.faculty = faculty
        self.rank = rank
        self.degree = degree

    def __gt__(self, other):
        """Перегрузка оператора >"""
        if self.faculty != other.faculty:
            return self.faculty > other.faculty
        if self.surname != other.surname:
            return self.surname > other.surname
        if self.name != other.name:
            return self.name > other.name
        if self.patronymic != other.patronymic:
            return self.patronymic > other.patronymic
        if self.degree != other.degree:
            return self.degree > other.degree
        return self.rank > other.rank

    def __lt__(self, other):
        """Перегрузка оператора <"""
        if self.faculty != other.faculty:
            return self.faculty < other.faculty
        if self.surname != other.surname:
            return self.surname < other.surname
        if self.name != other.name:
            return self.name < other.name
        if self.patronymic != other.patronymic:
            return self.patronymic < other.patronymic
        if self.degree != other.degree:
            return self.degree < other.degree
        return self.rank < other.rank

    def __ge__(self, other):
        """Перегрузка оператора >="""
        if self.faculty != other.faculty:
            return self.faculty >= other.faculty
        if self.surname != other.surname:
            return self.surname >= other.surname
        if self.name != other.name:
            return self.name >= other.name
        if self.patronymic != other.patronymic:
            return self.patronymic >= other.patronymic
        if self.degree != other.degree:
            return self.degree >= other.degree
        return self.rank >= other.rank

    def __le__(self, other):
        """Перегрузка оператора <="""
        if self.faculty != other.faculty:
            return self.faculty <= other.faculty
        if self.surname != other.surname:
            return self.surname <= other.surname
        if self.name != other.name:
            return self.name <= other.name
        if self.patronymic != other.patronymic:
            return self.patronymic <= other.patronymic
        if self.degree != other.degree:
            return self.degree <= other.degree
        return self.rank <= other.rank

"""Запись сгенерированных данных в файл MS Excel"""
with pd.ExcelWriter("./sets.xlsx") as writer:
    for i in sizes:
        pd.DataFrame(generate(i)).to_excel(writer, sheet_name=f"{i}", index=False)

"""Считывание входных данных из файла MS Excel и запись в словарь"""
teachers = {}
for i in sizes:
    temp = pd.read_excel('./sets.xlsx', sheet_name=f"{i}").to_dict('records')
    teachers[i] = [Teacher(t['Фамилия'], t['Имя'], t['Отчество'], t['Факультет'], t['Учёная степень'], t['Учёное звание']) for t in temp]

for i in sizes:
    faculties = [k.faculty for k in teachers[i]]
    key = Teacher("", "", "", random.choice(list_faculties), "", "")

    """Поиск по ключу в массиве"""
    teacher_multi_map = defaultdict(list)
    for t in teachers[i]:
        teacher_multi_map[t.faculty].append(t)
    starttime1 = timeit.default_timer()
    print(teacher_multi_map[key.faculty])
    end1 = timeit.default_timer() - starttime1
    time_key.append(end1)

    """Прямой поиск"""
    starttime2 = timeit.default_timer()
    linear_search(teachers[i], key)
    end2 = timeit.default_timer() - starttime2
    time_linear.append(end2)

    """Сортировка массива и бинарный поиск"""
    starttime3 = timeit.default_timer()
    quick_sort(teachers[i], 0, len(teachers[i]) - 1)
    binary_search(teachers[i], 0, len(teachers[i]) -1, key)
    end3 = timeit.default_timer() - starttime3
    time_binary_sort.append(end3)

    """Бинарный поиск"""
    starttime4 = timeit.default_timer()
    binary_search(teachers[i], 0, len(teachers[i]) -1, key)
    end4 = timeit.default_timer() - starttime4
    time_binary.append(end4)

print(f'time_linear = {time_linear}')
print(f'time_binary = {time_binary}')
print(f'time_binary_sort = {time_binary_sort}')
print(f'time_key = {time_key}')