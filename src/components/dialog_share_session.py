import streamlit as st
import segno
import io
import os

@st.dialog("📲 Share Live Attendance Link")
def share_session_dialog(session_id, session_pin, subject_name):
    app_domain = None
    try:
        if hasattr(st, "secrets"):
            app_domain = st.secrets.get('APP_DOMAIN')
    except Exception:
        pass
    if not app_domain:
        app_domain = os.environ.get('APP_DOMAIN', 'http://localhost:8501')
    if not app_domain.startswith('http'):
        app_domain = f'http://{app_domain}'

    session_url = f"{app_domain}/?session={session_id}"

    st.markdown(f"""
        <div style="background: #eff6ff; border: 1px solid #3b82f6; border-radius: 12px; padding: 12px; margin-bottom: 15px;">
            <b style="color: #1d4ed8; font-size: 1.1rem;">Subject: {subject_name}</b><br/>
            <span style="color: #1e40af;">Students will open this link on their mobile to take their in-class selfie.</span>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔗 Session Link")
        st.code(session_url, language="text")
        st.markdown("### 🔑 Classroom PIN")
        st.markdown(f"""
            <div style="background: #fef08a; padding: 8px 16px; border-radius: 8px; font-size: 1.5rem; font-weight: bold; text-align: center; color: #854d0e; border: 2px dashed #ca8a04;">
                {session_pin}
            </div>
            <p style="font-size: 0.85rem; color: #64748b; margin-top: 5px;">
                Announce this 4-digit PIN in the room so students outside cannot submit.
            </p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📷 Scan QR Code")
        qr = segno.make(session_url)
        out = io.BytesIO()
        qr.save(out, kind='png', scale=8, border=1)
        st.image(out.getvalue(), caption="Scan with phone camera to open check-in")

