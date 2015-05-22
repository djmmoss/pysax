import numpy as np

class SAX(object):
    def __init__(self, x, w, a):
        # Window
        self.window = w

        # Alphabet Size
        self.alph_size = a

        self.alph = self.make_alph(a)

        # Signal Length
        self.signal_length = len(x)

        # Signal
        self.signal = self.normalise(x)

        # Compute PAA
        self.signal_paa = self.compute_paa(self.signal,
                                           self.signal_length,
                                           self.window)

        # Compute SAX
        self.signal_sax = self.compute_sax(self.signal_paa,
                                           self.window,
                                           self.alph_size,
                                           self.alph)

    def make_alph(self, a):
        if a == 1:
            return np.array([0])
        elif a == 2:
            return np.array([-0.43, 0.43])
        elif a == 3:
            return np.array([-0.67, 0, 0.67])
        elif a == 4:
            return np.array([-0.84, -0.25, 0.25, 0.84])
        elif a == 5:
            return np.array([-0.97, -0.43, 0, 0.43, 0.97])
        elif a == 6:
            return np.array([-1.07, -0.57, -0.18, 0.18, 0.57, 1.07])
        elif a == 7:
            return np.array([-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15])
        elif a == 8:
            return np.array([-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22])

    def compress(self):
        sax_letters = self.to_letters()
        n = len(sax_letters)
        sax_compress = []
        prev_sax = sax_letters[0]
        c = 1
        for i in xrange(1, n):
            if sax_letters[i] == prev_sax:
                c += 1
            else:
                sax_compress.append((prev_sax, c))
                c = 1
            prev_sax = sax_letters[i]

        sax_compress.append((prev_sax, c))
        return sax_compress

    def level_of_compression(self):
        sax_compress = self.compress()
        sax_letters = self.to_letters()
        return 100 - float(len(sax_compress))/float(len(sax_letters)) * 100

    def to_letters(self):
        sax_numeric = self.signal_sax
        n = len(sax_numeric)
        sax_letter = []
        for i in xrange(n):
            sax_letter.append(self.determine_letter(sax_numeric[i]))

        return ''.join(sax_letter)

    def determine_letter(self, n):
        if n == 0:
            return 'a'
        elif n == 1:
            return 'b'
        elif n == 2:
            return 'c'
        elif n == 3:
            return 'd'
        elif n == 4:
            return 'e'
        elif n == 5:
            return 'f'
        elif n == 6:
            return 'g'
        elif n == 7:
            return 'h'
        elif n == 8:
            return 'i'
        elif n == 9:
            return 'j'

        return 'ERR'

    def normalise(self, sig):
        mean_norm = sig - np.mean(sig)
        std_norm = mean_norm/np.std(sig)
        return std_norm

    def compute_paa(self, sig, n, w):
        sig_paa = np.zeros(w)
        for i in xrange(w):
            lower = n/w*i
            upper = n/w*(i+1)
            sig_sum = sum(sig[lower:upper])
            sig_paa[i] = float(w)/float(n)*sig_sum

        return sig_paa

    def compute_sax(self, sig, w, a, alph):
        sax_word = np.zeros(w)
        for i in xrange(w):
            for j in xrange(a):
                if sig[i] < alph[j]:
                    sax_word[i] = j
                    break
                elif j == a:
                    sax_word[i] = j+1

        return sax_word
