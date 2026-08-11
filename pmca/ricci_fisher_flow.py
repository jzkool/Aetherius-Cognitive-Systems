import jax.numpy as jnp
from jax import jit

@jit
def compute_christoffel_symbols(g):
    n = g.shape[0]
    g_inv = jnp.linalg.pinv(g + jnp.eye(n) * 1e-6)
    
    g_exp_k = jnp.expand_dims(g, axis=1) 
    g_exp_i = jnp.expand_dims(g, axis=0) 
    dg = g_exp_k - g_exp_i
    
    mask = 1.0 - jnp.eye(n)[:, :, jnp.newaxis]
    dg = dg * mask
    
    term = (jnp.einsum('kl,ijl->kij', g_inv, dg) + 
            jnp.einsum('kl,jil->kij', g_inv, dg) - 
            jnp.einsum('kl,lij->kij', g_inv, dg))
    return 0.5 * term

@jit
def compute_ricci_tensor(Gamma):
    Gamma_kjk = jnp.expand_dims(jnp.einsum('kjk->kj', Gamma), axis=1)
    dGamma_jk_i = Gamma_kjk - Gamma
    
    Gamma_kik = jnp.expand_dims(jnp.einsum('kik->ki', Gamma), axis=2)
    Gamma_jik = jnp.transpose(Gamma, (2, 1, 0))
    dGamma_ik_j = Gamma_kik - Gamma_jik
    
    term1 = jnp.sum(dGamma_jk_i - dGamma_ik_j, axis=0)
    term2 = jnp.einsum('mjk,kim->ij', Gamma, Gamma) - jnp.einsum('mik,kjm->ij', Gamma, Gamma)
    
    R = term1 + term2
    return (R + R.T) / 2.0

@jit
def compute_perelman_normalization(R, g):
    n = g.shape[0]
    g_inv = jnp.linalg.pinv(g + jnp.eye(n) * 1e-6)
    S_total = jnp.trace(g_inv @ R)
    V_total = jnp.trace(g)
    return jnp.where(V_total == 0, 0.0, S_total / V_total)

@jit
def compute_fisher_metric(L):
    return L + jnp.eye(L.shape[0])

@jit
def integration_step(g, L, alpha=0.1, beta=0.05, eta=0.01):
    n = g.shape[0]
    Gamma = compute_christoffel_symbols(g)
    R = compute_ricci_tensor(Gamma)
    r_scalar = compute_perelman_normalization(R, g)
    
    Delta_g = jnp.dot(L, g)
    F = compute_fisher_metric(L)
    
    R_norm = R - (r_scalar / n) * g
    dg_dt = -alpha * R_norm + beta * (Delta_g + F)
    
    g_next = g + eta * dg_dt
    return (g_next + g_next.T) / 2.0

