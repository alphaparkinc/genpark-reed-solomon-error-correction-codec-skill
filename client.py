class GF256:
    def __init__(self):
        self.exp = [0] * 512
        self.log = [0] * 256
        x = 1
        for i in range(255):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:
                x ^= 0x11D
        for i in range(255, 512):
            self.exp[i] = self.exp[i - 255]

    def mul(self, x, y):
        if x == 0 or y == 0:
            return 0
        return self.exp[self.log[x] + self.log[y]]

class ReedSolomonCodec:
    """
    Reed-Solomon Error Correction Codec over GF(2^8).
    Appends parity symbols and computes algebraic syndromes.
    """
    def __init__(self, nsym=4):
        self.gf = GF256()
        self.nsym = nsym
        self.gen = self._generator_poly(nsym)

    def _generator_poly(self, nsym):
        def poly_mul(p, q):
            r = [0] * (len(p) + len(q) - 1)
            for j in range(len(q)):
                for i in range(len(p)):
                    r[i + j] ^= self.gf.mul(p[i], q[j])
            return r

        g = [1]
        for i in range(nsym):
            g = poly_mul(g, [1, self.gf.exp[i]])
        return g

    def encode(self, msg):
        msg = list(msg)
        out = msg + [0] * self.nsym
        for i in range(len(msg)):
            coef = out[i]
            if coef != 0:
                for j in range(len(self.gen)):
                    out[i + j] ^= self.gf.mul(self.gen[j], coef)
        return msg + out[len(msg):]

    def verify_syndromes(self, codeword):
        syndromes = []
        for i in range(self.nsym):
            val = 0
            root = self.gf.exp[i]
            for coef in codeword:
                val = self.gf.mul(val, root) ^ coef
            syndromes.append(val)
        return syndromes
