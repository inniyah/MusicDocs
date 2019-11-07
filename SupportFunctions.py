#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Hue: angle in degrees (0-360)
# Saturation: fraction between 0 and 1
# Value: fraction between 0 and 1

def hsv_to_rgb(hue, saturation=1., value=1.):
    h = float(hue)
    s = float(saturation)
    v = float(value)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if   hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    return r, g, b

# Red: fraction between 0 and 1
# Green: fraction between 0 and 1
# Blue: fraction between 0 and 1

def rgb_to_hsv(r, g, b):
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if   mx == mn: h = 0
    elif mx == r:  h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:  h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:  h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx) * 100
    v = mx * 100
    return h, s, v

def lab_to_rgb(l, a, b):
    y = (l + 16.) / 116.
    x = a / 500. + y
    z = y - b / 200.

    x = 0.95047 * ((x * x * x) if (x * x * x > 0.008856) else ((x - 16./116.) / 7.787))
    y = 1.00000 * ((y * y * y) if (y * y * y > 0.008856) else ((y - 16./116.) / 7.787))
    z = 1.08883 * ((z * z * z) if (z * z * z > 0.008856) else ((z - 16./116.) / 7.787))

    r = x *  3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y *  1.8758 + z *  0.0415
    b = x *  0.0557 + y * -0.2040 + z *  1.0570

    r = (1.055 * (r**(1./2.4)) - 0.055) if (r > 0.0031308) else (12.92 * r)
    g = (1.055 * (g**(1./2.4)) - 0.055) if (g > 0.0031308) else (12.92 * g)
    b = (1.055 * (b**(1./2.4)) - 0.055) if (b > 0.0031308) else (12.92 * b)

    return [ max(0., min(1., r)), max(0., min(1., g)), max(0., min(1., b)) ]

def rgb_to_lab(r, g, b):
    r = ((r + 0.055) / 1.055)**2.4 if (r > 0.04045) else (r / 12.92);
    g = ((g + 0.055) / 1.055)**2.4 if (g > 0.04045) else (g / 12.92);
    b = ((b + 0.055) / 1.055)**2.4 if (b > 0.04045) else (b / 12.92);

    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000;
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;

    x = x**(1./3.) if (x > 0.008856) else (7.787 * x) + 16/116.0;
    y = y**(1./3.) if (y > 0.008856) else (7.787 * y) + 16/116.0;
    z = z**(1./3.) if (z > 0.008856) else (7.787 * z) + 16/116.0;

    return [(116. * y) - 16., 500. * (x - y), 200. * (y - z)]

# This works for counting non-zero bits in 64-bit positive numbers
def count_bits(n):
    n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
    n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
    n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
    n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
    n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
    n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32)
    return n

# Unoptimized Discrete Fourier transform (DFT). It ncurs a complexity of O(N^2)
# See: https://jyhmiinlin.github.io/pynufft/misc/dft.html
def naive_DFT(x):
    N = numpy.size(x)
    X = numpy.zeros((N,), dtype=numpy.complex128)
    for m in range(0, N):
        for n in range(0, N):
            X[m] += x[n] * numpy.exp(-numpy.pi * 2j * m * n / N)
    return X

# Unoptimized Inverse Discrete Fourier transform (IDFT). It ncurs a complexity of O(N^2)
# See: https://jyhmiinlin.github.io/pynufft/misc/dft.html
def naive_IDFT(x):
    N = numpy.size(x)
    X = numpy.zeros((N,), dtype=numpy.complex128)
    for m in range(0, N):
        for n in range(0, N):
            X[m] += x[n] * numpy.exp(numpy.pi * 2j * m * n / N)
    return X/N

def polar(z):
    a= z.real
    b= z.imag
    r = math.hypot(a, b)
    theta = math.atan2(b, a)
    return r, theta

def main():
    x = numpy.random.rand(12,)
    # compute DFT
    X = naive_DFT(x)
    # compute FFT using numpy's fft function
    X2 = numpy.fft.fft(x)
    # now compare DFT with numpy fft
    print('Is DFT close to fft?', numpy.allclose(X - X2, 1e-12))

    x = numpy.random.rand(12,)
    # compute FFT
    X = numpy.fft.fft(x)
    # compute IDFT using IDFT
    x2 = naive_IDFT(X)
    # now compare DFT with numpy fft
    print('Is IDFT close to original?', numpy.allclose(x - x2, 1e-12))

    tonic = 1
    scale = (1<<0) + (1<<2) + (1<<4) + (1<<6) + (1<<7) + (1<<9) + (1<<11)
    notes_in_scale = [(scale & 1<<(r%12) != 0) for r in range(tonic*7, tonic*7 + 12)]
    eprint("{}".format([polar(c) for c in naive_DFT(notes_in_scale)]))

if __name__ == '__main__':
    main()


