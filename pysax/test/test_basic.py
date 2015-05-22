import numpy as np
import pytest
from pysax import sax


def test_one():
    n = 20
    w = 10
    a = 4

    sig = np.zeros(n)
    for i in xrange(n):
        sig[i] = 1 if i % 5 == 0 else 3 if i % 7 == 0 else 7 if i % 3 == 0 else 9

    s = sax.SAX(sig, w, a)

    expect_letters = 'bdbbdbdaad'
    assert(s.to_letters() == expect_letters)

