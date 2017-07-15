# Hashpass & Diceware

Hashpass and Diceware-powered memorable deterministic password generator

# Goals

* Reuse [Hashpass](https://github.com/stepchowfun/hashpass).
* Maintain a stateless algorithm.
* Maintain simplicity such that it can all be reimplemented from memory (except for the wordlist which will hopefully be well-archived on the Internet).
* Implement an easily memorable algorithm for generation of memorable passwords (intended usecase - when Hashpass is not used as a primary password manager but as a failsafe password manager in case that the user loses their stateful password manager database and forgets the service-specific passwords and loses their devices and access to all data).
* Implement both in Python and Javascript & HTML.

# Changes from [Hashpass](https://github.com/stepchowfun/hashpass)

* The html page works in any modern browser.
* The python implementation from [Stephan Boyer's original README](https://github.com/stepchowfun/hashpass/blob/master/README.md) as a standalone Python 3 program.
* Added an algorithm of generating dice numbers. (An algorithm easy enough so as to be easily remembered - really, it's just adding a counter (0, 1, 2, ...) to the key and getting all the digits from the base64 results, ignoring all non-numerical characters, and then ignoring all digits that aren't on a 6-sided dice.)
* Added the [EFF's large diceware wordlist](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt). (Easily retrievable from the Internet.)
* Added automatic conversion of the numbers from the generated dice numbers into [Diceware](https://en.wikipedia.org/wiki/Diceware) words.

# Overview of the Hashpass-powered deterministic diceware algorithm

* Have `domain` and `key` strings as usual (the same as for the original [Hashpass](https://github.com/stepchowfun/hashpass)).
* In loop, increase counter `i` from 0 to 40, and for each `i` value, generate a new result of `Hashpass(domain, key + i.toString())`, concatenate the results.
* From the results, select only digits.
* From the digits, select only digits 1-6 (those allowable on a 6-sided dice).
* Group the digits by 5 (here starts the regular diceware way of generating passwords).
* Find the diceware words for the 5-digit digit groups.
* Print results.
* Around 7 to 12 words are usually found for `i` in (0, 40).
* It is also possible to do this by hand using the existing Hashpass and Diceware implementations, e.g. the [Hashpass](https://play.google.com/store/apps/details?id=se.slackers.hashpass) ([GitHub](https://github.com/bysse/hashpass-android)) and [Diceware](https://play.google.com/store/apps/details?id=com.dougsko.diceware) ([GitHub](https://github.com/dougsko/com.dougsko.diceware)) apps for Android in case of dire need and no access to this repo, as well as it is possible to reimplement the algorithm from memory.
* It is possible to use the intermediate outputs to generate numeric PIN codes (usually `i` in (0, 3) are enough).

# Hashpass

Hashpass is an algorithm originally developed as a [Chrome extension](https://github.com/stepchowfun/hashpass) designed to make passwords less painful. It generates a unique password for every *thing* you use, and you only have to memorize a single secret key and the way you name the *thing*, e.g. a domain, username@domain combination, or something else.

Hashpass is deterministic, meaning that it will always generate the same password for any given site and secret key. It uses a well-known formula to generate the passwords, so you could even compute them yourself.

A key feature of Hashpass is that it's stateless. Hashpass never writes to the file system or makes network requests. There is no password database.

## How Hashpass passwords are generated

Suppose your secret key is `bananas`, and you're signing up for Dropbox. Suppose your login email to Dropbox is example@example.com. Suppose your scheme for combining the username, domain, password version, results in the string `v1:personal:example@example.com@dropbox.com`. You enter that string as a `domain` and your secret key as a `key` to Hashpass. Hashpass combines the current domain name and your secret key with a `/` as follows: `v1:personal:example@example.com@dropbox.com/bananas`. It then computes the [SHA-256 hash](http://en.wikipedia.org/wiki/SHA-2) of that string. Then it hashes it again and again, `2^16` times in total. Finally, it outputs the first 96 bits of the result, encoded as 16 characters in [Base64](http://en.wikipedia.org/wiki/Base64). In this example, the final output is `i3Xv/TwtsEnW3QP7`. This result can be reproduced using the Python script and the HTML & Javascript in the repository.

## How Hashpass-powered Diceware passwords are generated

Let's continue with the example. A counter starting at `0` is appended to your secret key and successive Hashpass passwords are generated:

~~~
$ python3 hashpass.py --diceware-helper --show-key
Domain: v1:personal:example@example.com@dropbox.com
Key: 
Password: i3Xv/TwtsEnW3QP7
counter = 0, key = bananas0, pwd = UzQWe68kSMqxUvq+, numbers = ['6', '8']
counter = 1, key = bananas1, pwd = so2V7R+nlJnBtiaR, numbers = ['2', '7']
counter = 2, key = bananas2, pwd = y7Ck/s/T0s+CAnMK, numbers = ['7', '0']
counter = 3, key = bananas3, pwd = tM1PhxWTtbGutJhe, numbers = ['1']
counter = 4, key = bananas4, pwd = bMHbOmhPtPtxCN6u, numbers = ['6']
counter = 5, key = bananas5, pwd = FbckRsMvjdJRWTEf, numbers = []

...example shortened...

counter = 39, key = bananas39, pwd = v/QSgdbL2+a35KGz, numbers = ['2', '3', '5']
diceware numbers: [6, 2, 1, 6, 2, 1, 2, 3, 3, 2, 5, 1, 2, 1, 1, 4, 6, 4, 6, 6, 1, 3, 4, 1, 6, 5, 4, 1, 1, 6, 2, 4, 4, 3, 2, 3, 5, 1, 5, 2, 2, 6, 2, 5, 3, 3, 2, 2, 4, 3, 5, 4, 2, 5, 3, 6, 3, 4, 2, 1, 1, 2, 3, 5]
diceware numbers by groups of 5:
62162 thing
23325 dining
21146 correct
66134 wager
65411 value
24432 dyslexia
51522 requisite
25332 endurance
43542 paramount
36342 luncheon
1235
~~~

The numbers from the passwords are collected in order, then filtered for only numbers 1-6 (that can appear on ordinary dice), grouped by 5 and searched in the [EFF's large diceware wordlist](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt) just like the [Diceware](https://en.wikipedia.org/wiki/Diceware) algorithm works, except for the lack of physical dice-based randomness. In this case, your deterministic Hashpass-Diceware password might be `thing dining correct wager`.

Note that the number of words in the site-specific generated password should be determined under a different threat model than the length of the master password in that the site-specific generated password can be usually quite short since the services usually limit the number of attempts and usually don't use the password for encryption of local data (except for Mozilla Firefox Sync, Google Chrome sync, etc.).

## Security

If an adversary has your secret key, they have access to all of your accounts.

### Password Complexity

If you use a master key weak enough, it is possible to recover the master key from a generated password. E.g. when an adversary induces you to generate a site-specific password for their site or when they get hold of your password leaked from a site you use ([as some of them are stored in plaintext](https://duckduckgo.com/?q=plaintext+passwords+leaked+site%3Aarstechnica.com) and others are often simply hashed, effectively adding one iteration).

SHA-256 is one of the most widely-used cryptographic hash functions, and is considered unbroken at the time of this writing. However, nothing except computational power prevents an adversary to mount a dictionary-based / brute-force attack to try many possible keys until they get a matching output.

Let's look at possible passwords and try to guess how costly it would be to brute-force such a password.

Copying [the estimate from One Shall Pass readme](https://github.com/maxtaco/oneshallpass), let's assume one hash costs 2\^(-45) USD (that's less than the original estimate, but it is a few years old). Hashpass performs 2\^16 iterations, so one attempt against Hashpass costs 2\^(-29) USD. On average, it is necessary to try only half of the possibilities to find the correct one, so we can continue calculations with 2\^(-29-1) == 2\^(-30).

Say you use a 5-dice diceware password - there are 7776 words in a diceware wordlist for 5 rolls (6\^5). Let's see the prices for individual numbers of words:

* 3-word password (e.g. census usable thicken) - 7776\^3 == ~2\^38.7 possible keys, costing approx. 2\^(-30 + 38.7) == 2\^(8.7) == ~416 USD
* 4-word password (e.g. census usable thicken cricket) - 7776\^4 == ~2\^51.7 possible keys, costing approx. 2\^(-30 + 51.7) == 2\^(21.7) == ~3.4 million USD
* 5-word password (e.g. census usable thicken cricket surreal) - 7776\^5 == ~2\^64.6 possible keys, costing approx. 2\^(-30 + 64.6) == 2\^(34.6) == ~26 billion USD
* 6-word password (e.g. census usable thicken cricket surreal dyslexia) - 7776\^6 == ~2\^77.5 possible keys, costing approx. 2\^(-30 + 77.5) == 2\^(47.5) == ~199 trillion USD

This means that given a hash of a long and random string, an adversary can't recover that original string. However, secret keys produced by humans are not typically long, nor are they perfectly random. They often contain predictable words or phrases. It is therefore crucial to pick a truly random password that is long enough. If you choose a relatively small dictionary, you have to use relatively long password, if you choose from a relatively large dictionary, you can have a relatively shorter password.

Example calculation with a password from the dictionary `/usr/share/dict/words` that has 479 828 words:

* 3-word password (e.g. vacabond vapourized proteida) - 479828\^3 == ~2\^56.6 possible keys, costing approx. 2\^(-30 + 56.6) == 2\^(26.6) == ~101 million USD

It is up to you to pick a key with enough [entropy](http://en.wikipedia.org/wiki/Password_strength#Entropy_as_a_measure_of_password_strength) to defend against attacks. Longer is better. More random is better. Don't use a single word. Definitely don't use `bananas`. Hashpass doesn't limit the size of your secret key—take advantage of this.

A determined attacker might try *all* strings up to some length. This generally takes longer or requires more computational power, but it's not impossible. There are 64 characters in the [base64](https://en.wikipedia.org/wiki/Base64) alphabet. Assume a password is composed of these characters:

* 6-character password (e.g. gy+87f) - 64\^6 == 2\^36 possible keys, costing approx. 2\^(-30 + 36) == 2\^(6) == ~64 USD
* 8-character password (e.g. gy+87fxs) - 64\^8 == 2\^48 possible keys, costing approx. 2\^(-30 + 48) == 2\^(18) == ~262 000 USD
* 12-character password (e.g. gy+87fxs82/b) - 64\^12 == 2\^72 possible keys, costing approx. 2\^(-30 + 72) == 2\^(42) == ~4 trillion USD

**It is strongly advised that you pick a key with at least 10 truly random alphanumeric+symbol characters or with at least 4 truly randomly chosen diceware words or at least 3 truly randomly chosen words from a huge dictionary that has a half a million words.**

### Points of Failure

I'll use [Keepass](http://keepass.info/) as an example for a stateful database-based password manager here.

An adversary needs two things to access a database-based password manager (database, master password) but only one thing to access a stateless password manager (the master password). In this regard, Keepass is much more secure.

With a database-based password manager, it is possible to use information-theoretically independent passwords for each site - an attacker seeing one site password learns nothing about the others. With a stateless password manager, all passwords are tied together (since they are computed from the same master key) and we just hope the link is infeasible to compute. Again, Keepass is much more secure in this regard.

With a database-based password manager, once an adversary gains access, they have a list of all accounts and other things (like passwords to hardware) on a silver platter. With a stateless password manager, the adversary has to either compel the owner to divulge all accounts and usernames etc., or to observe the user's habits to gather such a list, or to brute-force all conceivable services.

## Comparison with traditional password managers

With Hashpass, an adversary with one of your generated passwords can try to guess your secret key and gain access to all your accounts. With a traditional password manager, those with access to your password database can try to guess your master password. These are very different threat models, but it is not obvious which is better. Things to consider under your threat model are methods of attack you want to protect yourself from, and usability fails you want to protect from (e.g. consider a house fire in which all your storage is destroyed, together with your phone, and you also realize you forgot the passwords to your 2FA-protected Google and Dropbox accounts where your last Keepass backups are. You now have practically no way to recover your passwords. Without gaining access to your Google, Dropbox, and Keepass, you can't easily access your bank account, backups of your scanned documents you might suddenly need, communicate with others, etc. Hashpass would help you in this situation.)

Since Hashpass doesn't store passwords in a database, you have no chance of accidentally deleting them, and you don't need to sync them across multiple devices. You also don't have to worry about me abandoning the project, or using a computer that doesn't have Hashpass. Since Hashpass uses a well-known hash function rather than a proprietary password database, you can always compute the passwords yourself if Hashpass is unavailable. All of the information needed to produce your passwords is in your head. That property is what motivated the development of this project.

You are advised to consider combining both password manager approaches so that you reap the benefits of stateful password storage and can recover important passwords through a stateless one. It requires planning and perhaps a regular practice of your chosen passphrase.

## Practical notes

- If a generated password is ever compromised, you don't need to memorize a whole new secret key and update all of your passwords. For that service only, just add an incrementing index to your secret key. Such a tiny change in your secret key results in a completely new password for that service. Continuing with the example `v1:personal:example@example.com@dropbox.com` from the beginning of this readme, you can change it to `v2:personal:example@example.com@dropbox.com`. If you can't remember which iteration of your secret key you used for a particular service, simply try them all in order.

- Some websites have certain requirements on passwords, e.g., at least one number and one capital letter. A simple way to meet such requirements is to append something like `A9!` to the generated password (and remember you did that).

- You don't have to use the same key for every service. But the point of Hashpass is that you can, provided your key is strong enough and you've considered the security implications.

- You can protect yourself from an adversary that monitors one of your devices by having two equally strong (and strong on their own) master passwords and generating the resulting service passwords serially. E.g. running hashpass(`v1:personal:example@example.com@dropbox.com`, `oranges`), resulting in `cra/u98rCbnNqqaI`, and then running hashpass(`v1:personal:example@example.com@dropbox.com`, `cra/u98rCbnNqqaI bananas`), resulting in `+XIu1aONroWnsE0U`, which might be your resulting password for the given service. The key here is to *always* enter the first strong master password (`oranges`) only into one class of devices (e.g. mobile phones, and never to computers), and to enter the second strong master password (`bananas`) only into another class of devices (e.g. computers, and never to mobile phones); one slip-up and the adversary monitoring only one of the devices learns both passwords and can attack you. This is feasible only if you do this seldom, such as in cases when you want to use Hashpass to generate passwords that you ordinarily keep in Keepass but you want to have the possibility to regenerate them in case you lose access to your Keepass.

- As with any good security software, Hashpass is open-source ([Github](https://github.com/SvobodaJakub/hashpass)). The HTML & Javascript version uses the [Stanford Javascript Crypto Library](http://bitwiseshiftleft.github.io/sjcl/) to compute SHA-256.

- The Hashpass scheme is very simple and can be implemented as this Python script:

    ```python
    #!/usr/bin/python2
    import base64, getpass, hashlib

    domain = raw_input('Domain: ').strip().lower()
    key = getpass.getpass('Key: ')

    bits = domain + '/' + key
    for i in range(2 ** 16):
      bits = hashlib.sha256(bits).digest()
    password = base64.b64encode(bits)[:16]

    print('Password: ' + password)
    ```

## License

Copyright (c) 2016 Stephan Boyer
Copyright (c) 2017 Jakub Svoboda

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
