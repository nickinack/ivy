# global
from typing import Union, Optional, Sequence
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability import distributions as tfd
from tensorflow.python.framework.dtypes import DType

# local
import ivy
from .. import backend_version
from ivy.func_wrapper import with_unsupported_dtypes
from ivy.functional.ivy.random import (
    _check_bounds_and_get_shape,
    _check_shapes_broadcastable,
)


# dirichlet
@with_unsupported_dtypes({"2.9.1 and below": ("blfoat16", "float16",)}, backend_version)
def dirichlet(
    alpha: Union[tf.Tensor, tf.Variable, float, Sequence[float]],
    /,
    *,
    size: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
    seed: Optional[int] = None,
    dtype: Optional[tf.Tensor] = None,
) -> Union[tf.Tensor, tf.Variable]:
    size = size if size is not None else len(alpha)

    if dtype is None:
        dtype = tf.float64
    else:
        dtype = dtype
    if seed is not None:
        tf.random.set_seed(seed)
    return tf.cast(
        tfd.Dirichlet(
            concentration=alpha,
            validate_args=False,
            allow_nan_stats=True,
            force_probs_to_zero_outside_support=False,
            name="Dirichlet",
        ).sample(size),
        dtype=dtype,
    )


def beta(
    alpha: Union[float, tf.Tensor, tf.Variable],
    beta: Union[float, tf.Tensor, tf.Variable],
    /,
    *,
    shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    device: str = None,
    dtype: Optional[Union[DType, ivy.Dtype]] = None,
    seed: Optional[int] = None,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    if not dtype:
        dtype = ivy.default_float_dtype()
    dtype = ivy.as_native_dtype(dtype)
    shape = _check_bounds_and_get_shape(alpha, beta, shape)
    alpha = tf.cast(alpha, dtype)
    beta = tf.cast(beta, dtype)
    with tf.device(device):
        return tfp.distributions.Beta(alpha, beta).sample(shape, seed=seed)


def gamma(
    alpha: Union[float, tf.Tensor, tf.Variable],
    beta: Union[float, tf.Tensor, tf.Variable],
    /,
    *,
    shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    device: str = None,
    dtype: Optional[Union[DType, ivy.Dtype]] = None,
    seed: Optional[int] = None,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    if not dtype:
        dtype = ivy.default_float_dtype()
    dtype = ivy.as_native_dtype(dtype)
    shape = _check_bounds_and_get_shape(alpha, beta, shape)
    alpha = tf.cast(alpha, dtype)
    beta = tf.cast(beta, dtype)
    with tf.device(device):
        return tfp.distributions.Gamma(alpha, beta).sample(shape, seed=seed)


@with_unsupported_dtypes({"2.9.1 and below": ("bfloat16",)}, backend_version)
def poisson(
        lam: Union[float, tf.Tensor, tf.Variable],
        *,
        shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
        device: str,
        dtype: DType,
        seed: Optional[int] = None,
        out: Optional[Union[tf.Tensor, tf.Variable]] = None,
):
    lam = tf.cast(lam, "float32")
    with tf.device(device):
        if seed:
            tf.random.set_seed(seed)
        if shape is None:
            return tf.random.poisson((), lam, dtype=dtype, seed=seed)
        _check_shapes_broadcastable(shape, lam.shape)
        lam = tf.broadcast_to(lam, tuple(shape))
        return tf.random.poisson((), lam, dtype=dtype, seed=seed)
