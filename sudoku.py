import pathlib # Модуль для работы с путями к файлам
import typing as tp # Типы данных для аннотации к функциям
from itertools import islice # Итерации
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    #Функция открывает файл, читает его содержимое и затем передает его в функцию create_grid для создания Судоку-сетки
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    # Функция создает из строки с цифрами и точками двумерный список (сетку) размером 9х9
    digits = [c for c in puzzle if c in "123456789."] # Список цифр и точек из строки puzzle
    grid = group(digits, 9) # Разбиение на подсписки длиной 9
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    # Функция выводит Судоку на экран, создавая сетку, разделяя ячейки и блоки горизонтальными и вертикальными линиями
    width = 2 # Ширина ячейки
    line = "+".join(["-" * (width * 3)] * 3) # Горизонтальная линия разделения между квадратами
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9) # Каждый символ ставится в центр ячейки. И каждые 3 столбца добавляется вертикальная черта
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    # Функция разбивает список на списки размера n
    return [values[i:i+n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    # Возвращает все значения для номера строки, указанной в pos
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    # Возвращает все значения для номера столбца, указанного в pos
    return [grid[i][pos[1]] for i in range(len(grid))]   

def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    # Возвращает все значения из квадрата 3x3, в который попадает позиция pos
    row, col = pos # pos - кортеж из двух целых чисел (строка и столбец)
    start_row, start_col = 3 * (row // 3), 3 * (col // 3) # Вычисление начальной координаты (верхний левый угол), в котором лежит pos. Деление\Умножение на 3 - для округления для ближайшего кратного 3
    return [grid[start_row+i][start_col+j] for i in range(3) for j in range(3)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    # Найти первую свободную позицию в пазле
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    # Функция, вовзращающая множество возможных значения для указанной позиции
    row_vals = set(get_row(grid, pos)) # Все значения строки, находящейся в позиции pos
    col_vals = set(get_col(grid, pos)) # Аналогично - столбца
    block_vals = set(get_block(grid, pos)) # Все значения квадрата, в который попадает позиция pos
    return set(str(i) for i in range(1, 10)) - row_vals - col_vals - block_vals # Множество, содержащее все значения, кроме row_vals и col_vals


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    # Решение пазла, заданного в grid (рекурсивная функция)
    empty_pos = find_empty_positions(grid) # Нахождение первой свободной свободной позиции в сетке и ее координат
    if not empty_pos: # Проверка: есть ли еще свободные позиции
        return grid
    else:
        row, col = empty_pos
        possible_values = find_possible_values(grid, empty_pos) # Множество возможных значений для текущей свободной позиции
        for value in possible_values:
            grid[row][col] = value
            solution = solve(grid)
            if solution:
                return solution
            grid[row][col] = '.'  
        return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    # Если решение solution верно, то вернуть True, в противном случае False 
    # Функция, проверяющая, является ли корректным полученное решение
    if not solution:
        return False
    for i in range(9):
        for j in range(9):
            if solution[i][j] == '.':
                return False
            if solution[i].count(solution[i][j]) > 1:
                return False
            if [solution[k][j] for k in range(9)].count(solution[i][j]) > 1:
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    
    # Сгенерируем полностью заполненное судоку
    filled_sudoku = solve([['.' for _ in range(9)] for _ in range(9)])

    # Определим количество пустых элементов для генерации
    empty_count = 81 - N

    # Создадим копию полностью заполненного судоку
    sudoku = [row[:] for row in filled_sudoku]

    # Случайным образом заменим некоторые элементы на пустые места
    while empty_count > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)

        # Проверим, что ячейка не пустая
        if sudoku[row][col] != '.':
            # Заменим элемент на пустое место
            sudoku[row][col] = '.'
            empty_count -= 1

    return sudoku











# Блок используется для тестирования кода.

# Проходится по пазлам в файлах, отображает их и пытается решить.
# Если решение не существует, выводит сообщение.
if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)