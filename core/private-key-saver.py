from cryptography.fernet import Fernet

# Генерация ключа для шифрования
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Шифрование приватного ключа
encrypted_private_key = cipher.encrypt(private_key.encode())
print(f"Зашифрованный приватный ключ: {encrypted_private_key}")

# Расшифровка приватного ключа
decrypted_private_key = cipher.decrypt(encrypted_private_key).decode()
print(f"Расшифрованный приватный ключ: {decrypted_private_key}")
