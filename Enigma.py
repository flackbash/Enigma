import doctest
import random


class Enigma():
    """Implementation of the Enigma cipher machine as used by the Germans during
    World War II.
    """

    def __init__(self, num_walzen=3, random=False, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        self.__num_walzen = num_walzen
        self.__base = alphabet[0] * num_walzen
        self.__alphabet = alphabet
        self.__walzen = [alphabet for i in range(num_walzen)]
        self.__umkehrwalze = alphabet
        self.__steckerbrett = []
        self.__ringkerben = [len(alphabet) for i in range(num_walzen)]
        if random:
            for i in range(num_walzen):
                self.set_walze(i)
            self.set_umkehrwalze()
            self.set_steckerbrett()
            self.set_ringkerben()

    def set_walze(self, num, walze=0):
        """Generates a random Walze or sets the Walze to the given value.

        Arguments:
        num -- position of the Walze which is to be generated (an integer)
        walze -- the Walze (a string containing each character of the alphabet
                 exactly once)
        """
        if walze == 0:
            # generate a random Walze
            walze = ''.join(random.sample(self.__alphabet, len(self.__alphabet)))
        else:
            # check whether the given Walze is valid
            if len(self.__alphabet) != len(walze):
                raise InputError(walze)
            for char in self.__alphabet:
                if char not in walze:
                    raise InputError(walze)
        self.__walzen[num] = walze

    def set_umkehrwalze(self, walze=0):
        """Generates a random Umkehrwalze (randomly switches each letter with
        another one) or sets the Walze to the given value.

        Arguments:
        walze -- Umkehrwalze (a string containing each character of the
                 alphabet exactly once)
        """
        if walze == 0:
            # generate a random Umkehrwalze
            residual = self.__alphabet
            uncle_walter = list(self.__alphabet)
            while residual != '':
                tupl = ''.join(random.sample(residual, 2))
                residual = residual.replace(tupl[0], '')
                residual = residual.replace(tupl[1], '')
                index_a = self.__alphabet.index(tupl[0])
                index_b = self.__alphabet.index(tupl[1])
                uncle_walter[index_a] = tupl[1]
                uncle_walter[index_b] = tupl[0]
            self.__umkehrwalze = ''.join(uncle_walter)
        else:
            # check whether the given Walze is valid
            if len(self.__alphabet) != len(walze):
                raise InputError(walze)
            for char in self.__alphabet:
                if char not in walze:
                    raise InputError(walze)
            for char in walze:
                if self.__alphabet[self.__alphabet.index(char)] != char:
                    raise InputError(walze)
            self.__umkehrwalze = walze

    def set_steckerbrett(self, steckerbrett=0, number=10):
        """Sets the Steckerbrett to the given value or generates a random
        Steckerbrett (randomly computes <number> pairs of letters, where each
        letter appears only once) if no Steckerbrett is given.

        Arguments:
        steckerbrett -- the Steckerbrett (a list of two-character strings)
        number -- number of pairs to be computed (an integer)
        """
        if steckerbrett == 0:
            # generate a random Steckerbrett
            residual = self.__alphabet
            steckerbrett = []
            while residual != '' and len(steckerbrett) < number:
                tupl = ''.join(random.sample(residual, 2))
                residual = residual.replace(tupl[0], '')
                residual = residual.replace(tupl[1], '')
                steckerbrett.append(tupl)
        else:
            # check whether the given Steckerbrett is valid
            sb = ''.join(steckerbrett)
            for i, char in enumerate(sb):
                if char not in self.__alphabet or char in sb[i+1:]:
                    raise InputError(steckerbrett)
        self.__steckerbrett = steckerbrett

    def set_ringkerben(self, rk=[]):
        """Sets the Ringkerben for all Walzen, indicating on which letter the
        next Walze rotates (the last one has no meaning but is left in here
        for historical reasons).

        Arguments:
        rk -- the Ringkerben for each Walze (a list of integers between 1 and 26)
        """
        if rk == []:
            # generate random Ringkerben
            rk = [0, 0, 0]
            for i in range(self.__num_walzen):
                rk[i] = random.randint(1, 26)
        else:
            # check whether the given Ringkerben are valid
            if len(rk) != self.__num_walzen:
                raise InputError(rk)
            for i in rk:
                if i < 1 or i > 26:
                    raise InputError(rk)
        self.__ringkerben = rk

    def set_base(self, base):
        """Sets the base for all Walzen, that is the initial position of the
        Walzen.

        Arguments:
        base -- base letters for each Walze, first letter for the first Walze
                (a string)
        """
        # check whether the given base is valid
        if len(base) != self.__num_walzen:
            raise InputError(base)
        for char in base:
            if char not in self.__alphabet:
                raise InputError(base)
        self.__base = base

    def encode(self, msg, verbose=False, vverbose=False):
        """En- or decodes a given input message according to the Enigma machine
        used by the Germans in World War II.

        Arguments:
        msg -- message to be en- or decoded (a string)
        verbose -- prints a detailed output if True (a boolean)
        vverbose -- prints a very detailed output if True (a boolean)

        >>> enigma = Enigma(3, alphabet="ABCDEFGH")
        >>> enigma.set_walze(0, "BDGCAEFH")
        >>> enigma.set_walze(1, "FBEAGCHD")
        >>> enigma.set_walze(2, "FDEABGCH")
        >>> enigma.set_umkehrwalze("HFGEDBCA")
        >>> enigma.encode("A")
        'G'
        >>> enigma = Enigma()
        >>> enigma.set_walze(0, 'BDFHJLCPRTXVZNYEIWGAKMUSQO')
        >>> enigma.set_walze(1, 'AJDKSIRUXBLHWTMCQGZNPYFVOE')
        >>> enigma.set_walze(2, 'EKMFLGDQVZNTOWYHXUSPAIBRCJ')
        >>> enigma.set_umkehrwalze("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        >>> enigma.set_base("LCM")
        >>> enigma.set_ringkerben([22, 5, 1])
        >>> enigma.encode("QMJIDO MZWZJFJR")
        'ENIGMAREVEALED'
        """
        wlz = self.__walzen
        ukw = self.__umkehrwalze
        sb = self.__steckerbrett
        base = self.__base
        rk = self.__ringkerben
        alphabet = self.__alphabet

        if verbose or vverbose:
            print("Enigma\n{:*>79}\
                   \nYou are using an Enigma machine with {} Walzen:\n{: >40}\
                   \n{: >40}\n{:>40}\nUmkehrwalze: {: >27}\nSteckerbrett: {}\
                   \nBase: {: >11}\nRingkerben:   {}\n{:*>79}".format("",
                  len(wlz), wlz[0], wlz[1], wlz[2], ukw, sb, base, rk, ""))

        # process the input message to fit requirements (upper case, list)
        msg = msg.upper()
        char_list = list(msg)

        # compute the relation Walzen and set them to the given position
        walzen = []
        # counts the current index of the Walzen in relation to the original Walzen
        # necessary for the Ringkerben to work properly
        count = [0, 0, 0]
        for i, walze in enumerate(wlz):
            # compute the relation between the alphabet and the letter on the walze
            relation_walze = []
            for j, char in enumerate(walze):
                new_char = ord(char) - 65 - j
                relation_walze.append(new_char)
            index = ord(base[i]) - 65
            walze = relation_walze[index:] + relation_walze[:index]
            count[i] = index
            walzen.append(walze)

        # encode the message
        encoded_message = ""

        for char in char_list:
            lex_index = ord(char) - 65
            if lex_index >= 0 and lex_index <= 25:
                # get the corresponding letter Walze for each current relation Walze
                walzen_curr = []
                for walze in walzen:
                    walzen_curr.append("".join([chr((num + i) % len(alphabet) + 65)
                                               for i, num in enumerate(walze)]))

                if vverbose:
                    print("{: >8}Input: {}".format("", char))

                # send the input character through the Steckerbrett
                for stecker in sb:
                    if char in stecker:
                        new_char = stecker.replace(char, "")
                        lex_index = ord(new_char) - 65
                        if vverbose:
                            print("{: >8}Steckerbrett: {} --> {}".format("", char, new_char))
                        break

                # send the current character through the 3 selected Walzen
                for walze in walzen_curr:
                    new_letter = walze[lex_index]
                    lex_index = ord(new_letter) - 65
                    if vverbose:
                        print("{: >38}".format(alphabet))
                        print("{: >38} --> {}".format(walze, new_letter))

                # reflect the current character on the selected Umkehrwalze
                new_letter = ukw[lex_index]
                lex_index = ord(new_letter) - 65
                if vverbose:
                    print("{: >42}".format(alphabet))
                    print("{: >42} --> {}".format(ukw, new_letter))

                # send the current character back through the 3 Walzen in reverse order
                for walze in walzen_curr[-1::-1]:
                    index = walze.index(new_letter)
                    new_letter = alphabet[index]
                    lex_index = ord(new_letter) - 65
                    if vverbose:
                        print("{: >38}".format(walze))
                        print("{: >38} --> {}".format(alphabet, new_letter))

                char = chr(lex_index + 65)

                # send the character back through the Steckerbrett
                for stecker in sb:
                    if char in stecker:
                        char = stecker.replace(char, "")
                        if vverbose:
                            print("{: >8}Steckerbrett: {} --> {}".format("", new_letter, char))
                        break

                if vverbose:
                    print("{: >8}Output: {}".format("", char))

                # add the computed character to the encoded message
                encoded_message = encoded_message + char
                if vverbose:
                    print("   ", encoded_message)

                # rotate the Walzen according to the Ringkerben and the current position
                walzen[0] = walzen[0][1:] + [walzen[0][0]]
                count[0] = count[0] % 26 + 1
                if count[0] == rk[0]:
                    if vverbose:
                        print("Rotate second Walze")
                    walzen[1] = walzen[1][1:] + [walzen[1][0]]
                    count[1] = count[1] % 26 + 1
                    if count[1] == rk[1]:
                        if vverbose:
                            print("Rotate third Walze")
                        walzen[2] = walzen[2][1:] + [walzen[2][0]]
        if verbose or vverbose:
            print("Message: {}\nCode:    {}".format(msg, encoded_message))
        return encoded_message


class InputError(Exception):
    def __init__(self, input):
        self._input = input

    def __str__(self):
        return "Invalid Argument:" + repr(self._input)


if __name__ == "__main__":
    doctest.testmod()
