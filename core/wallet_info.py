btc_text = \
"""
Среди форматов адресов Bitcoin наиболее популярны следующие:

1. P2PKH (Pay to Public Key Hash): Эти адреса начинаются с цифры 1. Это самый старый и распространенный формат адресов. Пример: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.

2. P2SH (Pay to Script Hash): Адреса этого типа начинаются с цифры 3. Они используются для мультиподписных кошельков и других скриптовых функций. Пример: 3EktnHQD7RiAE6uzMj2ZifT9YgRrkSgzQX.

3. Bech32 (SegWit): Адреса в формате Bech32 начинаются с bc1. Они представляют собой новый формат, который более эффективен и обеспечивает меньшие комиссии за транзакции. Пример: bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4.

На сегодняшний день, все три формата широко используются, но Bech32 постепенно становится более популярным из-за преимуществ SegWit, таких как уменьшение комиссий и повышение безопасности.

"""

eth_text = \
"""
На платформе Ethereum существует несколько типов адресов, которые используются для различных целей. Вот основные из них:

1. Публичные адреса: Это адреса, которые используются для отправки и получения транзакций. Они могут быть представлены в виде строки из 40 шестнадцатеричных символов, начинающихся с "0x". Программа генерирует именно их.

2. Приватные ключи: Это секретные ключи, которые используются для подписания транзакций и доступа к счету. Они обычно представлены в виде строки из 64 шестнадцатеричных символов.

3. Мультискооперативные адреса (Multisig addresses): Эти адреса требуют подписей от нескольких участников для выполнения транзакций. Они обеспечивают дополнительный уровень безопасности.

4. Контрактные адреса: Это адреса, которые принадлежат смарт-контрактам на платформе Ethereum. Смарт-контракты могут взаимодействовать с другими контрактами и пользователями.

На адрес Ethereum можно отправлять любые токены, которые созданы на базе Ethereum блокчейна, включая ERC-20 и ERC-721 токены. 
Важно убедиться, что токен, который вы хотите отправить, поддерживает стандарты Ethereum и совместим с вашим кошельком или платформой.

"""
tron_text = \
"""
На блокчейне TRON существует несколько типов адресов, каждый из которых имеет свои особенности и предназначение:

Публичные адреса: Эти адреса используются для отправки и получения транзакций TRX. Они и создаются с помощью этой программы.

Контрактные адреса: Эти адреса используются для управления контрактами на платформе TRON. Контракты могут выполнять различные функции, такие как автоматизация бизнес-процессов или создание децентрализованных приложений (DApps).

Административные адреса: Эти адреса принадлежат администраторам и управляющим сети TRON. Они используются для управления сетью и внесения изменений в её конфигурацию.

Системные адреса: Эти адреса используются для внутреннего управления сетью TRON и обеспечения её стабильности и безопасности.

"""


litecoin_text = \
"""
Litecoin (LTC) - это децентрализованная криптовалюта, созданная Чарли Ли в 2011 году. Она была разработана как "облегченная" версия Bitcoin, отсюда и название "Litecoin". Цель Litecoin заключается в том, чтобы предложить более быстрые подтверждения транзакций и низкие комиссии по сравнению с Bitcoin. Litecoin использует другой алгоритм хеширования, называемый Scrypt, который предназначен для большей доступности для индивидуальных майнеров.

Что касается типов адресов, используемых в Litecoin, существует два основных типа:

Legacy (устаревшие) адреса: Это оригинальные адреса, используемые в Litecoin, которые начинаются с буквы "L". Они основаны на том же формате, что и адреса Bitcoin.

Адреса Segregated Witness (SegWit): Эти адреса начинаются с буквы "ltc1" и являются обновленной версией, которая позволяет более эффективно проводить транзакции и улучшать масштабируемость.

"""