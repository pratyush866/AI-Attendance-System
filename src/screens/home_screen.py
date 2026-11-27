import os
import streamlit as st
from src.components.footer import footer_home
from src.components.header import GRAD_CAP_SVG
from src.ui.base_layout import style_base_layout, style_background_home
from src.ui.image_utils import get_image_base64


@st.dialog("About SNAPCLASS — AI Attendance System")
def about_dialog():
    st.markdown("""
### 🎓 Dual-Verification Anti-Bunk Platform
**SNAPCLASS** eliminates proxy attendance and classroom bunking using **Dlib ResNet-34 128D Face Recognition** and **Resemblyzer 256D Voice Biometrics**.

**How Anti-Bunk Works:**
1. **Student Selfie Check-in:** Student enters a dynamic 4-digit classroom PIN and takes a live selfie.
2. **Faculty Classroom Photo:** Teacher captures a wide-angle panoramic photo of the seated class.
3. **AI Cross-Match:** Presence is marked **PRESENT** only when the student's face is confirmed inside the classroom snapshot.

---
**👥 Orbitals Project Team (BCA Final Year — ITM College, Gorakhpur)**
- **Pratyush Mishra** *(Team Leader)* — Roll: `2514018680059`
- **Atul Upadhyay** — Roll: `2514018680041`
- **Divyanshu Upadhyay** — Roll: `2514018680045`
- **Adesh Bhatt** — Roll: `2514018680026`
- **Mo Ashad** — Roll: `2514018680055`
- **Project Guide:** **Ms. Vinita Yadav** *(Dept. of Computer Applications)*
""")


@st.dialog("Quick Start Guide — How to Use")
def help_dialog():
    st.markdown("""
### 👨‍🎓 For Students
1. Click **Student Login →** on the Student card.
2. Scan your face with **FaceID Scanner** (first-time users can enroll their face & roll number right there).
3. Join your subject using the **Subject Code** shared by your teacher.
4. During class, scan the teacher's QR or enter the **4-digit PIN** and take a live selfie.

### 👨‍🏫 For Faculty
1. Click **Faculty Login →** on the Teacher card *(Demo account pre-filled: `prof_roy` / `admin123`)*.
2. Create a subject or pick an existing subject, then click **Launch Attendance Session**.
3. Share the **4-digit PIN / QR** with seated students.
4. Snap & upload the **Classroom Photo** to automatically verify every student and export Excel/CSV reports!
""")


def _hero_face_hud_html():
    return """
<div style="position:relative;border-radius:26px;padding:18px;background:linear-gradient(145deg,rgba(124,58,237,0.16) 0%,rgba(99,102,241,0.22) 55%,rgba(56,189,248,0.16) 100%);border:1px solid rgba(167,139,250,0.4);box-shadow:0 24px 50px -15px rgba(79,70,229,0.25);overflow:hidden;min-height:295px;display:flex;align-items:center;justify-content:center;">
<style>
@keyframes scanBeam {
  0% { transform: translateY(-62px); opacity: 0.2; }
  50% { transform: translateY(62px); opacity: 0.95; }
  100% { transform: translateY(-62px); opacity: 0.2; }
}
.snap-scan-line { animation: scanBeam 2.8s ease-in-out infinite; }
</style>
<svg viewBox="0 0 420 270" width="100%" style="max-width:420px;display:block;" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="bgSky" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#4c1d95" stop-opacity="0.78"/>
<stop offset="55%" stop-color="#4338ca" stop-opacity="0.82"/>
<stop offset="100%" stop-color="#312e81" stop-opacity="0.92"/>
</linearGradient>
<linearGradient id="cyanGlow" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#22d3ee"/>
<stop offset="100%" stop-color="#38bdf8"/>
</linearGradient>
<filter id="neon" x="-30%" y="-30%" width="160%" height="160%">
<feGaussianBlur stdDeviation="3.5" result="blur"/>
<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>
<rect width="420" height="270" rx="20" fill="url(#bgSky)"/>
<!-- Subtle Campus Skyline Silhouette -->
<path d="M0 225 L35 225 L35 165 L88 165 L88 225 L105 225 L105 140 L170 140 L170 225 L260 225 L260 155 L320 155 L320 225 L350 225 L350 175 L420 175 L420 270 L0 270 Z" fill="#1e1b4b" fill-opacity="0.45"/>
<!-- Decorative Dot Matrix -->
<g fill="#c4b5fd" fill-opacity="0.35">
<circle cx="360" cy="30" r="2.2"/><circle cx="375" cy="30" r="2.2"/><circle cx="390" cy="30" r="2.2"/>
<circle cx="360" cy="45" r="2.2"/><circle cx="375" cy="45" r="2.2"/><circle cx="390" cy="45" r="2.2"/>
<circle cx="360" cy="60" r="2.2"/><circle cx="375" cy="60" r="2.2"/><circle cx="390" cy="60" r="2.2"/>
</g>
<!-- Stylized Smiling Student Silhouette / Bust -->
<path d="M128 270 C128 215, 165 194, 200 194 C235 194, 272 215, 272 270 Z" fill="#e0e7ff"/>
<path d="M174 194 L200 226 L226 194" fill="#c7d2fe"/>
<rect x="186" y="168" width="28" height="32" rx="12" fill="#fed7aa"/>
<!-- Hair Back -->
<ellipse cx="200" cy="116" rx="54" ry="62" fill="#1e1b4b"/>
<!-- Face -->
<ellipse cx="200" cy="122" rx="42" ry="50" fill="#fde6d2"/>
<!-- Hair Bangs -->
<path d="M158 112 C160 72, 240 72, 242 112 C230 88, 175 88, 158 112 Z" fill="#1e1b4b"/>
<!-- Eyes & Smile -->
<circle cx="183" cy="118" r="3.4" fill="#1e293b"/>
<circle cx="217" cy="118" r="3.4" fill="#1e293b"/>
<path d="M187 141 Q200 151 213 141" stroke="#be185d" stroke-width="2.6" stroke-linecap="round" fill="none"/>
<!-- 68-Point AI Facial Landmark Mesh Overlay -->
<g stroke="#67e8f9" stroke-width="0.9" stroke-opacity="0.72" fill="none">
<polygon points="183,118 200,112 217,118 200,132"/>
<polygon points="183,118 168,128 187,143 200,132"/>
<polygon points="217,118 232,128 213,143 200,132"/>
<polyline points="165,112 170,138 184,154 200,160 216,154 230,138 235,112"/>
</g>
<g fill="#ffffff" filter="url(#neon)">
<circle cx="183" cy="118" r="2.2"/><circle cx="217" cy="118" r="2.2"/>
<circle cx="200" cy="112" r="2.2"/><circle cx="200" cy="132" r="2.4"/>
<circle cx="187" cy="143" r="2.0"/><circle cx="213" cy="143" r="2.0"/>
<circle cx="168" cy="128" r="2.0"/><circle cx="232" cy="128" r="2.0"/>
<circle cx="200" cy="160" r="2.2"/>
</g>
<!-- Glowing Neon Cyan AI Bounding Box -->
<g stroke="url(#cyanGlow)" stroke-width="3.5" stroke-linecap="round" fill="none" filter="url(#neon)">
<path d="M132 82 V60 H156"/>
<path d="M268 82 V60 H244"/>
<path d="M132 162 V184 H156"/>
<path d="M268 162 V184 H244"/>
</g>
<!-- Animated Scan Beam -->
<line class="snap-scan-line" x1="136" y1="122" x2="264" y2="122" stroke="#22d3ee" stroke-width="2" stroke-opacity="0.85" filter="url(#neon)"/>
<!-- Status Pill Top-Left -->
<rect x="16" y="16" width="142" height="26" rx="13" fill="#0f172a" fill-opacity="0.72" stroke="#22d3ee" stroke-opacity="0.5"/>
<circle cx="30" cy="29" r="4" fill="#10b981"/>
<text x="41" y="33" fill="#ecfeff" font-family="Plus Jakarta Sans,sans-serif" font-size="10.5" font-weight="700">128D Vector Matched</text>
<!-- Cursive Callout Right -->
<text x="348" y="124" text-anchor="middle" fill="#ffffff" font-family="Caveat,cursive,sans-serif" font-size="22" font-weight="700" transform="rotate(-7 348 124)">Scan.</text>
<text x="352" y="150" text-anchor="middle" fill="#a5f3fc" font-family="Caveat,cursive,sans-serif" font-size="22" font-weight="700" transform="rotate(-7 352 150)">Check-in.</text>
<text x="354" y="176" text-anchor="middle" fill="#ffffff" font-family="Caveat,cursive,sans-serif" font-size="22" font-weight="700" transform="rotate(-7 354 176)">Get Noticed!</text>
</svg>
</div>
"""


def home_screen():
    style_background_home()
    style_base_layout()

    # Load Card Images with fallback
    student_img_b64 = get_image_base64("assets/student_new.png") or get_image_base64("student.png")
    teacher_img_b64 = get_image_base64("assets/teacher_new.png") or get_image_base64("snap-teacher.png")

    # =========================================================================
    # 1. FLOATING GLASS NAVBAR PILL
    # =========================================================================
    with st.container(key="navbar_pill"):
        nav_brand, nav_home, nav_about, nav_help, nav_status = st.columns(
            [5.6, 1.0, 1.0, 0.95, 1.45], vertical_alignment="center"
        )
        with nav_brand:
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
{GRAD_CAP_SVG}
<span style="font-family:'Outfit',sans-serif;font-weight:900;font-size:1.25rem;letter-spacing:-0.4px;color:#0f172a;">
SNAP<span style="background:linear-gradient(135deg,#4338ca,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CLASS</span>
</span>
<span style="color:#cbd5e1;font-weight:300;font-size:1.1rem;">|</span>
<span style="color:#64748b;font-size:0.84rem;font-weight:500;font-style:italic;">
Smart Dual-Verification &amp; Anti-Bunk Attendance Platform
</span>
</div>
""", unsafe_allow_html=True)

        with nav_home:
            st.button("🏠 Home", type="primary", use_container_width=True, key="nav_home_btn")
        with nav_about:
            if st.button("ℹ️ About", type="secondary", use_container_width=True, key="nav_about_btn"):
                about_dialog()
        with nav_help:
            if st.button("❓ Help", type="secondary", use_container_width=True, key="nav_help_btn"):
                help_dialog()
        with nav_status:
            st.markdown("""
<div style="display:flex;justify-content:flex-end;">
<span style="display:inline-flex;align-items:center;gap:7px;background:#ecfdf5;border:1px solid #a7f3d0;color:#065f46;padding:6px 14px;border-radius:9999px;font-size:0.8rem;font-weight:700;white-space:nowrap;">
<span style="width:8px;height:8px;border-radius:50%;background:#10b981;display:inline-block;"></span>
Live System
</span>
</div>
""", unsafe_allow_html=True)

    # =========================================================================
    # 2. HERO BANNER SECTION (Headline + Feature Badges + AI Face Scan HUD)
    # =========================================================================
    hero_left, hero_right = st.columns([1.18, 1], gap="large", vertical_alignment="center")

    with hero_left:
        st.markdown("""
<div style="padding:0.4rem 0;">
<div style="display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,0.88);border:1px solid rgba(167,139,250,0.45);border-radius:9999px;padding:5px 15px;margin-bottom:14px;box-shadow:0 4px 12px rgba(79,70,229,0.08);">
<span style="color:#6366f1;font-size:0.88rem;">✦</span>
<span style="font-size:0.83rem;font-weight:700;color:#4338ca;font-family:'Outfit',sans-serif;">
Smarter Attendance. Brighter Future.
</span>
</div>
<h1 style="font-family:'Outfit',sans-serif !important;font-size:3.55rem !important;font-weight:900 !important;line-height:1.02 !important;margin:0 0 6px 0 !important;letter-spacing:-1.5px;color:#0f172a;">
SNAP<span style="background:linear-gradient(135deg,#4338ca 0%,#6366f1 50%,#7c3aed 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CLASS</span>
</h1>
<div style="font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800;color:#1e293b;line-height:1.2;margin-bottom:8px;">
Smart Attendance System
</div>
<div style="font-size:1.05rem;color:#475569;font-weight:500;margin-bottom:22px;">
Powered by <span style="font-weight:800;font-style:italic;color:#4338ca;border-bottom:3px solid #818cf8;padding-bottom:2px;">Face Recognition AI</span>
</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;max-width:540px;">
<div style="background:rgba(255,255,255,0.92);border:1px solid rgba(199,210,254,0.7);border-radius:14px;padding:10px 12px;display:flex;align-items:center;gap:9px;box-shadow:0 6px 16px rgba(79,70,229,0.06);">
<span style="display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:9px;background:#d1fae5;color:#059669;font-size:0.95rem;flex-shrink:0;">🛡️</span>
<span style="font-size:0.78rem;font-weight:700;color:#1e293b;line-height:1.25;">Anti-Bunk Verification</span>
</div>
<div style="background:rgba(255,255,255,0.92);border:1px solid rgba(199,210,254,0.7);border-radius:14px;padding:10px 12px;display:flex;align-items:center;gap:9px;box-shadow:0 6px 16px rgba(79,70,229,0.06);">
<span style="display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:9px;background:#e0e7ff;color:#4338ca;font-size:0.95rem;flex-shrink:0;">🪪</span>
<span style="font-size:0.78rem;font-weight:700;color:#1e293b;line-height:1.25;">Face Recognition Check-in</span>
</div>
<div style="background:rgba(255,255,255,0.92);border:1px solid rgba(199,210,254,0.7);border-radius:14px;padding:10px 12px;display:flex;align-items:center;gap:9px;box-shadow:0 6px 16px rgba(79,70,229,0.06);">
<span style="display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:9px;background:#ede9fe;color:#6d28d9;font-size:0.95rem;flex-shrink:0;">📊</span>
<span style="font-size:0.78rem;font-weight:700;color:#1e293b;line-height:1.25;">Real-Time Reports</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    with hero_right:
        st.markdown(_hero_face_hud_html(), unsafe_allow_html=True)

    st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 3. DUAL ROLE CARDS ("I'm a Student" & "I'm a Teacher")
    # =========================================================================
    col1, col2 = st.columns(2, gap="large")

    # STUDENT CARD
    with col1:
        with st.container(key="student_card"):
            student_photo_html = (
                f"<img src='{student_img_b64}' style='width:100%;height:185px;object-fit:cover;object-position:center;border-radius:18px;border:2px solid #e0e7ff;box-shadow:0 10px 22px -8px rgba(79,70,229,0.28);' />"
                if student_img_b64 else ""
            )
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
<div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#4f46e5,#7c3aed);display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.5rem;flex-shrink:0;box-shadow:0 8px 18px rgba(79,70,229,0.35);">
🎓
</div>
<div>
<h2 style="font-family:'Outfit',sans-serif !important;font-size:1.7rem !important;font-weight:800 !important;margin:0 !important;line-height:1.15;color:#0f172a;">
I'm a <span style="background:linear-gradient(135deg,#4338ca,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Student</span>
</h2>
<p style="color:#64748b;font-size:0.86rem;margin:3px 0 0 0;font-weight:500;">
Check-in, view records &amp; track my attendance
</p>
</div>
</div>
<div style="display:grid;grid-template-columns:1.1fr 0.9fr;gap:14px;align-items:center;margin-bottom:16px;">
<div style="display:flex;flex-direction:column;gap:11px;">
<div style="display:flex;align-items:center;gap:9px;font-size:0.88rem;font-weight:600;color:#334155;">
<span style="width:20px;height:20px;border-radius:50%;background:#4f46e5;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;">✓</span>
Live Selfie Check-in
</div>
<div style="display:flex;align-items:center;gap:9px;font-size:0.88rem;font-weight:600;color:#334155;">
<span style="width:20px;height:20px;border-radius:50%;background:#4f46e5;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;">✓</span>
View Attendance History
</div>
<div style="display:flex;align-items:center;gap:9px;font-size:0.88rem;font-weight:600;color:#334155;">
<span style="width:20px;height:20px;border-radius:50%;background:#4f46e5;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;">✓</span>
Track Performance
</div>
</div>
<div style="background:linear-gradient(145deg,#eef2ff,#f5f3ff);border-radius:20px;padding:6px;">
{student_photo_html}
</div>
</div>
""", unsafe_allow_html=True)

            if st.button("Student Login  →", type="primary", use_container_width=True, key="student_login_cta"):
                st.session_state["login_type"] = "student"
                st.rerun()

    # TEACHER CARD
    with col2:
        with st.container(key="teacher_card"):
            teacher_photo_html = (
                f"<img src='{teacher_img_b64}' style='width:100%;height:185px;object-fit:cover;object-position:top center;border-radius:18px;border:2px solid #fbcfe8;box-shadow:0 10px 22px -8px rgba(219,39,119,0.25);' />"
                if teacher_img_b64 else ""
            )
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
<div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#db2777,#ec4899);display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.45rem;flex-shrink:0;box-shadow:0 8px 18px rgba(219,39,119,0.32);">
👩‍🏫
</div>
<div>
<h2 style="font-family:'Outfit',sans-serif !important;font-size:1.7rem !important;font-weight:800 !important;margin:0 !important;line-height:1.15;color:#0f172a;">
I'm a <span style="background:linear-gradient(135deg,#db2777,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Teacher</span>
</h2>
<p style="color:#64748b;font-size:0.86rem;margin:3px 0 0 0;font-weight:500;">
Manage classes &amp; verify attendance
</p>
</div>
</div>
<div style="display:grid;grid-template-columns:1.1fr 0.9fr;gap:14px;align-items:center;margin-bottom:16px;">
<div style="display:flex;flex-direction:column;gap:11px;">
<div style="display:flex;align-items:center;gap:9px;font-size:0.88rem;font-weight:600;color:#334155;">
<span style="width:20px;height:20px;border-radius:50%;background:#db2777;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;">✓</span>
Start/End Class Session
</div>
<div style="display:flex;align-items:center;gap:9px;font-size:0.88rem;font-weight:600;color:#334155;">
<span style="width:20px;height:20px;border-radius:50%;background:#db2777;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;">✓</span>
Monitor Live Attendance
</div>
<div style="display:flex;align-items:center;gap:9px;font-size:0.88rem;font-weight:600;color:#334155;">
<span style="width:20px;height:20px;border-radius:50%;background:#db2777;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:0.7rem;flex-shrink:0;">✓</span>
Export Reports
</div>
</div>
<div style="background:linear-gradient(145deg,#fdf2f8,#fce7f3);border-radius:20px;padding:6px;">
{teacher_photo_html}
</div>
</div>
""", unsafe_allow_html=True)

            if st.button("Faculty Login  →", type="primary", use_container_width=True, key="teacher_login_cta"):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    # =========================================================================
    # 4. BOTTOM TRUST STRIP FOOTER
    # =========================================================================
    footer_home()
