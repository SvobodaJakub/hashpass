#!/usr/bin/python3
import base64, getpass, hashlib, sys

# TODO parse arguments properly
# TODO docstring and documentation
# TODO proper help with --help argument

if len(sys.argv) >= 2 and sys.argv[1] in ["--help", "-h", "/?"]:
    print("hashpass.py [--diceware-helper [--show-key]]")
    exit(0)

domain = input('Domain: ').strip().lower()
key = getpass.getpass('Key: ')

def com(domain, key):
    bits = domain + '/' + key
    bits = bytes(bits, "utf8")
    for i in range(2 ** 16):
        bits = hashlib.sha256(bits).digest()
    password = base64.b64encode(bits)[:16]
    password = str(password, "utf8")
    return password

password = com(domain, key)
print('Password: ' + password)

if len(sys.argv) >= 2 and sys.argv[1] == "--diceware-helper":
    all_dice_nums = []
    for i in range(40):
        key_i = "{}{}".format(str(key), str(i))
        passwd_i = com(domain, key_i)
        num_in_passwd_i = [x for x in passwd_i if x.isdigit()]
        dice_nums = [int(x) for x in num_in_passwd_i if int(x) <= 6 and int(x) > 0]
        all_dice_nums += dice_nums
        if len(sys.argv) >= 3 and sys.argv[2] == "--show-key":
            print("counter = {}, key = {}, pwd = {}, numbers = {}".format(str(i), key_i, passwd_i, str(num_in_passwd_i)))
        else:
            print("counter = {}, pwd = {}, numbers = {}".format(str(i), passwd_i, str(num_in_passwd_i)))
    print("diceware numbers: {}".format(str(all_dice_nums)))
    print("diceware numbers by groups of 5:")

    diceware_word_dict = {}
    DICEWARE_FILE_NAME = "eff_large_wordlist.txt"
    try:
        with open(DICEWARE_FILE_NAME, "r") as f:
            for line in f:
                number, word = line.split()
                diceware_word_dict[number] = word
    except:
        print("Problem accessing {}".format(DICEWARE_FILE_NAME))

    curr_group = ""
    words = []
    def print_curr_group(curr_group):
        if curr_group in diceware_word_dict:
            print("{} {}".format(curr_group, diceware_word_dict[curr_group]))
            words.append(diceware_word_dict[curr_group])
        else:
            print(curr_group)

    for i in all_dice_nums:
        if len(curr_group) < 5:
            curr_group += str(i)
        else:
            print_curr_group(curr_group)
            curr_group = ""
    if curr_group:
        print_curr_group(curr_group)

    print(" ".join(words))


