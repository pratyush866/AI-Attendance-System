import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    stats_html = ""
    if stats:
        stats_html = '<div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:14px;">'
        for icon, label, value in stats:
            stats_html += f"""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:6px 14px; border-radius:999px; font-size:0.85rem; color:#334155; display:inline-flex; align-items:center; gap:6px;">
                <span>{icon}</span> <span style="font-weight:700; color:#0F172A;">{value}</span> <span>{label}</span>
            </div>
            """
        stats_html += "</div>"

    html = f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; padding:22px 24px; margin-bottom:18px; box-shadow:0 4px 16px -2px rgba(0,0,0,0.04); position:relative; overflow:hidden; transition:all 0.25s ease;">
            <div style="position:absolute; top:0; left:0; right:0; height:4px; background:linear-gradient(90deg, #4F46E5 0%, #6366F1 50%, #818CF8 100%);"></div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
                <div>
                    <h3 style="margin:0 0 6px 0; color:#0F172A; font-size:1.35rem; font-weight:800; letter-spacing:-0.02em;">{name}</h3>
                    <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                        <span style="background:#EEF2FF; color:#4F46E5; border:1px solid #C7D2FE; padding:2px 10px; border-radius:6px; font-size:0.8rem; font-weight:700;">
                            Code: {code}
                        </span>
                        <span style="background:#F1F5F9; color:#475569; border:1px solid #E2E8F0; padding:2px 10px; border-radius:6px; font-size:0.8rem; font-weight:600;">
                            Section: {section}
                        </span>
                    </div>
                </div>
            </div>
            {stats_html}
        </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
