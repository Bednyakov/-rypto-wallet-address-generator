def identify_blockchain(wallet_address: str) -> str:
    """
    Определяет блокчейн, к которому принадлежит данный адрес кошелька.
    """

    if wallet_address.startswith("1") or wallet_address.startswith("3") or wallet_address.startswith("bc1"):
        return "Bitcoin"
    elif wallet_address.startswith("0x"):
        return "Ethereum"
    elif wallet_address.startswith("T"):
        return "TRON"
    elif wallet_address.startswith("ltc1") or wallet_address.startswith("L"):
        return "Litecoin"
    elif wallet_address.startswith("bnb") or wallet_address.startswith("tbnb"):
        return "Binance Chain"
    elif wallet_address.startswith("r"):
        return "Ripple"
    elif wallet_address.startswith("D"):
        return "Dogecoin"
    else:
        return "Unknown Blockchain"

if __name__ == "__main__":
    print(identify_blockchain("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"))  # Bitcoin
    print(identify_blockchain("0x32Be343B94f860124dC4fEe278FDCBD38C102D88"))  # Ethereum
    print(identify_blockchain("THpYXV6kFjYwgGJ8SuLSPxqPoTxP2m5E8h"))  # TRON
    print(identify_blockchain("ltc1q5rq35jxth9elqktynh0pa78zrfscqpkamr2jge"))  # Litecoin
    print(identify_blockchain("bnb1u4x6uc0g8p34yrsrk5efys5phgm39s9v4l2c56"))  # Binance Chain
    print(identify_blockchain("rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh"))  # Ripple
    print(identify_blockchain("DBXu2kgc3xtvCUWFcxFE3r9hEYgmuaaCyD"))  # Dogecoin
