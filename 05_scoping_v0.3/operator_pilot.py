"""
Illustrative pilot for the Arctic microtopography benchmark review (v0.3).

Purpose: show, with closed-form results plus a small simulation, how much of the
proposed "Experiment A" (synthetic operator benchmark) is already determined by
linear-filter theory, and where the real uncertainty lies (support scale, noise
structure). This is a design aid, NOT a result of the proposed study.

Outputs (written to ./out):
  - kernel_properties.csv      closed-form noise gains / false-slope floors
  - false_slope_floor.csv      expected spurious gradient on flat ground
  - synthetic_results.csv      simulation errors by operator x support x noise
  - fig_response.png           along-/cross-gradient amplitude responses
  - fig_synthetic.png          error vs support scale for each operator
"""
import os
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261002)

# ---------------------------------------------------------------------------
# 1. 3x3 x-derivative kernels (rows = y, cols = x), unit grid spacing.
#    Divide by h at use. Each kernel returns exactly a for a plane z = a*x.
# ---------------------------------------------------------------------------
r2 = np.sqrt(2.0)
KERNELS = {
    # Zevenbergen & Thorne (1987) partial quartic -> central difference (2FD)
    "2FD (Zevenbergen-Thorne)": np.array([[0, 0, 0], [-1, 0, 1], [0, 0, 0]]) / 2.0,
    # Evans-Young quadratic LSQ over 3x3 -> equal weights (3FD / Prewitt)
    "3FD (Evans-Young; Prewitt)": np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]) / 6.0,
    # Unwin (1981) reciprocal-distance weights (3FDWRD)
    "3FDWRD (Unwin)": np.array([[-1, 0, 1], [-r2, 0, r2], [-1, 0, 1]]) / (4 + 2 * r2),
    # Horn (1981) reciprocal-squared-distance weights (3FDWRSD / Sobel)
    "Horn (3FDWRSD; Sobel)": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]) / 8.0,
}
# check plane reproduction
xx = np.array([[-1, 0, 1]] * 3, dtype=float)
for k, w in KERNELS.items():
    assert abs((w * xx).sum() - 1.0) < 1e-12, k


def cross_smoothing(k, fy):
    """Cross-gradient (y) transfer factor of the kernel at cycles/cell fy."""
    col = KERNELS[k][:, 2]  # right column weights (y profile)
    col = col / col.sum()
    # col = [a, b, a]  ->  b + 2a cos(2 pi fy)
    return col[1] + 2 * col[0] * np.cos(2 * np.pi * fy)


def along_response(fx):
    """All four kernels share the same along-gradient response:
    H(fx)/ideal = sin(2 pi fx) / (2 pi fx)  (fx in cycles per cell)."""
    fx = np.asarray(fx, dtype=float)
    return np.sinc(2 * fx)  # numpy sinc(x) = sin(pi x)/(pi x)


# ---------------------------------------------------------------------------
# 2. Closed-form noise gain and false-slope floor
#    For white elevation noise sd_z, SD of each gradient component is
#    sd_z * sqrt(sum w^2) / h. For symmetric kernels Gx and Gy are uncorrelated,
#    so on truly flat ground |grad| is Rayleigh with mean s*sqrt(pi/2).
# ---------------------------------------------------------------------------
rows = []
for k, w in KERNELS.items():
    g = np.sqrt((w ** 2).sum())
    rows.append((k, g))
with open(os.path.join(OUT, "kernel_properties.csv"), "w") as f:
    f.write("kernel,noise_gain_sqrt_sum_w2,relative_to_3FD\n")
    g3 = dict(rows)["3FD (Evans-Young; Prewitt)"]
    for k, g in rows:
        f.write(f"\"{k}\",{g:.4f},{g / g3:.3f}\n")

# Error scenarios drawn from the 2024 NOAA Quinhagak QL1 lidar metadata:
#   NVA = 0.031 m RMSE (non-vegetated); VVA = 0.254 m at the 95th percentile
#   (vegetated). VVA/1.96 = 0.13 m is used ONLY as a rough Gaussian-equivalent
#   scale for illustration; vegetated errors are not Gaussian and are biased.
scen = {"NVA 0.031 m (open ground)": 0.031, "VVA-equivalent 0.13 m (vegetated)": 0.254 / 1.96}
with open(os.path.join(OUT, "false_slope_floor.csv"), "w") as f:
    f.write("scenario,cell_m,kernel,sd_component,mean_false_gradient,mean_false_slope_deg\n")
    for sname, sd in scen.items():
        for h in (0.25, 0.5, 1.0, 2.0):
            for k, g in rows:
                s = sd * g / h
                m = s * np.sqrt(np.pi / 2)
                f.write(f"\"{sname}\",{h},\"{k}\",{s:.4f},{m:.4f},{np.degrees(np.arctan(m)):.2f}\n")

# ---------------------------------------------------------------------------
# 3. Figure: amplitude responses
# ---------------------------------------------------------------------------
fx = np.linspace(0, 0.5, 201)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].plot(fx, along_response(fx), "k-", lw=2, label="all four 3x3 kernels")
ax[0].plot(fx, np.ones_like(fx), "k:", lw=1, label="ideal derivative")
ax[0].set_xlabel("frequency along gradient (cycles per cell)")
ax[0].set_ylabel("response / ideal")
ax[0].set_title("Along-gradient: identical for 2FD, 3FD, 3FDWRD, Horn")
ax[0].legend(fontsize=8)
for k in KERNELS:
    ax[1].plot(fx, cross_smoothing(k, fx), lw=1.6, label=k)
ax[1].set_xlabel("frequency across gradient (cycles per cell)")
ax[1].set_ylabel("cross-gradient smoothing factor")
ax[1].set_title("Across-gradient: the only difference")
ax[1].legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_response.png"), dpi=200)
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. Small synthetic simulation
#    Surface: Gaussian hummock (relief A, width sigma_f) on a 0.5% plane.
#    Two reference definitions:
#      native truth  = analytical gradient of the unsmoothed surface
#      truth at L    = gradient of surface convolved with Gaussian(sigma_L);
#                      exact for a Gaussian mound: amplitude A*sf^2/(sf^2+sL^2),
#                      width sqrt(sf^2+sL^2); the plane is unchanged.
#    Errors are normalised by the mean true gradient magnitude over the mound,
#    so different supports are comparable.
# ---------------------------------------------------------------------------
A, SF, BG = 0.30, 1.0, 0.005           # m, m, m/m
EXTENT = 24.0                           # m


def truth_grad(X, Y, sl):
    s2 = SF ** 2 + sl ** 2
    amp = A * SF ** 2 / s2
    g = amp * np.exp(-(X ** 2 + Y ** 2) / (2 * s2))
    gx = -X / s2 * g + BG
    gy = -Y / s2 * g
    return np.hypot(gx, gy)


def surface(X, Y):
    return A * np.exp(-(X ** 2 + Y ** 2) / (2 * SF ** 2)) + BG * X


def correlated_noise(shape, h, sd, corr_len):
    n = rng.standard_normal(shape)
    if corr_len > 0:
        n = ndimage.gaussian_filter(n, sigma=corr_len / h, mode="wrap")
        n /= n.std()
    return n * sd


def estimate(z, h, k, sl):
    """Estimator k applied after Gaussian pre-smoothing at support sl (m)."""
    if k == "Gaussian derivative":
        s = max(sl, 1e-9) / h
        gx = ndimage.gaussian_filter(z, sigma=s, order=(0, 1), mode="nearest") / h
        gy = ndimage.gaussian_filter(z, sigma=s, order=(1, 0), mode="nearest") / h
        return np.hypot(gx, gy)
    zs = ndimage.gaussian_filter(z, sigma=sl / h, mode="nearest") if sl > 0 else z
    w = KERNELS[k]
    gx = ndimage.correlate(zs, w, mode="nearest") / h
    gy = ndimage.correlate(zs, w.T, mode="nearest") / h
    return np.hypot(gx, gy)


noise_models = {
    "white 0.031 m (open-ground NVA)": (0.031, 0.0),
    "white 0.13 m (vegetated, illustrative)": (0.13, 0.0),
    "correlated 0.10 m, ~1 m range (vegetation-patch bias, illustrative)": (0.10, 1.0),
}
supports = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
ESTS = list(KERNELS) + ["Gaussian derivative"]
NREP = 30
results = []
for h in (0.25, 0.5, 1.0):
    x = np.arange(-EXTENT / 2, EXTENT / 2 + 1e-9, h)
    X, Y = np.meshgrid(x, x)
    z0 = surface(X, Y)
    inner = (np.abs(X) < EXTENT / 2 - 4) & (np.abs(Y) < EXTENT / 2 - 4)
    mound = inner & (np.hypot(X, Y) <= 2.5 * SF)
    flat = inner & (np.hypot(X, Y) >= 5 * SF)
    native = truth_grad(X, Y, 0.0)
    norm_native = native[mound].mean()
    for nname, (sd, cl) in noise_models.items():
        noises = [correlated_noise(z0.shape, h, sd, cl) for _ in range(NREP)]
        for sl in supports:
            tL = truth_grad(X, Y, sl)
            normL = tL[mound].mean()
            for k in ESTS:
                if k == "Gaussian derivative" and sl < h / 2:
                    continue
                if k != "Gaussian derivative" and 0 < sl < h / 2:
                    continue
                e_nat, e_L, fflat = [], [], []
                for n in noises:
                    g = estimate(z0 + n, h, k, sl)
                    e_nat.append(np.sqrt(np.mean((g[mound] - native[mound]) ** 2)) / norm_native)
                    e_L.append(np.sqrt(np.mean((g[mound] - tL[mound]) ** 2)) / normL)
                    fflat.append(np.mean(g[flat]) - BG)
                results.append((h, nname, sl, k, np.mean(e_nat), np.mean(e_L), np.mean(fflat)))

with open(os.path.join(OUT, "synthetic_results.csv"), "w") as f:
    f.write("cell_m,noise,support_sigma_m,estimator,nrmse_vs_native_truth,nrmse_vs_truth_at_L,mean_false_grad_flat\n")
    for r in results:
        f.write(f"{r[0]},\"{r[1]}\",{r[2]},\"{r[3]}\",{r[4]:.4f},{r[5]:.4f},{r[6]:.4f}\n")

# Figure: h = 0.5 m, three noise models, NRMSE vs native truth (solid) and vs truth-at-L (dashed)
cols = {"2FD (Zevenbergen-Thorne)": "#d62728", "3FD (Evans-Young; Prewitt)": "#1f77b4",
        "3FDWRD (Unwin)": "#2ca02c", "Horn (3FDWRSD; Sobel)": "#9467bd", "Gaussian derivative": "#000000"}
fig, axs = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
for ax, nname in zip(axs, noise_models):
    for k in ESTS:
        pts = sorted([(r[2], r[4], r[5]) for r in results if r[0] == 0.5 and r[1] == nname and r[3] == k])
        if not pts:
            continue
        ax.plot([p[0] for p in pts], [p[1] for p in pts], "-", marker="o", ms=3, color=cols[k], label=k)
        ax.plot([p[0] for p in pts], [p[2] for p in pts], ":", color=cols[k], lw=1)
    ax.set_title(nname, fontsize=8.5)
    ax.set_xlabel("support sigma_L (m) applied before estimator; 0 = raw 3x3")
    ax.set_yscale("log")
    ax.grid(alpha=0.3)
axs[0].set_ylabel("normalised RMSE of |grad| on hummock")
axs[0].legend(fontsize=7, loc="upper right")
fig.suptitle("Pilot (0.5 m cells; hummock relief 0.30 m, sigma 1.0 m). Solid: vs native truth. "
             "Dotted: vs truth defined at the same support L.", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_synthetic.png"), dpi=200)
plt.close(fig)
print("done")
