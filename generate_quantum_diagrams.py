"""
Generate high-resolution (300 DPI) diagrams for Quantum Computing Seminar Report and Presentation:
1. Bloch Sphere & Qubit Superposition Principles
2. Quantum Computer Physical & Layered Architecture (Dilution Refrigerator -> Control -> QPU)
3. Quantum vs Classical Computational Complexity & Algorithms (Shor's & Grover's speedup)
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('assets', exist_ok=True)

# -----------------------------------------------------------------------------
# 1. BLOCH SPHERE & QUBIT SUPERPOSITION
# -----------------------------------------------------------------------------
def generate_bloch_superposition():
    fig = plt.figure(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Subplot 1: Classical Bit vs Quantum Qubit
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')

    ax1.text(5, 9.3, "CLASSICAL BIT vs QUANTUM QUBIT", fontsize=11, fontweight='bold', ha='center', color='#0F172A')

    # Classical Bit Card
    box_c = patches.FancyBboxPatch((0.8, 5.0), 8.4, 3.6, boxstyle="round,pad=0.1,rounding_size=0.15", ec="#2563EB", fc="#EFF6FF", lw=1.5)
    ax1.add_patch(box_c)
    ax1.text(5, 8.1, "CLASSICAL BIT (Deterministic)", fontsize=10, fontweight='bold', ha='center', color='#1E40AF')
    ax1.text(2.6, 6.7, "[ 0 ]", fontsize=18, fontweight='bold', ha='center', va='center', color='#1D4ED8')
    ax1.text(5.0, 6.7, "OR", fontsize=11, fontweight='bold', ha='center', va='center', color='#64748B')
    ax1.text(7.4, 6.7, "[ 1 ]", fontsize=18, fontweight='bold', ha='center', va='center', color='#1D4ED8')
    ax1.text(5, 5.5, "Can only exist in one definite state at any given moment\nState space for N bits = 1 state out of 2^N", 
             fontsize=7.8, ha='center', color='#334155', linespacing=1.2)

    # Quantum Qubit Card
    box_q = patches.FancyBboxPatch((0.8, 0.6), 8.4, 3.8, boxstyle="round,pad=0.1,rounding_size=0.15", ec="#7C3AED", fc="#F5F3FF", lw=1.5)
    ax1.add_patch(box_q)
    ax1.text(5, 3.9, "QUANTUM QUBIT (Superposition)", fontsize=10, fontweight='bold', ha='center', color='#5B21B6')
    ax1.text(5, 2.8, r"$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$", fontsize=13, fontweight='bold', ha='center', va='center', color='#6D28D9')
    ax1.text(5, 1.8, r"where $|\alpha|^2 + |\beta|^2 = 1$ (Probability Amplitudes)", fontsize=8.5, fontstyle='italic', ha='center', color='#4C1D95')
    ax1.text(5, 1.0, "Exists in a linear continuum of |0> and |1> simultaneously\nState space for N qubits = 2^N states simultaneously in superposition", 
             fontsize=7.6, ha='center', color='#334155', linespacing=1.2)

    # Subplot 2: Bloch Sphere Diagram (3D Projection)
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.set_facecolor('#FFFFFF')
    
    # Sphere Wireframe
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 30)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    ax2.plot_wireframe(x, y, z, color='#E2E8F0', alpha=0.35, linewidth=0.6)
    
    # Equator circle
    theta = np.linspace(0, 2 * np.pi, 100)
    ax2.plot(np.cos(theta), np.sin(theta), np.zeros(100), color='#94A3B8', linestyle='--', linewidth=1.2)

    # Axes
    ax2.plot([-1.2, 1.2], [0, 0], [0, 0], color='#475569', linewidth=1.2) # X
    ax2.plot([0, 0], [-1.2, 1.2], [0, 0], color='#475569', linewidth=1.2) # Y
    ax2.plot([0, 0], [0, 0], [-1.2, 1.2], color='#475569', linewidth=1.2) # Z

    ax2.text(1.3, 0, 0, "+X", fontsize=9, fontweight='bold', color='#334155')
    ax2.text(0, 1.3, 0, "+Y", fontsize=9, fontweight='bold', color='#334155')
    ax2.text(0, 0, 1.3, "|0⟩ (North)", fontsize=10, fontweight='bold', color='#047857')
    ax2.text(0, 0, -1.4, "|1⟩ (South)", fontsize=10, fontweight='bold', color='#B91C1C')

    # State Vector |psi> in Superposition
    # theta = pi/3, phi = pi/4
    th, ph = np.pi / 3, np.pi / 4
    vx = np.sin(th) * np.cos(ph)
    vy = np.sin(th) * np.sin(ph)
    vz = np.cos(th)
    ax2.quiver(0, 0, 0, vx, vy, vz, color='#7C3AED', linewidth=2.8, arrow_length_ratio=0.15)
    ax2.text(vx * 1.15, vy * 1.15, vz * 1.15, "|ψ⟩ State Vector", fontsize=9.5, fontweight='bold', color='#6D28D9')

    ax2.set_xlim([-1.2, 1.2])
    ax2.set_ylim([-1.2, 1.2])
    ax2.set_zlim([-1.2, 1.2])
    ax2.axis('off')
    ax2.set_title("THE BLOCH SPHERE GEOMETRIC MODEL", fontsize=11, fontweight='bold', pad=8, color='#0F172A')

    plt.tight_layout()
    plt.savefig('assets/quantum_bloch_sphere_superposition.png', dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Generated assets/quantum_bloch_sphere_superposition.png successfully!")

# -----------------------------------------------------------------------------
# 2. QUANTUM COMPUTER PHYSICAL & LAYERED ARCHITECTURE
# -----------------------------------------------------------------------------
def generate_quantum_architecture():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(6.0, 7.65, "PHYSICAL & SYSTEM ARCHITECTURE OF A QUANTUM COMPUTER", 
            fontsize=14, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(6.0, 7.3, "From Classical High-Level Quantum Software down to Cryogenic Sub-Kelvin Hardware", 
            fontsize=9.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # Layer 1: Classical User & Software Layer (Room Temp: 300 K)
    b1 = patches.FancyBboxPatch((0.6, 5.5), 10.8, 1.5, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#3B82F6", fc="#EFF6FF", lw=1.8)
    ax.add_patch(b1)
    ax.text(0.9, 6.75, "LAYER 1: QUANTUM APPLICATION & SOFTWARE STACK (Room Temp: 300 K)", fontsize=10, fontweight='bold', color='#1E40AF')
    
    softwares = [
        ("High-Level Applications", "Quantum Chemistry, Optimization,\nCryptography & Quantum ML", 1.0),
        ("Quantum SDKs & Frameworks", "Qiskit (IBM), Cirq (Google),\nPennylane, Q# (Microsoft)", 4.6),
        ("Quantum Compiler & Transpiler", "Circuit Optimization, Gate Mapping\n& OpenQASM Synthesis", 8.2)
    ]
    for stitle, sdesc, sx in softwares:
        box = patches.FancyBboxPatch((sx, 5.65), 3.4, 0.9, boxstyle="round,pad=0.06,rounding_size=0.08", ec="#93C5FD", fc="#FFFFFF", lw=1.2)
        ax.add_patch(box)
        ax.text(sx + 1.7, 6.25, stitle, fontsize=8.5, fontweight='bold', ha='center', color='#1D4ED8')
        ax.text(sx + 1.7, 5.9, sdesc, fontsize=7.2, ha='center', color='#334155')

    # Arrow Down 1 -> 2
    for ax_x in [2.7, 6.3, 9.9]:
        ax.annotate('', xy=(ax_x, 4.95), xytext=(ax_x, 5.5),
                    arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.8))

    # Layer 2: Classical-Quantum Control Electronics (Room Temp to 4 K)
    b2 = patches.FancyBboxPatch((0.6, 3.4), 10.8, 1.45, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#8B5CF6", fc="#F5F3FF", lw=1.8)
    ax.add_patch(b2)
    ax.text(0.9, 4.6, "LAYER 2: CRYOGENIC CONTROL & READOUT INTERFACE (300 K down to 4 K)", fontsize=10, fontweight='bold', color='#5B21B6')

    controls = [
        ("Arbitrary Waveform Generators (AWG)", "Generates precise microwave pulses\n(4–8 GHz) for single/two-qubit gates", 1.0),
        ("Cryogenic Attenuators & Filters", "Attenuates thermal noise photons;\nShields qubits from ambient heat", 4.6),
        ("Readout Resonators & Amplifiers", "Low-noise HEMT and Traveling-Wave\nParametric Amplifiers (JPA / TWPA)", 8.2)
    ]
    for ctitle, cdesc, cx in controls:
        box = patches.FancyBboxPatch((cx, 3.55), 3.4, 0.85, boxstyle="round,pad=0.06,rounding_size=0.08", ec="#C4B5FD", fc="#FFFFFF", lw=1.2)
        ax.add_patch(box)
        ax.text(cx + 1.7, 4.12, ctitle, fontsize=8.2, fontweight='bold', ha='center', color='#6D28D9')
        ax.text(cx + 1.7, 3.78, cdesc, fontsize=7.0, ha='center', color='#334155')

    # Arrow Down 2 -> 3
    for ax_x in [2.7, 6.3, 9.9]:
        ax.annotate('', xy=(ax_x, 2.85), xytext=(ax_x, 3.4),
                    arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.8))

    # Layer 3: Dilution Refrigerator & Quantum Processing Unit (15 mK = -273.135 °C)
    b3 = patches.FancyBboxPatch((0.6, 0.5), 10.8, 2.25, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#059669", fc="#ECFDF5", lw=1.8)
    ax.add_patch(b3)
    ax.text(0.9, 2.5, "LAYER 3: QUANTUM HARDWARE CORE (Dilution Refrigerator at 15 milliKelvin)", fontsize=10, fontweight='bold', color='#065F46')

    q_cores = [
        ("Dilution Refrigerator Stages", "50K Flange -> 4K Plate -> 0.8K Still\n-> 100mK Cold Plate -> 15mK Base Plate\n(Colder than deep interstellar space)", 1.0),
        ("Quantum Processor Unit (QPU)", "Superconducting Transmon Qubits\nJosephson Junction Non-linear Inductors\n2D Planar Lattice Coupling Architecture", 4.6),
        ("Magnetic & Thermal Shielding", "Cryoperm & Mu-Metal Magnetic Shields\nPrevents stray Earth magnetic fields\nfrom destroying fragile superposition", 8.2)
    ]
    for qtitle, qdesc, qx in q_cores:
        box = patches.FancyBboxPatch((qx, 0.65), 3.4, 1.6, boxstyle="round,pad=0.06,rounding_size=0.08", ec="#6EE7B7", fc="#FFFFFF", lw=1.2)
        ax.add_patch(box)
        ax.text(qx + 1.7, 1.95, qtitle, fontsize=8.2, fontweight='bold', ha='center', color='#047857')
        ax.text(qx + 1.7, 1.25, qdesc, fontsize=7.2, ha='center', color='#334155', linespacing=1.2)

    plt.tight_layout()
    plt.savefig('assets/quantum_system_architecture.png', dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Generated assets/quantum_system_architecture.png successfully!")

# -----------------------------------------------------------------------------
# 3. QUANTUM ALGORITHMS & COMPUTATIONAL COMPLEXITY SPEEDUP
# -----------------------------------------------------------------------------
def generate_algorithms_speedup():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(5.5, 5.65, "QUANTUM ADVANTAGE: COMPUTATIONAL SPEEDUP COMPARISON", 
            fontsize=13, fontweight='bold', ha='center', color='#0F172A')
    ax.text(5.5, 5.3, "Exponential and Polynomial Acceleration Over Best Classical Algorithms", 
            fontsize=9, fontstyle='italic', ha='center', color='#475569')

    # Algorithm 1: Shor's Algorithm
    b_shor = patches.FancyBboxPatch((0.6, 0.6), 4.7, 4.4, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#DC2626", fc="#FEF2F2", lw=1.8)
    ax.add_patch(b_shor)
    ax.text(2.95, 4.65, "SHOR'S ALGORITHM (1994)", fontsize=11, fontweight='bold', ha='center', color='#991B1B')
    ax.text(2.95, 4.3, "Integer Factorization & Discrete Logarithms", fontsize=8.5, fontstyle='italic', ha='center', color='#7F1D1D')

    # Inner boxes
    c_clas = patches.FancyBboxPatch((0.9, 2.7), 4.1, 1.4, boxstyle="round,pad=0.06,rounding_size=0.08", ec="#FCA5A5", fc="#FFFFFF", lw=1.2)
    ax.add_patch(c_clas)
    ax.text(2.95, 3.75, "Classical Best: General Number Field Sieve", fontsize=8, fontweight='bold', ha='center', color='#991B1B')
    ax.text(2.95, 3.25, r"Sub-exponential: $O(e^{c \sqrt[3]{N \log^2 N}})$", fontsize=9.5, ha='center', color='#1E293B')
    ax.text(2.95, 2.85, "Factoring 2048-bit RSA = Billions of Years", fontsize=7.5, ha='center', color='#64748B')

    c_quant = patches.FancyBboxPatch((0.9, 1.0), 4.1, 1.5, boxstyle="round,pad=0.06,rounding_size=0.08", ec="#86EFAC", fc="#F0FDF4", lw=1.2)
    ax.add_patch(c_quant)
    ax.text(2.95, 2.15, "Quantum Shor's Algorithm: QFT Period Finding", fontsize=8, fontweight='bold', ha='center', color='#166534')
    ax.text(2.95, 1.65, r"Polynomial Time: $O((\log N)^3)$", fontsize=10.5, fontweight='bold', ha='center', color='#15803D')
    ax.text(2.95, 1.2, "Factoring 2048-bit RSA = Minutes to Hours!\nBreaks standard RSA-2048 & ECC encryption", fontsize=7.5, ha='center', color='#14532D', linespacing=1.1)

    # Algorithm 2: Grover's Algorithm
    b_grov = patches.FancyBboxPatch((5.7, 0.6), 4.7, 4.4, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#2563EB", fc="#EFF6FF", lw=1.8)
    ax.add_patch(b_grov)
    ax.text(8.05, 4.65, "GROVER'S ALGORITHM (1996)", fontsize=11, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(8.05, 4.3, "Unstructured Database & Black-Box Search", fontsize=8.5, fontstyle='italic', ha='center', color='#1E3A8A')

    c_g_c = patches.FancyBboxPatch((6.0, 2.7), 4.1, 1.4, boxstyle="round,pad=0.06,rounding_size=0.08", ec="#93C5FD", fc="#FFFFFF", lw=1.2)
    ax.add_patch(c_g_c)
    ax.text(8.05, 3.75, "Classical Search: Linear Scan", fontsize=8, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(8.05, 3.25, r"Linear Time Complexity: $O(N)$", fontsize=10, ha='center', color='#1E293B')
    ax.text(8.05, 2.85, "Searching 1 Trillion items = ~500 Billion checks", fontsize=7.5, ha='center', color='#64748B')

    c_g_q = patches.FancyBboxPatch((6.0, 1.0), 4.1, 1.5, boxstyle="round,pad=0.06,rounding_size=0.08", ec="#86EFAC", fc="#F0FDF4", lw=1.2)
    ax.add_patch(c_g_q)
    ax.text(8.05, 2.15, "Quantum Grover's Search: Amplitude Amplification", fontsize=8, fontweight='bold', ha='center', color='#166534')
    ax.text(8.05, 1.65, r"Quadratic Speedup: $O(\sqrt{N})$", fontsize=10.5, fontweight='bold', ha='center', color='#15803D')
    ax.text(8.05, 1.2, "Searching 1 Trillion items = Only 1 Million checks!\nHalves symmetric cipher key strength (AES-128 -> AES-64)", fontsize=7.5, ha='center', color='#14532D', linespacing=1.1)

    plt.tight_layout()
    plt.savefig('assets/quantum_algorithms_speedup.png', dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Generated assets/quantum_algorithms_speedup.png successfully!")

if __name__ == '__main__':
    generate_bloch_superposition()
    generate_quantum_architecture()
    generate_algorithms_speedup()
    print("All Quantum Computing visual assets generated successfully!")

