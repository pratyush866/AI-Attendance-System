"""
Script to generate ultra-high-resolution, publication-grade academic architectural diagrams
for the BCA Final Project Report:
AI-Based Smart Student Attendance System Using Face Recognition, Voice Authentication & Dual-Verification
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('assets', exist_ok=True)

# -----------------------------------------------------------------------------
# 1. SYSTEM ARCHITECTURE DIAGRAM (Figure 10.1 / Figure 3.1)
# -----------------------------------------------------------------------------
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(13, 9), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')

    # Title Banner
    ax.text(6.5, 8.65, "SYSTEM ARCHITECTURE: AI-BASED SMART ATTENDANCE SYSTEM", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#0F172A', fontfamily='sans-serif')
    ax.text(6.5, 8.35, "Three-Tier Client-Server Architecture with Dual-Biometric Verification & Anti-Bunk Engine", 
            fontsize=10, fontstyle='italic', ha='center', va='center', color='#475569', fontfamily='sans-serif')

    # TIER 1: CLIENT LAYER
    rect_tier1 = patches.FancyBboxPatch((0.5, 6.4), 12.0, 1.65, boxstyle="round,pad=0.1,rounding_size=0.15", 
                                        ec="#3B82F6", fc="#EFF6FF", lw=2, linestyle='-')
    ax.add_patch(rect_tier1)
    ax.text(0.8, 7.8, "CLIENT LAYER (Presentation & User Interface)", fontsize=11, fontweight='bold', color='#1D4ED8')
    
    # Client Components
    clients = [
        ("Student Web Portal", "Self-Registration, Profile,\nPIN Entry & Live Selfie Upload", 1.0),
        ("Teacher Management Console", "Session Creation, 4-Digit PIN,\nQR Generator & Classroom Photo", 4.9),
        ("Administrator Dashboard", "User Accounts, Department Analytics,\nAudit Logs & Report Export", 8.8)
    ]
    for title, desc, x_pos in clients:
        box = patches.FancyBboxPatch((x_pos, 6.6), 3.2, 0.95, boxstyle="round,pad=0.08,rounding_size=0.1", 
                                     ec="#93C5FD", fc="#FFFFFF", lw=1.5)
        ax.add_patch(box)
        ax.text(x_pos + 1.6, 7.25, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#1E3A8A')
        ax.text(x_pos + 1.6, 6.85, desc, fontsize=7.5, ha='center', va='center', color='#334155')

    # Arrow Down from Tier 1 to Tier 2
    for ax_x in [2.6, 6.5, 10.4]:
        ax.annotate('', xy=(ax_x, 5.75), xytext=(ax_x, 6.4),
                    arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=2, mutation_scale=15))

    # TIER 2: APPLICATION & AI PROCESSING LAYER
    rect_tier2 = patches.FancyBboxPatch((0.5, 2.5), 12.0, 3.2, boxstyle="round,pad=0.1,rounding_size=0.15", 
                                        ec="#6366F1", fc="#EEF2FF", lw=2, linestyle='-')
    ax.add_patch(rect_tier2)
    ax.text(0.8, 5.45, "APPLICATION LAYER (Core Processing & Biometric AI Engines)", fontsize=11, fontweight='bold', color='#4338CA')

    # App Components
    app_modules = [
        ("Authentication & Security", "• bcrypt Password Hashing\n• Role-Based Access Control (RBAC)\n• Session Security & CSRF Token", 0.9, 4.0, 3.4, 1.15, "#C7D2FE", "#312E81"),
        ("Attendance Logic Controller", "• 4-Digit Session PIN Validator\n• Dynamic QR Token (Segno)\n• Timed Attendance Window Check", 4.8, 4.0, 3.4, 1.15, "#C7D2FE", "#312E81"),
        ("Reporting & Analytics Engine", "• Pandas Aggregation Pipeline\n• Attendance % Calculations\n• CSV / Excel Report Exporter", 8.7, 4.0, 3.4, 1.15, "#C7D2FE", "#312E81"),
        ("Face Recognition Engine", "• Dlib 68 Facial Landmark Detection\n• 128D ResNet Biometric Embeddings\n• Euclidean Distance Matching (d <= 0.58)", 0.9, 2.65, 3.4, 1.15, "#FBCFE8", "#831843"),
        ("Voice Authentication Engine", "• Librosa FFT Audio Preprocessing\n• Resemblyzer 256D d-vector Model\n• Cosine Similarity Verification", 4.8, 2.65, 3.4, 1.15, "#FDE68A", "#78350F"),
        ("Dual-Verification Anti-Bunk Engine", "• Student Selfie vs. Profile Cross-Match\n• Classroom Wide Photo Face Detection\n• Classroom Presence Corroboration", 8.7, 2.65, 3.4, 1.15, "#A7F3D0", "#064E3B"),
    ]
    for title, desc, x_pos, y_pos, w, h, border_c, text_c in app_modules:
        box = patches.FancyBboxPatch((x_pos, y_pos), w, h, boxstyle="round,pad=0.08,rounding_size=0.1", 
                                     ec=border_c, fc="#FFFFFF", lw=1.5)
        ax.add_patch(box)
        ax.text(x_pos + w/2, y_pos + h - 0.22, title, fontsize=9, fontweight='bold', ha='center', va='center', color=text_c)
        ax.text(x_pos + w/2, y_pos + (h - 0.22)/2, desc, fontsize=7.2, ha='center', va='center', color='#334155', linespacing=1.2)

    # Arrow Down from Tier 2 to Tier 3
    for ax_x in [2.6, 6.5, 10.4]:
        ax.annotate('', xy=(ax_x, 1.85), xytext=(ax_x, 2.5),
                    arrowprops=dict(arrowstyle="->", color="#6366F1", lw=2, mutation_scale=15))

    # TIER 3: DATA & STORAGE LAYER
    rect_tier3 = patches.FancyBboxPatch((0.5, 0.4), 12.0, 1.4, boxstyle="round,pad=0.1,rounding_size=0.15", 
                                        ec="#10B981", fc="#ECFDF5", lw=2, linestyle='-')
    ax.add_patch(rect_tier3)
    ax.text(0.8, 1.6, "DATA STORAGE LAYER (Centralized Relational & Biometric Repositories)", fontsize=11, fontweight='bold', color='#047857')

    data_stores = [
        ("Cloud PostgreSQL (Supabase)", "Users, Teachers, Subjects, Encodings,\nAttendance Records & Audit Trails", 1.0),
        ("Local SQLite Database Engine", "High-Speed Standalone Local Replica,\nZero-Latency Classroom Fallback", 4.9),
        ("Media & Biometric Vault", "128D Face Vectors, 256D Voice Embeddings,\nLive Session Selfies & Class Photos", 8.8)
    ]
    for title, desc, x_pos in data_stores:
        box = patches.FancyBboxPatch((x_pos, 0.55), 3.2, 0.85, boxstyle="round,pad=0.08,rounding_size=0.1", 
                                     ec="#6EE7B7", fc="#FFFFFF", lw=1.5)
        ax.add_patch(box)
        ax.text(x_pos + 1.6, 1.1, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#065F46')
        ax.text(x_pos + 1.6, 0.78, desc, fontsize=7.5, ha='center', va='center', color='#334155')

    plt.tight_layout()
    plt.savefig('assets/architecture_diagram.png', dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Generated assets/architecture_diagram.png successfully!")

# -----------------------------------------------------------------------------
# 2. DUAL-VERIFICATION ANTI-BUNK WORKFLOW DIAGRAM
# -----------------------------------------------------------------------------
def generate_dual_verification_flow():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(6.5, 7.6, "DUAL-VERIFICATION ANTI-BUNK ATTENDANCE PROTOCOL", 
            fontsize=14, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(6.5, 7.25, "Sequential Verification: Live Classroom Selfie + Teacher Panoramic Photo Cross-Match", 
            fontsize=9.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # Workflow Steps
    # Step 1: Teacher starts session
    b1 = patches.FancyBboxPatch((0.6, 5.0), 3.2, 1.6, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#2563EB", fc="#EFF6FF", lw=1.8)
    ax.add_patch(b1)
    ax.text(2.2, 6.2, "STEP 1: SESSION INITIATION", fontsize=9.5, fontweight='bold', ha='center', color='#1E40AF')
    ax.text(2.2, 5.5, "• Teacher opens subject portal\n• Generates 4-digit PIN\n• Displays Dynamic QR in room\n• Session timer starts (e.g., 5 min)", fontsize=8, ha='center', color='#1E293B')

    # Arrow 1 -> 2
    ax.annotate('', xy=(4.6, 5.8), xytext=(3.9, 5.8),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2, mutation_scale=15))

    # Step 2: Student Selfie
    b2 = patches.FancyBboxPatch((4.7, 5.0), 3.4, 1.6, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#7C3AED", fc="#F5F3FF", lw=1.8)
    ax.add_patch(b2)
    ax.text(6.4, 6.2, "STEP 2: STUDENT IN-CLASS SELFIE", fontsize=9.5, fontweight='bold', ha='center', color='#5B21B6')
    ax.text(6.4, 5.5, "• Student enters 4-digit PIN\n• In-app camera captures live selfie\n• Face encodings extracted (128D)\n• Matched with student biometric profile", fontsize=8, ha='center', color='#1E293B')

    # Arrow 2 -> 3
    ax.annotate('', xy=(8.9, 5.8), xytext=(8.2, 5.8),
                arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=2, mutation_scale=15))

    # Step 3: Teacher Classroom Photo
    b3 = patches.FancyBboxPatch((9.0, 5.0), 3.4, 1.6, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#059669", fc="#ECFDF5", lw=1.8)
    ax.add_patch(b3)
    ax.text(10.7, 6.2, "STEP 3: TEACHER CLASS PHOTO", fontsize=9.5, fontweight='bold', ha='center', color='#065F46')
    ax.text(10.7, 5.5, "• Teacher snaps wide classroom photo\n• Captures all seated students\n• Uploads directly to session portal\n• Trigger AI Cross-Verification", fontsize=8, ha='center', color='#1E293B')

    # Arrow Down from Step 3 to AI Engine
    ax.annotate('', xy=(6.5, 4.2), xytext=(6.5, 4.8),
                arrowprops=dict(arrowstyle="->", color="#0F172A", lw=2, mutation_scale=15))

    # Center Box: AI Cross-Matching Engine
    b_ai = patches.FancyBboxPatch((3.0, 2.5), 7.0, 1.6, boxstyle="round,pad=0.1,rounding_size=0.15", ec="#D97706", fc="#FFFBEB", lw=2.2)
    ax.add_patch(b_ai)
    ax.text(6.5, 3.75, "AI DUAL-VERIFICATION CROSS-MATCHING ENGINE", fontsize=10.5, fontweight='bold', ha='center', color='#92400E')
    ax.text(6.5, 3.05, "1. Detect all faces in Teacher's classroom panoramic photo using Dlib HOG\n"
                       "2. Compute 128D embeddings for all detected classroom attendees\n"
                       "3. Cross-compare Student's live selfie vector against classroom face pool\n"
                       "4. Evaluate Euclidean Distance: Match if min(distance) <= 0.58 threshold", 
            fontsize=8.2, ha='center', color='#78350F')

    # Branch Left: Verified Present
    ax.annotate('', xy=(2.5, 1.6), xytext=(4.5, 2.5),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=15))
    b_yes = patches.FancyBboxPatch((0.6, 0.4), 4.2, 1.2, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#059669", fc="#D1FAE5", lw=2)
    ax.add_patch(b_yes)
    ax.text(2.7, 1.15, "VERIFIED PRESENT [SUCCESS]", fontsize=10, fontweight='bold', ha='center', color='#065F46')
    ax.text(2.7, 0.7, "• Student face found in Classroom Photo\n• Attendance Logged: 'PRESENT'\n• Timestamp & Session ID secured", fontsize=7.8, ha='center', color='#064E3B')

    # Branch Right: Bunk / Proxy Detected
    ax.annotate('', xy=(10.5, 1.6), xytext=(8.5, 2.5),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2, mutation_scale=15))
    b_no = patches.FancyBboxPatch((8.2, 0.4), 4.2, 1.2, boxstyle="round,pad=0.1,rounding_size=0.12", ec="#DC2626", fc="#FEE2E2", lw=2)
    ax.add_patch(b_no)
    ax.text(10.3, 1.15, "BUNK / PROXY DETECTED [REJECT]", fontsize=10, fontweight='bold', ha='center', color='#991B1B')
    ax.text(10.3, 0.7, "• Student took selfie but NOT in room\n• Attendance Marked: 'ABSENT / FLAGGED'\n• Proxy attempt alerted to Teacher", fontsize=7.8, ha='center', color='#7F1D1D')

    plt.tight_layout()
    plt.savefig('assets/dual_verification_flow.png', dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Generated assets/dual_verification_flow.png successfully!")

# -----------------------------------------------------------------------------
# 3. DATABASE ENTITY-RELATIONSHIP (ER) DIAGRAM
# -----------------------------------------------------------------------------
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(6.5, 7.6, "DATABASE ENTITY-RELATIONSHIP (ER) DIAGRAM", 
            fontsize=14, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(6.5, 7.25, "Relational Schema: Centralized Attendance & Biometric Storage Architecture", 
            fontsize=9.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # Entities
    tables = [
        ("TEACHERS", [
            ("id", "UUID / INT (PK)"),
            ("name", "VARCHAR(100)"),
            ("email", "VARCHAR(100) UNIQUE"),
            ("password_hash", "VARCHAR(255)"),
            ("department", "VARCHAR(100)"),
            ("created_at", "TIMESTAMP")
        ], 0.6, 4.0, 3.4, 2.8, "#1E3A8A", "#DBEAFE"),

        ("SUBJECTS", [
            ("id", "UUID / INT (PK)"),
            ("teacher_id", "UUID / INT (FK)"),
            ("subject_code", "VARCHAR(20)"),
            ("subject_name", "VARCHAR(100)"),
            ("semester", "VARCHAR(20)"),
            ("created_at", "TIMESTAMP")
        ], 4.8, 4.0, 3.4, 2.8, "#047857", "#D1FAE5"),

        ("STUDENTS", [
            ("id", "UUID / INT (PK)"),
            ("roll_no", "VARCHAR(50) UNIQUE"),
            ("name", "VARCHAR(100)"),
            ("email", "VARCHAR(100)"),
            ("face_encoding", "TEXT / FLOAT[128]"),
            ("voice_embedding", "TEXT / FLOAT[256]")
        ], 9.0, 4.0, 3.4, 2.8, "#7C2D12", "#FFEDD5"),

        ("ATTENDANCE_SESSIONS", [
            ("id", "UUID / INT (PK)"),
            ("teacher_id", "UUID / INT (FK)"),
            ("subject_id", "UUID / INT (FK)"),
            ("session_pin", "VARCHAR(6)"),
            ("classroom_image", "TEXT / PATH"),
            ("status", "VARCHAR(20)"),
            ("created_at", "TIMESTAMP")
        ], 0.6, 0.5, 3.4, 2.9, "#4338CA", "#E0E7FF"),

        ("SESSION_SELFIES", [
            ("id", "UUID / INT (PK)"),
            ("session_id", "UUID / INT (FK)"),
            ("student_id", "UUID / INT (FK)"),
            ("selfie_path", "TEXT"),
            ("verification_status", "VARCHAR(20)"),
            ("submitted_at", "TIMESTAMP")
        ], 4.8, 0.5, 3.4, 2.9, "#6D28D9", "#EDE9FE"),

        ("ATTENDANCE_LOGS", [
            ("id", "UUID / INT (PK)"),
            ("session_id", "UUID / INT (FK)"),
            ("student_id", "UUID / INT (FK)"),
            ("status", "VARCHAR(20) [PRESENT/ABSENT]"),
            ("method", "VARCHAR(50) [DUAL_VERIFY]"),
            ("timestamp", "TIMESTAMP")
        ], 9.0, 0.5, 3.4, 2.9, "#BE123C", "#FFE4E6")
    ]

    for title, fields, x, y, w, h, header_c, bg_c in tables:
        # Table card
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.1", ec=header_c, fc="#FFFFFF", lw=1.5)
        ax.add_patch(card)
        # Header banner
        header = patches.FancyBboxPatch((x, y + h - 0.55), w, 0.55, boxstyle="round,pad=0.05,rounding_size=0.08", ec=header_c, fc=header_c, lw=1)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.28, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color="#FFFFFF")
        
        # Fields
        for idx, (fname, ftype) in enumerate(fields):
            f_y = y + h - 0.95 - (idx * 0.35)
            is_key = "PK" in ftype or "FK" in ftype
            key_tag = "[PK] " if "PK" in ftype else ("[FK] " if "FK" in ftype else "     ")
            f_color = "#1E40AF" if is_key else "#334155"
            f_weight = 'bold' if is_key else 'normal'
            ax.text(x + 0.15, f_y, f"{key_tag}{fname}", fontsize=7.8, fontweight=f_weight, color=f_color, va='center')
            ax.text(x + w - 0.15, f_y, ftype.split()[0], fontsize=7.2, color='#64748B', ha='right', va='center')

    # Draw Relationship Connectors
    # 1. Teachers -> Subjects (1:N)
    ax.annotate('', xy=(4.8, 5.4), xytext=(4.0, 5.4),
                arrowprops=dict(arrowstyle="->", color="#047857", lw=1.8))
    ax.text(4.4, 5.55, "1 : N", fontsize=7.5, fontweight='bold', ha='center', color='#047857')

    # 2. Subjects -> Attendance Sessions (1:N)
    ax.annotate('', xy=(2.3, 3.4), xytext=(4.8, 4.3),
                arrowprops=dict(arrowstyle="->", color="#4338CA", lw=1.8, connectionstyle="arc3,rad=-0.1"))
    ax.text(3.3, 3.9, "1 : N", fontsize=7.5, fontweight='bold', ha='center', color='#4338CA')

    # 3. Attendance Sessions -> Session Selfies (1:N)
    ax.annotate('', xy=(4.8, 1.95), xytext=(4.0, 1.95),
                arrowprops=dict(arrowstyle="->", color="#6D28D9", lw=1.8))
    ax.text(4.4, 2.1, "1 : N", fontsize=7.5, fontweight='bold', ha='center', color='#6D28D9')

    # 4. Session Selfies -> Attendance Logs (1:1 / 1:N)
    ax.annotate('', xy=(9.0, 1.95), xytext=(8.2, 1.95),
                arrowprops=dict(arrowstyle="->", color="#BE123C", lw=1.8))
    ax.text(8.6, 2.1, "1 : 1", fontsize=7.5, fontweight='bold', ha='center', color='#BE123C')

    # 5. Students -> Session Selfies (1:N)
    ax.annotate('', xy=(6.5, 3.4), xytext=(9.0, 4.3),
                arrowprops=dict(arrowstyle="->", color="#7C2D12", lw=1.8, connectionstyle="arc3,rad=-0.1"))
    ax.text(7.6, 3.9, "1 : N", fontsize=7.5, fontweight='bold', ha='center', color='#7C2D12')

    plt.tight_layout()
    plt.savefig('assets/er_diagram.png', dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Generated assets/er_diagram.png successfully!")

# -----------------------------------------------------------------------------
# 4. DATA FLOW DIAGRAM (DFD LEVEL 1)
# -----------------------------------------------------------------------------
def generate_dfd_diagram():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(6.5, 7.6, "DATA FLOW DIAGRAM (DFD LEVEL 1)", 
            fontsize=14, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(6.5, 7.25, "Information Flow: Biometric Enrollment, Session Processing & Dual-Verification", 
            fontsize=9.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # Entities (Squares)
    def draw_entity(x, y, name):
        box = patches.Rectangle((x, y), 2.2, 1.0, ec="#1E3A8A", fc="#EFF6FF", lw=1.8)
        ax.add_patch(box)
        ax.text(x + 1.1, y + 0.5, name, fontsize=9.5, fontweight='bold', ha='center', va='center', color="#1E3A8A")

    draw_entity(0.5, 5.0, "STUDENT\n(Client)")
    draw_entity(0.5, 1.8, "TEACHER\n(Client)")
    draw_entity(10.3, 1.8, "ADMIN\n(Console)")

    # Processes (Circles / Rounded)
    processes = [
        ("1.0", "Biometric\nEnrollment", 3.8, 5.0),
        ("2.0", "Class Session\nInitiation", 3.8, 1.8),
        ("3.0", "Dual-Biometric\nCross-Verify", 7.0, 3.4),
        ("4.0", "Attendance\nAnalytics & Export", 10.3, 5.0)
    ]
    for p_id, p_name, px, py in processes:
        circle = patches.FancyBboxPatch((px, py), 2.2, 1.0, boxstyle="round,pad=0.1,rounding_size=0.5", ec="#059669", fc="#ECFDF5", lw=1.8)
        ax.add_patch(circle)
        ax.text(px + 1.1, py + 0.65, f"Process {p_id}", fontsize=8, fontweight='bold', ha='center', va='center', color="#065F46")
        ax.text(px + 1.1, py + 0.35, p_name, fontsize=8, ha='center', va='center', color="#064E3B")

    # Data Stores (Open-ended rectangles)
    def draw_datastore(x, y, d_id, d_name):
        rect = patches.Rectangle((x, y), 3.0, 0.7, ec="#475569", fc="#F8FAFC", lw=1.5)
        ax.add_patch(rect)
        # Left bar
        ax.plot([x + 0.6, x + 0.6], [y, y + 0.7], color="#475569", lw=1.5)
        ax.text(x + 0.3, y + 0.35, d_id, fontsize=8, fontweight='bold', ha='center', va='center', color="#334155")
        ax.text(x + 1.8, y + 0.35, d_name, fontsize=8, ha='center', va='center', color="#1E293B")

    draw_datastore(6.6, 6.4, "D1", "Biometric Vectors (128D/256D)")
    draw_datastore(6.6, 1.0, "D2", "Attendance Sessions & Logs")

    # Connectors
    # Student -> 1.0
    ax.annotate('Face/Voice Samples', xy=(3.8, 5.6), xytext=(2.7, 5.6), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    # 1.0 -> D1
    ax.annotate('Store Encodings', xy=(6.6, 6.7), xytext=(5.6, 5.9), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))
    # Teacher -> 2.0
    ax.annotate('Class Code, PIN', xy=(3.8, 2.3), xytext=(2.7, 2.3), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    # 2.0 -> D2
    ax.annotate('Save Session', xy=(6.6, 1.3), xytext=(5.5, 1.8), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))
    # Student -> 3.0 (Selfie)
    ax.annotate('Live Selfie + PIN', xy=(7.0, 4.0), xytext=(2.7, 5.2), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    # Teacher -> 3.0 (Classroom photo)
    ax.annotate('Classroom Photo', xy=(7.0, 3.6), xytext=(2.7, 2.5), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    # D1 -> 3.0
    ax.annotate('Fetch Biometrics', xy=(8.0, 4.4), xytext=(8.0, 6.4), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    # 3.0 -> D2
    ax.annotate('Mark PRESENT / BUNK', xy=(8.1, 1.7), xytext=(8.1, 3.4), arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5))
    # D2 -> 4.0
    ax.annotate('Raw Logs', xy=(10.5, 5.0), xytext=(8.8, 1.7), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5, connectionstyle="arc3,rad=-0.2"))
    # 4.0 -> Admin
    ax.annotate('Excel/CSV Reports', xy=(11.4, 2.8), xytext=(11.4, 5.0), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))

    plt.tight_layout()
    plt.savefig('assets/dfd_level1_diagram.png', dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print("Generated assets/dfd_level1_diagram.png successfully!")

if __name__ == '__main__':
    generate_architecture_diagram()
    generate_dual_verification_flow()
    generate_er_diagram()
    generate_dfd_diagram()
    print("All architectural diagrams generated successfully!")

