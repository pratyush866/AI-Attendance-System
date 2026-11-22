"""
Professional PowerPoint Presentation Generator (.pptx)
Seminar Topic: QUANTUM COMPUTING: Principles, Physical Architecture, Quantum Algorithms and Future Horizons
Institution: ITM College of Science and Management, GIDA, Gorakhpur
Course: BCA Final Year - Academic Session 2026-2027
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    print("Generating Quantum Computing PowerPoint Presentation (.pptx)...")
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    # Color Palette
    DARK_NAVY = RGBColor(10, 15, 36)      # #0A0F24
    NAVY_BLUE = RGBColor(30, 58, 138)     # #1E3A8A
    ROYAL_BLUE = RGBColor(37, 99, 235)    # #2563EB
    VIOLET = RGBColor(124, 58, 237)       # #7C3AED
    SLATE_DARK = RGBColor(15, 23, 42)     # #0F172A
    SLATE_BODY = RGBColor(51, 65, 85)     # #334155
    SLATE_MUTED = RGBColor(100, 116, 139) # #64748B
    LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
    WHITE = RGBColor(255, 255, 255)
    CYAN = RGBColor(6, 182, 212)
    GREEN = RGBColor(16, 185, 129)

    def add_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="SEMINAR ON QUANTUM COMPUTING | ITM COLLEGE"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ROYAL_BLUE
        
        p_tit = tf.add_paragraph()
        p_tit.text = title_text
        p_tit.font.name = "Arial"
        p_tit.font.size = Pt(22)
        p_tit.font.bold = True
        p_tit.font.color.rgb = SLATE_DARK
        p_tit.space_before = Pt(4)

        # Thin accent line under header
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        line.line.fill.background()

    def add_card(slide, left, top, width, height, title, items, border_color=ROYAL_BLUE, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)
        
        p_head = tf.paragraphs[0]
        p_head.text = title
        p_head.font.name = "Arial"
        p_head.font.size = Pt(15)
        p_head.font.bold = True
        p_head.font.color.rgb = border_color
        p_head.space_after = Pt(10)
        
        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = "Calibri"
            p.font.size = Pt(13)
            p.font.color.rgb = SLATE_BODY
            p.space_after = Pt(6)
            p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Premium Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, DARK_NAVY)

    # Decorative accent gradient-like shapes
    dec1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.1), Inches(5.9))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = CYAN
    dec1.line.fill.background()

    # Logo if available
    if os.path.exists('assets/itm_college_logo.png'):
        s1.shapes.add_picture('assets/itm_college_logo.png', Inches(11.2), Inches(0.8), width=Inches(1.3))

    tb_title = s1.shapes.add_textbox(Inches(1.2), Inches(0.9), Inches(9.8), Inches(3.2))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "ITM COLLEGE OF SCIENCE AND MANAGEMENT, GORAKHPUR"
    p0.font.name = "Calibri"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = CYAN

    p1 = tf1.add_paragraph()
    p1.text = "SEMINAR REPORT PRESENTATION"
    p1.font.name = "Calibri"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(148, 163, 184)
    p1.space_before = Pt(4)

    p2 = tf1.add_paragraph()
    p2.text = "QUANTUM COMPUTING"
    p2.font.name = "Arial"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Principles, Physical Architecture, Quantum Algorithms & Future Horizons"
    p3.font.name = "Calibri"
    p3.font.size = Pt(17)
    p3.font.color.rgb = RGBColor(196, 181, 253) # soft purple
    p3.space_before = Pt(4)

    # Info Card at Bottom
    tb_info = s1.shapes.add_textbox(Inches(1.2), Inches(4.3), Inches(11.0), Inches(2.5))
    tf_info = tb_info.text_frame
    tf_info.word_wrap = True

    p_by = tf_info.paragraphs[0]
    p_by.text = "SUBMITTED BY (BCA FINAL YEAR - SESSION 2026-2027):"
    p_by.font.name = "Calibri"
    p_by.font.size = Pt(12)
    p_by.font.bold = True
    p_by.font.color.rgb = CYAN

    p_st = tf_info.add_paragraph()
    p_st.text = "• Pratyush Mishra (Team Leader - Roll: 2514018680059)\n" \
                "• Atul Upadhyay (Roll: 2514018680041)  |  • Divyanshu Upadhyay (Roll: 2514018680045)\n" \
                "• Adesh Bhatt (Roll: 2514018680026)"
    p_st.font.name = "Calibri"
    p_st.font.size = Pt(13)
    p_st.font.color.rgb = WHITE
    p_st.space_before = Pt(4)

    p_gd = tf_info.add_paragraph()
    p_gd.text = "SEMINAR GUIDE: Ms. Vinita Yadav (Assistant Professor, Dept. of Computer Applications)"
    p_gd.font.name = "Calibri"
    p_gd.font.size = Pt(12.5)
    p_gd.font.bold = True
    p_gd.font.color.rgb = RGBColor(251, 191, 36) # gold
    p_gd.space_before = Pt(12)

    # =========================================================================
    # SLIDE 2: AGENDA & OUTLINE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, LIGHT_BG)
    add_header(s2, "Seminar Agenda & Presentation Roadmap")

    agenda_items_left = [
        ("1. Introduction to Quantum Computing", "Meaning, paradigm shift, classical transistor physical barriers"),
        ("2. Classical Bits vs. Quantum Qubits", "Deterministic Boolean logic vs. multi-dimensional Hilbert spaces"),
        ("3. History & Milestones", "Feynman's vision, Deutsch Turing Machine, NISQ era & Google Sycamore"),
        ("4. Core Physical Mechanisms", "Superposition, Bloch Sphere, Entanglement, and Quantum Interference")
    ]
    agenda_items_right = [
        ("5. Quantum Computer Architecture", "Dilution refrigerators (15 mK), control electronics, transmon qubits"),
        ("6. Quantum Algorithms & Speedup", "Shor's prime factorization & Grover's database search acceleration"),
        ("7. Real-World Applications", "Post-Quantum Cryptography, drug discovery, finance, and logistics"),
        ("8. Challenges & India's NQM", "Decoherence, error correction, National Quantum Mission, BCA careers")
    ]

    for idx, (title, desc) in enumerate(agenda_items_left):
        top_pos = Inches(1.8 + idx * 1.3)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(5.6), Inches(1.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ROYAL_BLUE
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(13)
        p1.font.color.rgb = NAVY_BLUE
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = SLATE_BODY

    for idx, (title, desc) in enumerate(agenda_items_right):
        top_pos = Inches(1.8 + idx * 1.3)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), top_pos, Inches(5.6), Inches(1.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = VIOLET
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.bold = True
        p1.font.size = Pt(13)
        p1.font.color.rgb = VIOLET
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = SLATE_BODY

    # =========================================================================
    # SLIDE 3: 1. INTRODUCTION - WHAT IS QUANTUM COMPUTING?
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, LIGHT_BG)
    add_header(s3, "1. Introduction: The Quantum Paradigm Shift")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "Classical Computing Limits",
             [
                 "Transistors have scaled down to sub-2nm boundaries.",
                 "At atomic scales, electrons experience quantum tunneling, creating thermal dissipation and data leakage.",
                 "Moore's Law is nearing fundamental physical limits.",
                 "Intractable Problems: Simulating molecular structures or factoring large composite numbers requires millions of years on classical supercomputers.",
                 "Classical computers evaluate possibilities sequentially (one trajectory at a time)."
             ],
             border_color=ROYAL_BLUE)

    add_card(s3, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "The Quantum Solution",
             [
                 "Directly utilizes subatomic quantum mechanics to perform computational operations.",
                 "Information encoded into Quantum Bits (Qubits) such as photon polarization or superconducting circuits.",
                 "Simultaneous Parallelism: Processes an exponential 2^N state space concurrently.",
                 "Constructive Interference: Amplitudes of correct solutions are amplified while incorrect paths cancel out.",
                 "Richard Feynman's Postulate (1981): Nature is quantum mechanical; to simulate nature, computers must be quantum."
             ],
             border_color=VIOLET)

    # =========================================================================
    # SLIDE 4: CLASSICAL BITS VS QUANTUM QUBITS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, LIGHT_BG)
    add_header(s4, "Classical Bits vs. Quantum Qubits (Bloch Sphere)")

    # Left: Text card
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.1),
             "Fundamental Differences",
             [
                 "Classical Bit: Deterministic; strictly in state 0 OR state 1.",
                 "Quantum Qubit: Exists in a continuous linear superposition of |0⟩ and |1⟩ simultaneously.",
                 "Mathematical Formulation:\n  |ψ⟩ = α|0⟩ + β|1⟩\n  where |α|² + |β|² = 1.",
                 "N Classical Bits = Stores 1 specific number out of 2^N.",
                 "N Quantum Qubits = Holds all 2^N states simultaneously.",
                 "Measurement causes wavefunction collapse to a single classical eigenvalue (0 or 1)."
             ],
             border_color=ROYAL_BLUE)

    # Right: Embedded Diagram
    if os.path.exists('assets/quantum_bloch_sphere_superposition.png'):
        s4.shapes.add_picture('assets/quantum_bloch_sphere_superposition.png', Inches(6.3), Inches(1.8), width=Inches(6.2))

    # =========================================================================
    # SLIDE 5: 2. HISTORY & MILESTONES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, LIGHT_BG)
    add_header(s5, "2. Evolution & Major Historical Milestones")

    milestones = [
        ("1981", "Richard Feynman (MIT)", "Proposed simulating physics using quantum mechanics rather than classical bits."),
        ("1985", "David Deutsch (Oxford)", "Formalized the Universal Quantum Turing Machine (QTM) and quantum logic gates."),
        ("1994", "Peter Shor (Bell Labs)", "Invented polynomial-time quantum prime factorization, threatening RSA encryption."),
        ("1996", "Lov Grover (Bell Labs)", "Demonstrated quadratic acceleration for unstructured database search (O(√N))."),
        ("2016", "IBM Quantum Cloud", "Launched IBM Quantum Experience, offering free public cloud access to real QPUs."),
        ("2019", "Google Quantum AI", "Sycamore 53-qubit processor proved 'Quantum Supremacy' in 200 seconds.")
    ]

    for idx, (yr, ent, desc) in enumerate(milestones):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.8 + row * 1.65)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(1.45))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ROYAL_BLUE if col == 0 else VIOLET
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        p0 = tf.paragraphs[0]
        p0.text = f"{yr} — {ent}"
        p0.font.bold = True
        p0.font.size = Pt(13)
        p0.font.color.rgb = NAVY_BLUE if col == 0 else VIOLET
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(11)
        p1.font.color.rgb = SLATE_BODY
        p1.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: 3. CORE PRINCIPLES: SUPERPOSITION & BLOCH SPHERE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, LIGHT_BG)
    add_header(s6, "3. Core Mechanism: Superposition & The Bloch Sphere")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.1),
             "Quantum Superposition",
             [
                 "Linear combination of orthonormal basis vectors |0⟩ and |1⟩.",
                 "Probability Amplitudes:\n  P(0) = |α|²\n  P(1) = |β|²\n  Total: |α|² + |β|² = 1.",
                 "Hadamard Gate (H):\nCreates equal 50/50 superposition:\n  H|0⟩ = (|0⟩ + |1⟩) / √2\n  H|1⟩ = (|0⟩ - |1⟩) / √2.",
                 "Unlocks simultaneous exploration of complex state spaces."
             ],
             border_color=ROYAL_BLUE)

    add_card(s6, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.1),
             "The Bloch Sphere",
             [
                 "Geometrical model of a single two-level qubit.",
                 "State vector parameterized by spherical angles (θ, φ):\n  |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩.",
                 "North Pole = State |0⟩ (θ = 0).",
                 "South Pole = State |1⟩ (θ = π).",
                 "Equator = Balanced superposition states (|+⟩, |-⟩, |+i⟩, |-i⟩).",
                 "Quantum gates act as rotations around axes on the sphere."
             ],
             border_color=VIOLET)

    add_card(s6, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.1),
             "Wavefunction Collapse",
             [
                 "Measurement is irreversible and probabilistic.",
                 "During computation: Qubit remains in delicate coherent superposition.",
                 "Upon observation: Interacts with macroscopic environment and collapses instantly.",
                 "Quantum programs must extract answers via phase interference rather than direct observation."
             ],
             border_color=CYAN)

    # =========================================================================
    # SLIDE 7: ENTANGLEMENT & INTERFERENCE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, LIGHT_BG)
    add_header(s7, "3. Core Mechanism: Entanglement & Interference")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "Quantum Entanglement",
             [
                 "Two or more qubits become inextricably interconnected such that the state of one instantly defines the state of the other.",
                 "Albert Einstein described it as 'Spooky action at a distance' (EPR Paradox).",
                 "Bell States (Maximally Entangled Pairs):\n  |Φ⁺⟩ = (|00⟩ + |11⟩) / √2\n  |Ψ⁺⟩ = (|01⟩ + |10⟩) / √2.",
                 "Exponential Scaling: 300 perfectly entangled qubits can hold more numbers simultaneously than atoms in the observable universe (2^300).",
                 "Forms the backbone of quantum teleportation and superdense coding."
             ],
             border_color=VIOLET)

    add_card(s7, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "Quantum Interference",
             [
                 "Probability amplitudes are complex numbers with real and imaginary phases.",
                 "Constructive Interference: Amplitudes with identical phases add together, dramatically increasing the probability of the correct output.",
                 "Destructive Interference: Amplitudes with opposite phases (180° out of phase) cancel each other out to zero.",
                 "Algorithmic Goal: Design quantum gate sequences so that all wrong answers cancel out, and the single correct answer has nearly 100% measurement probability."
             ],
             border_color=GREEN)

    # =========================================================================
    # SLIDE 8: QUANTUM LOGIC GATES
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, LIGHT_BG)
    add_header(s8, "Quantum Logic Gates: Reversible Unitary Operators")

    gates = [
        ("Pauli-X Gate (NOT)", "Performs a 180° flip across the X-axis on the Bloch sphere.\nTransforms |0⟩ → |1⟩ and |1⟩ → |0⟩.\nRepresented by matrix [[0, 1], [1, 0]].", ROYAL_BLUE),
        ("Hadamard Gate (H)", "The fundamental superposition gate.\nConverts basis states into equal linear combinations:\nH|0⟩ = |+⟩ and H|1⟩ = |-⟩.", VIOLET),
        ("Pauli-Z Gate (Phase)", "Flips the phase of the |1⟩ state by 180° while leaving |0⟩ completely unchanged.\nTransforms |1⟩ → -|1⟩.", CYAN),
        ("CNOT Gate (Controlled-NOT)", "Essential two-qubit gate.\nFlips the target qubit if and only if the control qubit is |1⟩.\nGenerates quantum entanglement.", GREEN)
    ]

    for idx, (gname, gdesc, col) in enumerate(gates):
        c = idx % 2
        r = idx // 2
        x = Inches(0.8 + c * 5.9)
        y = Inches(1.8 + r * 2.5)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = col
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        p0 = tf.paragraphs[0]
        p0.text = gname
        p0.font.bold = True
        p0.font.size = Pt(14)
        p0.font.color.rgb = col
        p1 = tf.add_paragraph()
        p1.text = gdesc
        p1.font.size = Pt(11.5)
        p1.font.color.rgb = SLATE_BODY
        p1.space_before = Pt(6)

    # =========================================================================
    # SLIDE 9: 4. PHYSICAL ARCHITECTURE (With Diagram)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, LIGHT_BG)
    add_header(s9, "4. Physical Architecture of a Quantum Computer")

    # Left: Description
    add_card(s9, Inches(0.8), Inches(1.8), Inches(4.8), Inches(5.1),
             "Layered Architecture",
             [
                 "Layer 1: Software & User Stack\n• High-level SDKs (Qiskit, Cirq, PennyLane)\n• Transpiler maps circuits to physical hardware.",
                 "Layer 2: Cryogenic Control\n• Microwave generators (4–8 GHz)\n• Low-noise HEMT & TWPA amplifiers\n• Attenuators isolate ambient thermal photons.",
                 "Layer 3: Quantum Hardware Core\n• Dilution Refrigerator operating at 15 milliKelvin\n• Superconducting Transmon Qubit lattice\n• Mu-metal magnetic shielding."
             ],
             border_color=ROYAL_BLUE)

    # Right: Embedded Architecture Diagram
    if os.path.exists('assets/quantum_system_architecture.png'):
        s9.shapes.add_picture('assets/quantum_system_architecture.png', Inches(5.8), Inches(1.8), width=Inches(6.7))

    # =========================================================================
    # SLIDE 10: DILUTION REFRIGERATION & EXTREME CRYOGENICS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10, LIGHT_BG)
    add_header(s10, "Cryogenics: The Dilution Refrigerator (15 milliKelvin)")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "Why Extreme Cold is Required",
             [
                 "Room temperature (300 K) contains violent thermal kinetic energy.",
                 "Thermal noise instantly destroys fragile quantum superpositions (thermal decoherence).",
                 "Superconductivity requires operating below the critical temperature (Tc) of metals like Niobium and Aluminum.",
                 "At 15 milliKelvin, thermal noise photons (k_B * T) are significantly smaller than the qubit transition frequency (h * f)."
             ],
             border_color=CYAN)

    add_card(s10, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "Refrigeration Mechanics",
             [
                 "Multi-Stage Golden Chandelier Structure:",
                 "• 50 Kelvin Flange (First heat shield)",
                 "• 4 Kelvin Plate (Pulse tube cooling)",
                 "• 0.8 Kelvin Still Plate (Helium distillation)",
                 "• 100 milliKelvin Cold Plate",
                 "• 15 milliKelvin Mixing Chamber Base Plate",
                 "Utilizes continuous circulation of rare Helium-3 and Helium-4 isotopes.",
                 "Colder than deep outer space (2.7 Kelvin) by a factor of 180x!"
             ],
             border_color=ROYAL_BLUE)

    # =========================================================================
    # SLIDE 11: PHYSICAL QUBIT MODALITIES
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11, LIGHT_BG)
    add_header(s11, "Leading Physical Qubit Technologies")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "1. Superconducting Transmon Qubits",
             [
                 "Pioneered by IBM, Google, Rigetti.",
                 "Printed circuits with Josephson Junctions acting as non-linear inductors.",
                 "Pros: Fast gate speeds (20–100 ns), scalable chip manufacturing.",
                 "Cons: Requires 15 mK dilution refrigerators; sensitive to charge noise."
             ],
             border_color=ROYAL_BLUE)

    add_card(s11, Inches(6.9), Inches(1.8), Inches(5.6), Inches(2.4),
             "2. Trapped-Ion Qubits",
             [
                 "Pioneered by IonQ, Quantinuum.",
                 "Individual charged atoms (Ytterbium/Barium) suspended in vacuum.",
                 "Pros: Identical natural qubits, longest coherence times (> minutes).",
                 "Cons: Slower gate speeds (microseconds); complex optical laser arrays."
             ],
             border_color=VIOLET)

    add_card(s11, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "3. Photonic Quantum Computing",
             [
                 "Pioneered by PsiQuantum, Xanadu.",
                 "Information encoded in polarization or squeeze states of light photons.",
                 "Pros: Operates at room temperature; immune to magnetic noise.",
                 "Cons: Photons do not naturally interact; requires non-linear optics."
             ],
             border_color=GREEN)

    add_card(s11, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.4),
             "4. Silicon Spin Qubits",
             [
                 "Pioneered by Intel, Silicon Quantum Computing.",
                 "Trapping electron spins inside artificial atoms (quantum dots).",
                 "Pros: Compatible with existing trillion-dollar silicon chip fabs.",
                 "Cons: Early developmental stage; sensitive to interface impurities."
             ],
             border_color=CYAN)

    # =========================================================================
    # SLIDE 12: 5. QUANTUM ALGORITHMS & SPEEDUP (With Diagram)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12, LIGHT_BG)
    add_header(s12, "5. Landmark Quantum Algorithms: Shor's & Grover's")

    # Left: Explanation
    add_card(s12, Inches(0.8), Inches(1.8), Inches(4.8), Inches(5.1),
             "Algorithmic Acceleration",
             [
                 "Shor's Algorithm (1994):\n• Converts prime factoring into period finding via Quantum Fourier Transform (QFT).\n• Polynomial speedup: O((log N)³).\n• Factoring 2048-bit RSA reduced from billions of years to hours!",
                 "Grover's Algorithm (1996):\n• Searches unstructured databases using amplitude amplification.\n• Quadratic speedup: O(√N).\n• Searching 1 trillion records requires only 1 million queries instead of 500 billion!"
             ],
             border_color=ROYAL_BLUE)

    # Right: Embedded Speedup Diagram
    if os.path.exists('assets/quantum_algorithms_speedup.png'):
        s12.shapes.add_picture('assets/quantum_algorithms_speedup.png', Inches(5.8), Inches(1.8), width=Inches(6.7))

    # =========================================================================
    # SLIDE 13: 6. APPLICATION: CRYPTOGRAPHY & POST-QUANTUM CRYPTOGRAPHY
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13, LIGHT_BG)
    add_header(s13, "6. Real-World Impact: Cryptography & Security (PQC)")

    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "The Quantum Threat: 'Q-Day'",
             [
                 "Public-Key Cryptography (RSA, ECC, Diffie-Hellman) powers global internet security (HTTPS, banking, VPNs, blockchains).",
                 "All depend on the difficulty of prime factorization or discrete logs.",
                 "A fault-tolerant quantum computer with ~4,000 logical qubits can break RSA-2048 in minutes.",
                 "'Harvest Now, Decrypt Later': Adversaries are intercepting and storing encrypted data today to decrypt once quantum machines mature."
             ],
             border_color=RGBColor(220, 38, 38)) # Red accent

    add_card(s13, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "The Solution: Post-Quantum Cryptography",
             [
                 "National Institute of Standards and Technology (NIST) finalized the first post-quantum encryption standards in 2024.",
                 "Lattice-Based Cryptography: ML-KEM (Kyber) and ML-DSA (Dilithium) rely on high-dimensional vector math impossible for quantum computers to solve.",
                 "Quantum Key Distribution (QKD): Uses quantum entanglement to exchange cryptographic keys; eavesdropping collapses the state, exposing attackers immediately.",
                 "Urgent Need: Organizations must transition to quantum-safe algorithms before Q-Day."
             ],
             border_color=GREEN)

    # =========================================================================
    # SLIDE 14: APPLICATION: CHEMISTRY & DRUG DISCOVERY
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14, LIGHT_BG)
    add_header(s14, "6. Real-World Impact: Molecular Chemistry & Drug Design")

    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "The Molecular Simulation Bottleneck",
             [
                 "Molecules are fundamentally quantum systems governed by electron wavefunctions.",
                 "Exact classical simulation of a modest caffeine molecule (C8 H10 N4 O2) requires 10^48 bits—more than all classical storage on Earth.",
                 "Pharmaceutical development currently relies on slow, expensive physical trial-and-error laboratory synthesis taking 10–15 years per drug.",
                 "Classical approximations fail to predict enzyme binding and catalytic transitions accurately."
             ],
             border_color=ROYAL_BLUE)

    add_card(s14, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "The Quantum Advantage",
             [
                 "Variational Quantum Eigensolver (VQE): Solves molecular ground-state energies directly on quantum hardware.",
                 "Targeted Oncology & Therapeutics: Simulates drug-protein interactions accurately, slashing development cycles from years to days.",
                 "Green Energy: Simulating nitrogenase enzymes could replace the energy-intensive Haber-Bosch fertilizer process (which consumes 2% of global energy).",
                 "Next-Gen Batteries: Designing solid-state lithium-metal battery chemistries for extended electric vehicle range."
             ],
             border_color=VIOLET)

    # =========================================================================
    # SLIDE 15: APPLICATION: FINANCE, LOGISTICS & QUANTUM ML
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_bg(s15, LIGHT_BG)
    add_header(s15, "6. Real-World Impact: Finance, Logistics & Quantum AI")

    add_card(s15, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.1),
             "Financial Engineering",
             [
                 "Quantum Monte Carlo algorithms offer quadratic speedup for pricing derivatives and portfolio risk.",
                 "Arbitrage Detection: Identifying instantaneous price discrepancies across global stock exchanges.",
                 "Actively explored by JPMorgan Chase, Goldman Sachs, and Barclays."
             ],
             border_color=ROYAL_BLUE)

    add_card(s15, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.1),
             "Supply Chain & Logistics",
             [
                 "Solving NP-Hard combinatorial optimization problems.",
                 "Quantum Approximate Optimization Algorithm (QAOA) for Traveling Salesperson Problem (TSP).",
                 "Airport runway scheduling, global cargo routing, and electrical grid load balancing."
             ],
             border_color=VIOLET)

    add_card(s15, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.1),
             "Quantum Machine Learning",
             [
                 "Mapping complex training data into exponentially large Hilbert feature spaces.",
                 "Quantum Support Vector Machines (QSVM) and Quantum Neural Networks (QNN).",
                 "Accelerates drug toxicity classification and financial fraud detection."
             ],
             border_color=CYAN)

    # =========================================================================
    # SLIDE 16: 7. CHALLENGES & QUANTUM ERROR CORRECTION
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_bg(s16, LIGHT_BG)
    add_header(s16, "7. Current Challenges: Noise, Decoherence & QEC")

    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "Physical Bottlenecks",
             [
                 "Quantum Decoherence: Fragile superposition states decay within 50 to 200 microseconds due to stray heat, radiation, and vibrations.",
                 "High Gate Error Rates: Physical two-qubit gate fidelities hover around 99% (1 error per 100 operations), compared to 1 error per 10^18 operations in classical silicon.",
                 "The Wiring Bottleneck: Routing thousands of individual coaxial microwave cables into a dilution refrigerator creates unmanageable physical heat loads.",
                 "Crosstalk: Neighboring qubits unintentionally interfere with each other during pulsing."
             ],
             border_color=RGBColor(220, 38, 38))

    add_card(s16, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "Quantum Error Correction (QEC)",
             [
                 "Surface Codes: Physical qubits are arranged in a 2D checkerboard grid.",
                 "Logical Qubit Synthesis: Hundreds of physical qubits work collectively to encode ONE clean 'Logical Qubit'.",
                 "Syndrome Measurements: Detects bit-flip (X) and phase-flip (Z) errors without measuring or collapsing the stored data.",
                 "Scaling Goal: Transition from today's Noisy Intermediate-Scale Quantum (NISQ) systems to Fault-Tolerant Quantum Supercomputers by the 2030s."
             ],
             border_color=GREEN)

    # =========================================================================
    # SLIDE 17: 8. FUTURE SCOPE & NATIONAL QUANTUM MISSION (INDIA)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_bg(s17, LIGHT_BG)
    add_header(s17, "8. Future Scope & India's National Quantum Mission")

    add_card(s17, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "National Quantum Mission (NQM - India)",
             [
                 "Approved in April 2023 with a budget outlay of ₹6,003 Crore (~$730 Million USD) over 2023–2031.",
                 "Target Milestones:",
                 "• Develop 50 to 1,000 physical qubit quantum computers on superconducting and photonic platforms.",
                 "• Deploy 2,000 km satellite-based secure quantum communication network across India.",
                 "• Establish 4 Thematic Hubs (T-Hubs) in Quantum Computing, Communication, Sensing, and Materials.",
                 "Positions India among the top 6 global quantum technology powers alongside the US, China, and EU."
             ],
             border_color=ROYAL_BLUE)

    add_card(s17, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "Career Pathways for BCA & IT Students",
             [
                 "Quantum Software Engineer: Design and optimize circuits using Python (Qiskit, Cirq, PennyLane).",
                 "Quantum Cloud Architect: Managing hybrid cloud infrastructure bridging classical HPC with QPUs.",
                 "Post-Quantum Security Specialist: Auditing enterprise cryptographic algorithms and migrating legacy ciphers to PQC.",
                 "Free Cloud Access Today: IBM Quantum Platform and AWS Braket allow students to run real quantum algorithms on physical QPUs for free."
             ],
             border_color=VIOLET)

    # =========================================================================
    # SLIDE 18: 9. CONCLUSION
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_bg(s18, LIGHT_BG)
    add_header(s18, "9. Conclusion: The Second Quantum Revolution")

    add_card(s18, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.1),
             "Summary of Findings & Strategic Outlook",
             [
                 "A Fundamental Shift in Computation: Quantum computing is not just an incremental speed boost for classical computers; it is an entirely new dimension of human problem-solving based on quantum mechanics.",
                 "Power of Quantum Parallelism: Harnessing Superposition and Entanglement allows evaluating 2^N state spaces simultaneously, while Quantum Interference extracts the single correct answer.",
                 "Near-Term Horizon (NISQ Era): Hybrid algorithms (VQE, QAOA) are already demonstrating tangible industrial advantages in molecular chemistry, material science, and portfolio optimization.",
                 "Long-Term Horizon (Fault-Tolerant Era): Scaled logical qubits will revolutionize cybersecurity through Post-Quantum Cryptography and solve currently intractable global scientific challenges.",
                 "Call to Action for ITM Students: With India's National Quantum Mission underway, mastering quantum programming languages like Qiskit today prepares BCA graduates to lead the next computational frontier."
             ],
             border_color=NAVY_BLUE)

    # =========================================================================
    # SLIDE 19: REFERENCES
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_bg(s19, LIGHT_BG)
    add_header(s19, "Bibliography & Academic References")

    refs_left = [
        "1. Feynman, R. P. (1982). 'Simulating physics with computers.' Int. J. Theor. Phys., 21(6/7), 467-488.",
        "2. Deutsch, D. (1985). 'Quantum theory and the universal quantum computer.' Proc. R. Soc. Lond. A, 400, 97-117.",
        "3. Shor, P. W. (1994). 'Algorithms for quantum computation: discrete logs and factoring.' IEEE FOCS, 124-134.",
        "4. Grover, L. K. (1996). 'A fast quantum mechanical algorithm for database search.' ACM STOC, 212-219.",
        "5. Nielsen, M. A., & Chuang, I. L. (2010). 'Quantum Computation and Quantum Information.' Cambridge Univ. Press."
    ]
    refs_right = [
        "6. Preskill, J. (2018). 'Quantum computing in the NISQ era and beyond.' Quantum, 2, 79.",
        "7. Arute, F. et al. (Google Quantum AI) (2019). 'Quantum supremacy using a superconducting processor.' Nature, 574, 505-510.",
        "8. IBM Quantum. (2024). 'Qiskit Software Development Kit.' https://qiskit.org",
        "9. NIST. (2024). 'Post-Quantum Cryptography Standards (ML-KEM, ML-DSA).' https://csrc.nist.gov",
        "10. Dept. of Science and Technology (DST), Govt. of India. (2023). 'National Quantum Mission (NQM).' https://dst.gov.in"
    ]

    add_card(s19, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
             "Classical Foundations", refs_left, border_color=ROYAL_BLUE)
    add_card(s19, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1),
             "Contemporary Milestones & Standards", refs_right, border_color=VIOLET)

    # =========================================================================
    # SLIDE 20: Q&A / THANK YOU (Dark Theme)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_bg(s20, DARK_NAVY)

    dec_end = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.1), Inches(5.9))
    dec_end.fill.solid()
    dec_end.fill.fore_color.rgb = CYAN
    dec_end.line.fill.background()

    tb_end = s20.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.5), Inches(4.0))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    pe0 = tf_end.paragraphs[0]
    pe0.text = "THANK YOU!"
    pe0.font.name = "Arial"
    pe0.font.size = Pt(44)
    pe0.font.bold = True
    pe0.font.color.rgb = WHITE

    pe1 = tf_end.add_paragraph()
    pe1.text = "Questions & Answers / Discussion Session"
    pe1.font.name = "Calibri"
    pe1.font.size = Pt(20)
    pe1.font.color.rgb = CYAN
    pe1.space_before = Pt(8)

    pe2 = tf_end.add_paragraph()
    pe2.text = "Presented by:\n" \
               "Pratyush Mishra (Leader - 2514018680059)  |  Atul Upadhyay (2514018680041)\n" \
               "Divyanshu Upadhyay (2514018680045)  |  Adesh Bhatt (2514018680026)\n\n" \
               "Guided By: Ms. Vinita Yadav\n" \
               "ITM College of Science and Management, GIDA, Gorakhpur (DDU Gorakhpur University)"
    pe2.font.name = "Calibri"
    pe2.font.size = Pt(14)
    pe2.font.color.rgb = RGBColor(203, 213, 225)
    pe2.space_before = Pt(20)

    output_pptx = "Quantum_Computing_Seminar_Presentation.pptx"
    prs.save(output_pptx)
    print(f"Presentation saved successfully as '{output_pptx}'")

if __name__ == '__main__':
    create_presentation()

