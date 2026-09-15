import numpy as np
import openseespy.opensees as ops
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


# ============================================================
# 1. Model parameters
# ============================================================
L = 4.0                  # Cantilever length
BC_len = 0.75 * L         # Strut BC length (constant)
q_load = 50.0            # Uniform load along beam (N/m, downward)
E = 200e9                # Young's modulus (Pa)
tw  = 0.008
p_side = 0.2            # Square section side length (m)
A_sec = p_side*tw*2 + (p_side - tw*2)*tw*2
I_sec = p_side ** 4 / 12.0 - (p_side-tw*2) ** 4 / 12.0  

# Node tags
NODE_A = 1   # Fixed end
NODE_C = 2   # Connection point C
NODE_D = 3   # Free end D
NODE_B = 4   # Support B

# Element tags
ELEM_AC = 1
ELEM_CD = 2
ELEM_BC = 3

MAT_STEEL = 1


# ============================================================
# 2. OpenSees model and analysis
# ============================================================
def build_and_analyze(k):
    """
    Given k (vertical distance from A to B), build and analyze
    the model with OpenSeesPy.
    BC length is constant, so C position is determined by geometry.
    Loads: concentrated load P at D + uniform load q along the beam.
    Returns absolute vertical displacement at D.
    """
    # Horizontal coordinate of C: x^2 + k^2 = BC_len^2
    x_C = np.sqrt(max(BC_len**2 - k**2, 1e-8))

    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)

    # Nodes
    ops.node(NODE_A, 0.0, 0.0)     # A fixed end
    ops.node(NODE_C, x_C, 0.0)     # C on beam
    ops.node(NODE_D, L, 0.0)       # D free end
    ops.node(NODE_B, 0.0, -k)      # B below A by k

    # Boundary conditions
    ops.fix(NODE_A, 1, 1, 1)       # A fixed
    ops.fix(NODE_B, 1, 1, 1)       # B pinned

    # Material
    ops.uniaxialMaterial('Elastic', MAT_STEEL, E)

    # Geometric transformation
    ops.geomTransf('Linear', 1)

    # Elements
    ops.element('elasticBeamColumn', ELEM_AC, NODE_A, NODE_C,
                A_sec, E, I_sec, 1)
    ops.element('elasticBeamColumn', ELEM_CD, NODE_C, NODE_D,
                A_sec, E, I_sec, 1)
    ops.element('Truss', ELEM_BC, NODE_B, NODE_C, A_sec, MAT_STEEL)

    # Loads
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)


    # Uniform load along the beam (downward)
    ops.eleLoad('-ele', ELEM_AC, '-type', '-beamUniform', -q_load, 0.0)
    ops.eleLoad('-ele', ELEM_CD, '-type', '-beamUniform', -q_load, 0.0)

    # Analysis settings
    ops.constraints('Plain')
    ops.numberer('Plain')
    ops.system('BandGeneral')
    ops.algorithm('Linear')
    ops.integrator('LoadControl', 1.0)
    ops.analysis('Static')

    ok = ops.analyze(1)
    if ok != 0:
        raise RuntimeError(f"OpenSees analysis failed, k = {k}")

    return abs(ops.nodeDisp(NODE_D, 2))


# ============================================================
# 3. One-dimensional Nelder-Mead simplex method
# ============================================================
def nelder_mead_1d(func, x0, step=0.1, max_iter=50, tol=1e-10):
    """One-dimensional Nelder-Mead using two vertices"""
    x1, x2 = x0, x0 + step
    f1, f2 = func(x1), func(x2)
    history = [(x1, f1), (x2, f2)]

    for it in range(max_iter):
        if f1 > f2:
            x1, x2 = x2, x1
            f1, f2 = f2, f1

        if abs(f2 - f1) < tol:
            break

        # Reflection
        x_r = 2 * x1 - x2
        f_r = func(x_r)

        if f_r < f1:
            # Expansion
            x_e = x1 + 2.0 * (x_r - x1)
            f_e = func(x_e)
            if f_e < f_r:
                x2, f2 = x_e, f_e
            else:
                x2, f2 = x_r, f_r
        elif f_r < f2:
            x2, f2 = x_r, f_r
        else:
            # Contraction
            x_c = x1 + 0.5 * (x2 - x1)
            f_c = func(x_c)
            if f_c < f2:
                x2, f2 = x_c, f_c
            else:
                x2 = x1 + 0.5 * (x2 - x1)
                f2 = func(x2)

        history.append((x1, f1))

    if f1 <= f2:
        return x1, f1, it + 1, history
    return x2, f2, it + 1, history


# ============================================================
# 4. Main program
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print(f"Cantilever + strut BC (constant length = {BC_len/L:.1f}L) optimization")
    print(f"Loads:  uniform q = {q_load} N/m")
    print("=" * 60)

    # Range of k
    k_min = 0.02 * L
    k_max = 0.98 * BC_len

    def objective(k):
        k = float(np.clip(k, k_min, k_max))
        return build_and_analyze(k)

    # Initial scan
    print("--- Initial scan ---")
    k_scan = np.linspace(k_min, k_max, 30)
    f_scan = np.array([objective(k) for k in k_scan])
    for i in range(0, len(k_scan), 5):
        x_C = np.sqrt(max(BC_len**2 - k_scan[i]**2, 0))
        print(f"  k = {k_scan[i]:.4f}  (x_C = {x_C:.4f})  ->  "
              f"deflection at D = {f_scan[i]:.6e} m")
    print()

    # Nelder-Mead optimization
    print("--- Nelder-Mead optimization ---")
    k_opt, f_opt, n_iter, history = nelder_mead_1d(
        objective, x0=BC_len / 2, step=0.1 * L,
        max_iter=40, tol=1e-12
    )
    x_C_opt = np.sqrt(max(BC_len**2 - k_opt**2, 0))

    print(f"\nIterations: {n_iter}")
    print(f"Optimal k = {k_opt:.6f} m  (k/L = {k_opt/L:.4f})")
    print(f"Corresponding C position x_C = {x_C_opt:.6f} m  "
          f"(x_C/L = {x_C_opt/L:.4f})")
    print(f"Minimum deflection at D = {f_opt:.6e} m")

    # ============================================================
    # 5. Plotting
    # ============================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # ---------- Left: structural layout ----------
    A = np.array([0.0, 0.0])
    D = np.array([L, 0.0])
    C = np.array([x_C_opt, 0.0])
    B = np.array([0.0, -k_opt])

    # Fixed support at A
    ax1.plot([A[0], A[0]], [-1.1, 1.1], 'k-', linewidth=3)
    for yy in np.linspace(-1.0, 1.0, 9):
        ax1.plot([A[0]-0.15, A[0]], [yy-0.10, yy+0.10], 'k-', linewidth=1.2)

    # Cantilever AD
    ax1.plot([A[0], D[0]], [A[1], D[1]], 'b-', linewidth=5,
             solid_capstyle='round', label='Cantilever AD')

    # Strut BC
    ax1.plot([B[0], C[0]], [B[1], C[1]], 'g-', linewidth=4,
             solid_capstyle='round', label=f'Strut BC = {BC_len/L:.1f}L')

    # Nodes
    for pt, name, dx, dy, col in [
        (A, 'A', -0.28, 0.0, 'r'),
        (C, 'C', 0.0, 0.25, 'r'),
        (D, 'D', 0.18, 0.25, 'r'),
        (B, 'B', -0.28, -0.05, 'k'),
    ]:
        ax1.plot(pt[0], pt[1], 'o', color=col, markersize=10)
        ax1.text(pt[0]+dx, pt[1]+dy, name, fontsize=14,
                 fontweight='bold', color=col)

    # Support triangle at B
    tri = plt.Polygon([[B[0]-0.14, B[1]-0.04],
                       [B[0]+0.14, B[1]-0.04],
                       [B[0], B[1]-0.32]],
                      closed=True, color='k')
    ax1.add_patch(tri)


    # Uniform load q arrows
    n_arrows = 8
    x_q = np.linspace(0.05*L, 0.95*L, n_arrows)
    for xq in x_q:
        ax1.annotate('', xy=(xq, 0.0), xytext=(xq, 0.55),
                     arrowprops=dict(arrowstyle='-|>', color='darkorange',
                                     lw=1.6, mutation_scale=12))
    ax1.text(L/2, 0.75, f'Uniform load q = {q_load} N/m',
             ha='center', fontsize=10, color='darkorange')

    # Dimension: k
    ax1.annotate('', xy=(A[0]-0.5, A[1]), xytext=(A[0]-0.5, B[1]),
                 arrowprops=dict(arrowstyle='<->', color='gray', lw=1.2))
    ax1.text(A[0]-0.72, (A[1]+B[1])/2, f'k={k_opt:.2f}',
             ha='right', va='center', fontsize=10, color='gray')

    # Dimension: x_C
    ax1.annotate('', xy=(A[0], A[1]-0.55), xytext=(C[0], C[1]-0.55),
                 arrowprops=dict(arrowstyle='<->', color='gray', lw=1.2))
    ax1.text((A[0]+C[0])/2, A[1]-0.78, f'x_C={x_C_opt:.2f}',
             ha='center', fontsize=10, color='gray')

    # Dimension: L
    ax1.annotate('', xy=(A[0], A[1]-1.0), xytext=(D[0], D[1]-1.0),
                 arrowprops=dict(arrowstyle='<->', color='gray', lw=1.2))
    ax1.text((A[0]+D[0])/2, A[1]-1.22, 'L', ha='center',
             fontsize=11, color='gray')

    ax1.set_xlim(-1.4, L+0.9)
    ax1.set_ylim(-1.6, 1.6)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title(f'Optimal configuration  (k={k_opt:.3f}, x_C={x_C_opt:.3f})',
                  fontsize=12)
    ax1.legend(loc='upper right', fontsize=9)

    # ---------- Right: deflection vs k ----------
    ax2.plot(k_scan, f_scan * 1e3, 'b-', linewidth=2,
             label='Deflection at D (P + q)')
    ax2.plot(k_opt, f_opt * 1e3, 'r*', markersize=18,
             label=f'Optimal k={k_opt:.3f}')
    ax2.axvline(k_opt, color='r', linestyle='--', alpha=0.5)

    # Annotate minimum
    ax2.annotate(f'Minimum\nf={f_opt*1e3:.4f} mm',
                 xy=(k_opt, f_opt*1e3),
                 xytext=(k_opt + 0.2,
                         f_opt*1e3 + 0.25*(max(f_scan)-min(f_scan))*1e3),
                 fontsize=10, color='r',
                 arrowprops=dict(arrowstyle='->', color='r'))

    ax2.set_xlabel('k  (vertical distance from A to B, m)', fontsize=11)
    ax2.set_ylabel('Vertical deflection at D (mm)', fontsize=11)
    ax2.set_title('Deflection vs k (concentrated + uniform load)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)

    plt.tight_layout()
    plt.show()