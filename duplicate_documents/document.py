# -*- encoding: utf-8 -*-

from datasketch import MinHash, LeanMinHash
import config



class document:
    def __init__(self, content):
        self.k_shingles = self.get_k_shingles(config.SHINGLE_CONFIG['k'], content)


    def get_k_shingles(self, k, data):
        if k < 1 or k > len(data):
            raise ValueError('value of k is in range (1, num_words_in_document)')
        data = data.lower().split()
        # shingles = set(data)
        shingles = set([])
        for i in xrange(0, len(data) - k + 1):
            shingles.update([u' '.join(data[i : i+k])])
        return shingles


    def get_minhash(self, shingles, num_perm):
        mh = MinHash(num_perm=num_perm)
        for d in shingles:
            mh.update(d.encode('utf8'))
        return LeanMinHash(mh)