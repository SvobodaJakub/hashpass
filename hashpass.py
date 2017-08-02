#!/usr/bin/python3
"""
Hashpass password generator and deterministic Diceware password generator.
See readme for more information
https://github.com/SvobodaJakub/hashpass

License

Copyright (c) 2016 Stephan Boyer

Copyright (c) 2017 Jakub Svoboda

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import base64, getpass, hashlib, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--diceware-helper", help="Generate deterministic Diceware-like passwords from the EFF's Large Wordlist", action="store_true")
parser.add_argument("-d", "--domain", help="The domain input into the Hashpass algorithm")
parser.add_argument("-k", "--key", help="The key input into the Hashpass algorithm. Alternatively, you can provide it through pipe if you provide domain through argument and specify --show-key to enable stdin.")
parser.add_argument("-s", "--show-key", help="Show key during processing, enables normal stdin input for key.", action="store_true")
parser.add_argument("-b", "--silent", help="Do not output anything except the last result (Hashpass password or Diceware password). In scripts, it is best used with -d provided by argument and key provided through pipe.", action="store_true")


args = parser.parse_args()

if args.domain:
    domain = args.domain
else:
    if args.silent:
        domain = input().strip().lower()
    else:
        domain = input('Domain: ').strip().lower()

if args.key:
    key = args.key
else:
    if args.show_key:
        if args.silent:
            key = input().strip()
        else:
            key = input('Key: ').strip()
    else:
        if args.silent:
            key = getpass.getpass()
        else:
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
if args.silent:
    if not args.diceware_helper:
        print(password)
else:
    print('Password: ' + password)

if args.diceware_helper:
    all_dice_nums = []
    for i in range(40):
        key_i = "{}{}".format(str(key), str(i))
        passwd_i = com(domain, key_i)
        num_in_passwd_i = [x for x in passwd_i if x.isdigit()]
        dice_nums = [int(x) for x in num_in_passwd_i if int(x) <= 6 and int(x) > 0]
        all_dice_nums += dice_nums
        if not args.silent:
            if args.show_key:
                print("counter = {}, key = {}, pwd = {}, numbers = {}".format(str(i), key_i, passwd_i, str(num_in_passwd_i)))
            else:
                print("counter = {}, pwd = {}, numbers = {}".format(str(i), passwd_i, str(num_in_passwd_i)))
    if not args.silent:
        print("diceware numbers: {}".format(str(all_dice_nums)))
        print("diceware numbers by groups of 5:")

    diceware_word_dict = {}
    DICEWARE_FILE_NAME = "eff_large_wordlist.txt"
    try:
        program_path = os.path.dirname(__file__)
        diceware_full_path = os.path.join(program_path, DICEWARE_FILE_NAME)
        with open(diceware_full_path, "r") as f:
            for line in f:
                number, word = line.split()
                diceware_word_dict[number] = word
    except:
        if not args.silent:
            print("Problem accessing {}".format(diceware_full_path))
        else:
            exit(2)

    curr_group = ""
    words = []
    def print_curr_group(curr_group):
        if curr_group in diceware_word_dict:
            if not args.silent:
                print("{} {}".format(curr_group, diceware_word_dict[curr_group]))
            words.append(diceware_word_dict[curr_group])
        else:
            if not args.silent:
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


