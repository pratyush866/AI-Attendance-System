import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 6px solid #4f46e5; padding: 22px; border-radius: 18px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04); transition: transform 0.2s ease;">
            <h3 style="margin: 0; color: #0f172a; font-size: 1.35rem; font-weight: 700; font-family: 'Outfit', sans-serif;">{name}</h3>
            <p style="color: #64748b; margin: 8px 0 14px 0; font-size: 0.92rem; font-family: 'Plus Jakarta Sans', sans-serif;">
                Code: <span style="background: #e0e7ff; color: #4338ca; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 0.85rem;">{code}</span> 
                &nbsp;|&nbsp; Section: <b style="color: #334155;">{section}</b>
            </p>
    """
    if stats:
        html += """
            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 6px;">
        """
        for icon, label, value in stats:
            is_total = (label == "Total" or "Total" in label)
            bg = "#fdf2f8" if is_total else "#f0fdf4"
            fg = "#be185d" if is_total else "#15803d"
            border = "#fbcfe8" if is_total else "#bbf7d0"

            html += f"""
                <div style="background: {bg}; color: {fg}; border: 1px solid {border}; padding: 4px 12px; border-radius: 10px; font-size: 0.88rem; font-weight: 600; font-family: 'Plus Jakarta Sans', sans-serif; display: inline-flex; align-items: center; gap: 4px;">
                    <span>{icon}</span> <span><b>{value}</b> {label}</span>
                </div>
            """
        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
