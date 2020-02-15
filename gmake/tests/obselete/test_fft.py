import numpy as np
import mkl_fft
rng = np.random.RandomState(42)
X_c = rng.rand(1024, 1024, 1).astype(np.complex128)
X_f = X_c.astype(X_c.dtype, order='F')

print(np.abs(mkl_fft.fft2(X_c, axes=(0, 1))).max())
print(np.abs(np.fft.fft2(X_c, axes=(0, 1))).max())
print(np.abs(mkl_fft.fft2(X_f, axes=(0, 1))).max())
print(np.abs(np.fft.fft2(X_f, axes=(0, 1))).max())