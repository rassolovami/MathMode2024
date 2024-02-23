import string
import typing as tp

def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""  # Инициализируем переменную для хранения зашифрованного текста
    for char in plaintext: 
        if char.isalpha():  # Проверяем, является ли символ буквой
            # Определение регистра символа (верхний или нижний)
            is_upper = char.isupper()
            # Применение шифра Цезаря к символу
            shifted_char = chr((ord(char) - ord('A' if is_upper else 'a') + shift) % 26 + ord('A' if is_upper else 'a'))
            ciphertext += shifted_char  # Добавляем зашифрованный символ к результату
        else:
            # Если символ не буква, оставить его без изменений
            ciphertext += char  # Добавляем символ без изменений к результату
    return ciphertext  # Возвращаем зашифрованный текст

def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    # Дешифрование аналогично шифрованию с отрицательным сдвигом
    return encrypt_caesar(ciphertext, -shift)  # Используем отрицательный сдвиг для дешифрования

def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0  # Инициализируем лучший сдвиг
    max_valid_words = 0  # Инициализируем максимальное количество валидных слов

    for shift in range(26):  # Пробуем все возможные сдвиги (0-25)
        decrypted_text = decrypt_caesar(ciphertext, shift)  # Дешифруем текст с текущим сдвигом
        valid_words = sum(word.lower() in dictionary for word in decrypted_text.split())  # Считаем количество валидных слов в тексте
        if valid_words > max_valid_words:  # Если текущий сдвиг дал больше валидных слов, чем предыдущий лучший
            max_valid_words = valid_words  # Обновляем максимальное количество валидных слов
            best_shift = shift  # Обновляем лучший сдвиг

    return best_shift  # Возвращаем лучший сдвиг

