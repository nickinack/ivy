# global
from hypothesis import strategies as st
import importlib

# local
import ivy
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


@st.composite
def _pop_size_num_samples_replace_n_probs(draw):
    prob_dtype = draw(helpers.get_dtypes("float", full=False))
    batch_size = draw(helpers.ints(min_value=1, max_value=5))
    replace = draw(st.booleans())
    num_samples = draw(helpers.ints(min_value=1, max_value=20))
    probs = draw(
        helpers.array_values(
            dtype=prob_dtype[0],
            shape=[batch_size, num_samples],
            min_value=1.0013580322265625e-05,
            max_value=1.0,
            exclude_min=True,
        )
    )
    return prob_dtype, batch_size, num_samples, replace, probs


# multinomial
@handle_frontend_test(
    fn_tree="torch.multinomial",
    everything=_pop_size_num_samples_replace_n_probs(),
)
def test_torch_multinomial(
    *,
    everything,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    prob_dtype, batch_size, num_samples, replace, probs = everything

    def call():
        return helpers.test_frontend_function(
            input_dtypes=prob_dtype,
            as_variable_flags=as_variable,
            with_out=with_out,
            num_positional_args=num_positional_args,
            native_array_flags=native_array,
            frontend=frontend,
            fn_tree=fn_tree,
            on_device=on_device,
            test_values=False,
            input=probs,
            num_samples=num_samples,
            replacement=replace,
        )

    ret = call()

    if not ivy.exists(ret):
        return

    ret_np, ret_from_np = ret
    ret_np = helpers.flatten_and_to_np(ret=ret_np)
    ret_from_np = helpers.flatten_and_to_np(ret=ret_from_np)
    for (u, v) in zip(ret_np, ret_from_np):
        assert u.dtype == v.dtype
        assert u.shape == v.shape


@handle_frontend_test(
    fn_tree="torch.manual_seed",
    seed=st.integers(min_value=0, max_value=2**32 - 1),
)
def test_torch_manual_seed(
    *,
    seed,
    fn_tree,
    frontend,
):
    # just test calling the function
    frontend_fw = importlib.import_module(fn_tree[25 : fn_tree.rfind(".")])
    split_index = fn_tree.rfind(".")
    _, fn_name = fn_tree[:split_index], fn_tree[split_index + 1 :]
    frontend_fw.__dict__[fn_name](seed)


@handle_frontend_test(
    fn_tree="torch.poisson",
    dtype_and_lam=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float", full=False),
        min_value=0,
        max_value=100,
        min_num_dims=0,
        max_num_dims=10,
        min_dim_size=1,
    )
)
def test_torch_poisson(
    *,
    dtype_and_lam,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    on_device,
    fn_tree,
    frontend,
):
    lam_dtype, lam = dtype_and_lam

    def call():
        return helpers.test_frontend_function(
            input_dtypes=lam_dtype,
            as_variable_flags=as_variable,
            with_out=with_out,
            num_positional_args=num_positional_args,
            native_array_flags=native_array,
            frontend=frontend,
            fn_tree=fn_tree,
            on_device=on_device,
            test_values=False,
            input=lam[0],
        )

    ret = call()

    if not ivy.exists(ret):
        return

    ret_np, ret_from_np = ret
    ret_np = helpers.flatten_and_to_np(ret=ret_np)
    ret_from_np = helpers.flatten_and_to_np(ret=ret_from_np)
    for (u, v) in zip(ret_np, ret_from_np):
        assert u.dtype == v.dtype
        assert u.shape == v.shape
