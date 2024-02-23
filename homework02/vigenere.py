def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""  # Инициализируем пустую строку для хранения зашифрованного текста
    keyword = keyword.upper()  # Преобразуем ключ к верхнему регистру для удобства
    key_length = len(keyword)  # Вычисляем длину ключа
    for i, char in enumerate(plaintext):  # Проходим по каждому символу в открытом тексте с использованием индекса i
        if char.isalpha():  # Проверяем, является ли символ буквой
            shift = ord(keyword[i % key_length]) - ord('A')  # Определяем сдвиг для текущего символа ключа
            # Шифруем символ, учитывая регистр
            shifted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A')) if char.isupper() else chr(
                (ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext += shifted_char  # Добавляем зашифрованный символ к строке зашифрованного текста
        else:
            ciphertext += char  # Если символ не буква, добавляем его как есть
    return ciphertext  # Возвращаем зашифрованный текст


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""  # Инициализируем пустую строку для хранения расшифрованного текста
    keyword = keyword.upper()  # Преобразуем ключ к верхнему регистру для удобства
    key_length = len(keyword)  # Вычисляем длину ключа
    for i, char in enumerate(ciphertext):  # Проходим по каждому символу в зашифрованном тексте с использованием индекса i
        if char.isalpha():  # Проверяем, является ли символ буквой
            shift = ord(keyword[i % key_length]) - ord('A')  # Определяем сдвиг для текущего символа ключа
            # Расшифровываем символ, учитывая регистр
            shifted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A')) if char.isupper() else chr(
                (ord(char) - ord('a') - shift) % 26 + ord('a'))
            plaintext += shifted_char  # Добавляем расшифрованный символ к строке расшифрованного текста
        else:
            plaintext += char  # Если символ не буква, добавляем его как есть
    return plaintext  # Возвращаем расшифрованный текст
