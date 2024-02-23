import random
import typing as tp


def is_prime(n: int) -> bool:
    """
    Tests to see if a number is prime.

    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if n <= 1: # Если число меньше или равно 1, то оно не является простым
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n: # Проверяем делители до корня из числа
        if n % i == 0:  # Если число делится на i, то оно не простое
            return False
        i += 2 # Переходим к следующему нечетному числу
    return True

def gcd(a: int, b: int) -> int:
    """
    Euclid's algorithm for determining the greatest common divisor.

    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while b != 0: # Применяем алгоритм Евклида для нахождения НОД
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.

    >>> multiplicative_inverse(7, 40)
    23
    """
    x1, x2 = phi, e # Инициализируем переменные для расширенного алгоритма Евклида
    y1, y2 = 0, 1
    while x2: # Применяем расширенный алгоритм Евклида
        q = x1 // x2
        x1, x2 = x2, x1 - q * x2
        y1, y2 = y2, y1 - q * y2
    return y1 if y1 >= 0 else y1 + phi # Возвращаем мультипликативный обратный элемент (может быть отрицательным)


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)): # Проверяем, что оба числа являются простыми
        raise ValueError("Both numbers must be prime.") # Исключение, если не оба числа простые
    elif p == q:
        raise ValueError("p and q cannot be equal") # Исключение, если оба числа равны

    # Calculate n
    n = p * q

    # Calculate phi
    phi = (p - 1) * (q - 1)

    # Вычисляем значение функции Эйлера для n
    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1: # Проверяем, что e и phi(n) взаимно просты
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n)) # Возвращаем открытый и закрытый ключи в виде кортежа


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    key, n = pk # Распаковываем открытый ключ
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher  # Возвращаем массив чисел


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    key, n = pk # Распаковываем закрытый ключ
    plain = [chr((char ** key) % n) for char in ciphertext] # Расшифровываем каждый символ закрытым ключом
    return "".join(plain) # Возвращаем расшифрованный текст как строку



if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
