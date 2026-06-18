import hashlib
import string
import secrets


# convert a hash to binary
def hash_to_bin(s):
    return bin(int(hashlib.sha256(s).hexdigest(), base=16))[2:].zfill(256)


# generate the watermark from a netid
def generate_watermark(netid):
    netidd = netid.encode("ascii")
    return hash_to_bin(netidd)[:16]


# generate coins with a specific prefix
def generate_coins(watermark):
    coins = []
    prefix_seen = {}
    random_bits = ["1", "0"]

    # generate the first coin
    preimage = watermark + "".join(secrets.choice(random_bits) for i in range(48))
    coin_str = hex(int(preimage, 2))[2:]
    coin_byte = bytes.fromhex(coin_str)
    hashed_coin_prefix = hash_to_bin(coin_byte)[:28]
    prefix_seen[hashed_coin_prefix] = []
    prefix_seen[hashed_coin_prefix].append(coin_str)

    Found_four = False

    # generate coins until four with the same prefix are found
    while not Found_four:
        preimage = watermark + "".join(secrets.choice(random_bits) for _ in range(48))
        coin_str = hex(int(preimage, 2))[2:]
        coin_byte = bytes.fromhex(coin_str)
        hashed_coin_prefix = hash_to_bin(coin_byte)[:28]
        if hashed_coin_prefix in prefix_seen:
            prefix_seen[hashed_coin_prefix].append(coin_str)
            if len(prefix_seen[hashed_coin_prefix]) == 4:
                coins = prefix_seen[hashed_coin_prefix]
                Found_four = True
        else:
            prefix_seen[hashed_coin_prefix] = []
            prefix_seen[hashed_coin_prefix].append(coin_str)

    return coins


# forge a watermark
def forge_watermark(watermark):
    all_letters = list(string.ascii_lowercase)
    all_digits = list(string.digits)
    fake_nid_found = ""
    num_letters_choices = list(range(2, 4))
    num_digits_choices = list(range(1, 11))

    # loop until a watermark is found that matches the original watermark
    while True:
        num_letters = secrets.choice(num_letters_choices)
        num_digits = secrets.choice(num_digits_choices)
        fake_nid = "".join(
            secrets.choice(all_letters) for _ in range(num_letters)
        ) + "".join(secrets.choice(all_digits) for _ in range(num_digits))
        fake_nidd = fake_nid.encode("ascii")
        temp_watermark = hash_to_bin(fake_nidd)[:16]
        if temp_watermark == watermark:
            fake_nid_found = fake_nid
            break

    return fake_nid_found


# save the coins to a file
def save_coins(coins):
    with open("coin.txt", "w") as output:
        output.write("\n".join(coins))


# save the forged watermark to a file
def save_forged_watermark(forged_watermark):
    with open("forged-watermark.txt", "w") as output:
        output.write(forged_watermark)


# Main function to run the process
def main(netid):
    watermark = generate_watermark(netid)
    coins = generate_coins(watermark)
    save_coins(coins)
    forged_watermark = forge_watermark(watermark)
    save_forged_watermark(forged_watermark)

netid = "ks2365"
main(netid)
