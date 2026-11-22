"""
Academic Seminar Report Generator: Quantum Computing (.docx)
Format: ITM College of Science and Management, GIDA, Gorakhpur
Course: BCA Final Year - Session 2026-2027
Topic: QUANTUM COMPUTING: Foundations, Physical Architecture, Quantum Algorithms, Real-World Applications, and Future Horizons

Team Leader: Pratyush Mishra (Roll No. 2514018680059)
Team Members:
  - Atul Upadhyay (Roll No. 2514018680041)
  - Divyanshu Upadhyay (Roll No. 2514018680045)
  - Adesh Bhatt (Roll No. 2514018680026)
Guide: Ms. Vinita Yadav
"""

import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text, title="KEY PRINCIPLE / CONCEPT HIGHLIGHT"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=130, bottom=130, left=180, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="1E3A8A"/>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_t = p.add_run(f"★ {title}: ")
    r_t.bold = True
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(10.5)
    r_t.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    r_b = p.add_run(text)
    r_b.font.name = "Times New Roman"
    r_b.font.size = Pt(10.5)
    r_b.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, header_bg="1E3A8A"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for idx, cell in enumerate(table.rows[0].cells):
        cell.width = col_widths[idx]
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=130, bottom=130, left=140, right=140)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.bold = True
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                
    for r_idx, row in enumerate(table.rows[1:], start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row.cells):
            cell.width = col_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12.5)
    r.bold = True
    r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    return p

def add_body_paragraph(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(11)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    return p

def add_bullet_point(doc, text, bold_title=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_title:
        r_t = p.add_run(bold_title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10.5)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    return p

def embed_figure(doc, image_path, caption_text, figure_num, width_in=6.2):
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(image_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_num = p_cap.add_run(f"Figure {figure_num}: ")
        r_num.bold = True
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(10)
        r_num.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
        r_cap = p_cap.add_run(caption_text)
        r_cap.italic = True
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

def build_quantum_report():
    print("Building Quantum Computing Academic Seminar Report (.docx)...")
    doc = Document()

    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        sec.header_distance = Inches(0.5)
        sec.footer_distance = Inches(0.5)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # =========================================================================
    # 1. FRONT COVER PAGE
    # =========================================================================
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(0)
    p_logo.paragraph_format.space_after = Pt(6)
    if os.path.exists('assets/itm_college_logo.png'):
        r_logo = p_logo.add_run()
        r_logo.add_picture('assets/itm_college_logo.png', width=Inches(1.2))

    p_col = doc.add_paragraph()
    p_col.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_col.paragraph_format.space_after = Pt(2)
    r_col = p_col.add_run("ITM COLLEGE OF SCIENCE AND MANAGEMENT\n")
    r_col.bold = True
    r_col.font.size = Pt(14)
    r_col.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    r_aff = p_col.add_run("Affiliated to Deen Dayal Upadhyay Gorakhpur University (DDU Gorakhpur)\nAL-1, Sector-7, GIDA, Gorakhpur – 273209 (U.P.)")
    r_aff.font.size = Pt(10)
    r_aff.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rep = p_rep.add_run("SEMINAR REPORT\nON")
    r_rep.bold = True
    r_rep.font.size = Pt(13)
    r_rep.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(8)
    r_t = p_title.add_run("“QUANTUM COMPUTING: PRINCIPLES, PHYSICAL ARCHITECTURE, QUANTUM ALGORITHMS AND FUTURE HORIZONS”")
    r_t.bold = True
    r_t.font.size = Pt(14.5)
    r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_after = Pt(14)
    r_deg = p_deg.add_run("Submitted in partial fulfilment of the requirements for the degree of\n")
    r_deg.font.size = Pt(10.5)
    r_deg.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    r_bca = p_deg.add_run("BACHELOR OF COMPUTER APPLICATIONS (BCA)\nFINAL YEAR\n")
    r_bca.bold = True
    r_bca.font.size = Pt(13)
    r_bca.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    r_uni = p_deg.add_run("Department of Computer Applications\nDeen Dayal Upadhyay Gorakhpur University, Gorakhpur")
    r_uni.font.size = Pt(10.5)

    # 2-Column Info Table
    info_tbl = doc.add_table(rows=1, cols=2)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_tbl.columns[0].width = Inches(3.6)
    info_tbl.columns[1].width = Inches(2.9)
    
    # Left Cell: Students
    c_left = info_tbl.cell(0, 0)
    set_cell_margins(c_left, 80, 80, 100, 100)
    p_by = c_left.paragraphs[0]
    p_by.paragraph_format.line_spacing = 1.15
    r_by_t = p_by.add_run("SUBMITTED BY:\n")
    r_by_t.bold = True
    r_by_t.font.size = Pt(10.5)
    r_by_t.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    students = [
        ("Pratyush Mishra", "2514018680059", " (Team Leader)"),
        ("Atul Upadhyay", "2514018680041", ""),
        ("Divyanshu Upadhyay", "2514018680045", ""),
        ("Adesh Bhatt", "2514018680026", "")
    ]
    for sname, sroll, stag in students:
        r_sn = p_by.add_run(f"• {sname}{stag}\n")
        r_sn.bold = True
        r_sn.font.size = Pt(10)
        r_sr = p_by.add_run(f"   Roll No: {sroll}\n")
        r_sr.font.size = Pt(9.5)
        r_sr.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Right Cell: Guide
    c_right = info_tbl.cell(0, 1)
    set_cell_margins(c_right, 80, 80, 100, 100)
    p_sup = c_right.paragraphs[0]
    p_sup.paragraph_format.line_spacing = 1.15
    r_sup_t = p_sup.add_run("UNDER THE GUIDANCE OF:\n")
    r_sup_t.bold = True
    r_sup_t.font.size = Pt(10.5)
    r_sup_t.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    r_gn = p_sup.add_run("Ms. Vinita Yadav\n")
    r_gn.bold = True
    r_gn.font.size = Pt(11)
    r_gt = p_sup.add_run("Assistant Professor / Seminar Guide\nDepartment of Computer Applications\nITM College of Science & Management\nGorakhpur - 273209\n\n")
    r_gt.font.size = Pt(9.5)
    r_gt.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    r_sess = p_sup.add_run("ACADEMIC SESSION: 2026 – 2027")
    r_sess.bold = True
    r_sess.font.size = Pt(10)
    r_sess.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_page_break()

    # =========================================================================
    # 2. CERTIFICATE
    # =========================================================================
    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ct = p_cert_title.add_run("CERTIFICATE")
    r_ct.bold = True
    r_ct.font.size = Pt(16)
    r_ct.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_body_paragraph(
        doc,
        "This is to certify that the seminar report entitled “QUANTUM COMPUTING: Principles, Physical Architecture, "
        "Quantum Algorithms and Future Horizons” has been prepared and submitted by the following students of Bachelor of "
        "Computer Applications (BCA), Final Year, ITM College of Science and Management, GIDA, Gorakhpur, affiliated to "
        "Deen Dayal Upadhyay Gorakhpur University (DDU Gorakhpur):"
    )

    cert_tbl = doc.add_table(rows=5, cols=3)
    col_w_cert = [Inches(1.0), Inches(3.2), Inches(2.3)]
    cert_headers = ["S.No.", "Name of Student", "University Roll Number"]
    for idx, name in enumerate(cert_headers):
        cert_tbl.rows[0].cells[idx].paragraphs[0].text = name
    
    c_data = [
        ("1", "Pratyush Mishra (Team Leader)", "2514018680059"),
        ("2", "Atul Upadhyay", "2514018680041"),
        ("3", "Divyanshu Upadhyay", "2514018680045"),
        ("4", "Adesh Bhatt", "2514018680026")
    ]
    for r_idx, row_data in enumerate(c_data, start=1):
        for c_idx, val in enumerate(row_data):
            p = cert_tbl.rows[r_idx].cells[c_idx].paragraphs[0]
            p.text = val
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_table(cert_tbl, col_w_cert)

    add_body_paragraph(
        doc,
        "The report has been prepared under my guidance for academic evaluation as part of the requirements of the BCA programme. "
        "To the best of my knowledge, the technical explanations, physical architectures, and algorithmic investigations presented "
        "herein represent bonafide scholarly work suitable for academic seminar submission.",
        space_after=30
    )

    sig_tbl = doc.add_table(rows=1, cols=3)
    sig_tbl.columns[0].width = Inches(2.2)
    sig_tbl.columns[1].width = Inches(2.2)
    sig_tbl.columns[2].width = Inches(2.1)
    
    sig_cells = [
        ("_______________________\nSeminar Guide\nMs. Vinita Yadav\nDept. of Computer Applications", 0),
        ("_______________________\nHead of Department\nDept. of Computer Applications\nITM College of Science & Mgt.", 1),
        ("_______________________\nExternal Examiner\nDeen Dayal Upadhyay\nGorakhpur University", 2)
    ]
    for text_val, c_idx in sig_cells:
        c = sig_tbl.cell(0, c_idx)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text_val)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.bold = True
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    p_seal = doc.add_paragraph()
    p_seal.paragraph_format.space_before = Pt(25)
    r_seal = p_seal.add_run("Date: _________________________\t\t\t\tPlace: Gorakhpur")
    r_seal.font.size = Pt(10)
    r_seal.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION & ACKNOWLEDGEMENT
    # =========================================================================
    p_dec_title = doc.add_paragraph()
    p_dec_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dt = p_dec_title.add_run("DECLARATION")
    r_dt.bold = True
    r_dt.font.size = Pt(15)
    r_dt.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_body_paragraph(
        doc,
        "We hereby declare that the seminar report entitled “QUANTUM COMPUTING: Principles, Physical Architecture, "
        "Quantum Algorithms and Future Horizons” is an authentic academic work prepared by our group as part of the "
        "Bachelor of Computer Applications (BCA), Final Year programme. The report explains the foundational concepts, history, "
        "mechanisms, physical cryogenic architectures, quantum algorithms (Shor's and Grover's), real-world applications, "
        "and future horizons of quantum computing."
    )
    add_body_paragraph(
        doc,
        "We have made a sincere effort to understand the core principles of quantum physics and computational complexity. "
        "Any ideas, facts, equations, or scientific illustrations obtained from established research sources have been duly "
        "acknowledged in the bibliography. This report is submitted for academic evaluation."
    )

    dec_tbl = doc.add_table(rows=1, cols=4)
    for c_i, (sn, sr, _) in enumerate(students):
        c = dec_tbl.cell(0, c_i)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run("__________________\n")
        r1.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
        r2 = p.add_run(f"{sn}\n")
        r2.bold = True
        r2.font.size = Pt(9)
        r3 = p.add_run(f"Roll: {sr}")
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    p_ack_title = doc.add_paragraph()
    p_ack_title.paragraph_format.space_before = Pt(24)
    p_ack_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_at = p_ack_title.add_run("ACKNOWLEDGEMENT")
    r_at.bold = True
    r_at.font.size = Pt(15)
    r_at.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_body_paragraph(
        doc,
        "We express our sincere gratitude to the management and faculty members of ITM College of Science and Management, "
        "GIDA, Gorakhpur, for providing us with the opportunity to prepare this comprehensive seminar report on “Quantum Computing.” "
        "We are especially thankful to our seminar guide, Ms. Vinita Yadav, for her invaluable guidance, encouragement, and insightful "
        "suggestions throughout our study of quantum information theory, cryogenics, and quantum circuit models."
    )
    add_body_paragraph(
        doc,
        "We also thank our classmates, friends, and family for their steadfast motivation. Finally, we acknowledge the global quantum "
        "computing research community, national quantum initiatives, and open-source frameworks (including IBM Qiskit, Google Cirq, "
        "and PennyLane) whose open documentation, research papers, and educational quantum cloud platforms enriched our understanding."
    )

    doc.add_page_break()

    # =========================================================================
    # 4. ABSTRACT
    # =========================================================================
    p_abs_title = doc.add_paragraph()
    p_abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ab = p_abs_title.add_run("ABSTRACT")
    r_ab.bold = True
    r_ab.font.size = Pt(16)
    r_ab.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_body_paragraph(
        doc,
        "Classical computing, founded on the Turing machine architecture and binary silicon transistors, has driven technological "
        "progress for over seven decades. However, as transistor gate dimensions approach atomic boundaries (sub-2 nanometers), classical "
        "computing encounters fundamental physical barriers imposed by quantum tunneling, thermal dissipation, and exponential algorithmic "
        "complexity. Intractable problems in quantum chemistry, molecular drug design, logistical combinatorial optimization, and prime factorization "
        "remain computationally unreachable for even the most powerful exascale classical supercomputers."
    )
    add_body_paragraph(
        doc,
        "Quantum Computing represents a revolutionary computational paradigm that directly harnesses the fundamental postulates of quantum mechanics—namely "
        "Superposition, Entanglement, and Quantum Interference—to execute information processing tasks with exponential and polynomial speedups over classical "
        "counterparts. Instead of binary bits restricted to deterministic 0 or 1 states, quantum computers utilize Quantum Bits (Qubits) that exist as linear "
        "combinations within a complex Hilbert space, geometrically visualized on the Bloch Sphere. When N qubits are entangled, the system processes 2^N states "
        "simultaneously, yielding extraordinary computational parallelism."
    )
    add_body_paragraph(
        doc,
        "This seminar report presents a comprehensive academic investigation into Quantum Computing across seven core dimensions: (1) Conceptual Foundations "
        "and Historical Evolution from Feynman's 1981 simulation postulate to modern Noisy Intermediate-Scale Quantum (NISQ) systems; (2) Core Mathematical Mechanisms "
        "including linear algebra formulations, state vectors, Bell states, and unitary quantum logic gates; (3) Multi-Tier Physical Architecture detailing "
        "dilution refrigeration systems operating at 15 milliKelvin, microwave control lines, and leading qubit modalities (Superconducting Transmons, Trapped Ions, "
        "and Photonics); (4) Paradigm-Shifting Quantum Algorithms, contrasting the exponential speedup of Shor's integer factorization algorithm against RSA cryptography "
        "and Grover's quadratic database search acceleration; (5) Transformative Real-World Applications spanning Post-Quantum Cryptography, drug discovery, financial "
        "portfolio modeling, and Quantum Machine Learning (QML); and (6) Current Technological Bottlenecks, decoherence challenges, Quantum Error Correction (QEC), "
        "and emerging career avenues for BCA and computer science graduates."
    )

    add_callout(
        doc,
        "Quantum computing does not simply represent faster microprocessors; it embodies a fundamentally distinct mathematical model of computation. "
        "It solves problems by configuring quantum interference to amplify correct computational pathways while canceling incorrect trajectories.",
        title="CORE PARADIGM SHIFT"
    )

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(8)
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.bold = True
    r_kwt.font.size = Pt(10)
    r_kwt.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    r_kw = p_kw.add_run("Quantum Computing, Qubits, Superposition, Entanglement, Bloch Sphere, Shor's Algorithm, Grover's Algorithm, Dilution Refrigerator, Superconducting Transmons, NISQ Era, Post-Quantum Cryptography.")
    r_kw.font.size = Pt(10)
    r_kw.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_page_break()

    # =========================================================================
    # 5. TABLE OF CONTENTS
    # =========================================================================
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_toc = p_toc.add_run("TABLE OF CONTENTS")
    r_toc.bold = True
    r_toc.font.size = Pt(16)
    r_toc.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    toc_items = [
        ("Certificate", "ii"),
        ("Declaration", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Tables & Figures", "vii"),
        ("1. Introduction", "1"),
        ("    1.1 Meaning of Quantum Computing", "1"),
        ("    1.2 Classical Bits versus Quantum Qubits", "2"),
        ("    1.3 Why Quantum Computing Matters", "3"),
        ("    1.4 Objectives of the Study", "4"),
        ("    1.5 Scope of the Report", "4"),
        ("2. History and Evolution of Quantum Computing", "5"),
        ("    2.1 Early Foundations & Feynman's 1981 Vision", "5"),
        ("    2.2 The Universal Quantum Turing Machine", "6"),
        ("    2.3 Breakthrough Algorithms: Shor and Grover", "6"),
        ("    2.4 The NISQ Era & Quantum Supremacy Milestones", "7"),
        ("    2.5 Chronological Timeline of Major Breakthroughs", "8"),
        ("3. Mechanisms and Core Principles", "9"),
        ("    3.1 Quantum Superposition and the Bloch Sphere", "9"),
        ("    3.2 Quantum Entanglement and Non-Locality", "10"),
        ("    3.3 Quantum Interference & Phase Manipulation", "11"),
        ("    3.4 Measurement and Wavefunction Collapse", "12"),
        ("    3.5 Quantum Logic Gates and Reversible Operations", "13"),
        ("4. Architecture of Quantum Computing Systems", "15"),
        ("    4.1 Overview of Physical Quantum Architecture", "15"),
        ("    4.2 Major Hardware Layers and Components", "16"),
        ("    4.3 Extreme Cryogenics & Dilution Refrigeration (15 mK)", "17"),
        ("    4.4 Leading Physical Qubit Modalities", "18"),
        ("    4.5 Classical-Quantum Hybrid Co-Processing", "19"),
        ("    4.6 Quantum Decoherence & Error Correction (QEC)", "20"),
        ("5. Quantum Algorithms and Real-World Applications", "21"),
        ("    5.1 Shor's Algorithm and the Cryptographic Threat", "21"),
        ("    5.2 Grover's Algorithm for Accelerated Database Search", "22"),
        ("    5.3 Quantum Chemistry and Molecular Drug Discovery", "23"),
        ("    5.4 Financial Portfolio Modeling & Monte Carlo Speedup", "24"),
        ("    5.5 Logistics, Route Optimization and Supply Chain", "25"),
        ("    5.6 Quantum Machine Learning (QML)", "26"),
        ("6. Future Scope and Challenges", "27"),
        ("    6.1 The Engineering Challenge of Decoherence and Noise", "27"),
        ("    6.2 Roadmap to Fault-Tolerant Quantum Supercomputers", "28"),
        ("    6.3 National Quantum Mission (NQM) - India's Strategic Push", "29"),
        ("    6.4 Career Pathways for BCA and IT Graduates", "30"),
        ("7. Conclusion", "31"),
        ("Bibliography / References", "32"),
        ("Appendix: Glossary of Quantum Computing Terms", "34")
    ]

    toc_tbl = doc.add_table(rows=len(toc_items), cols=2)
    toc_tbl.columns[0].width = Inches(5.5)
    toc_tbl.columns[1].width = Inches(1.0)
    for idx, (title, page) in enumerate(toc_items):
        c0 = toc_tbl.cell(idx, 0)
        c1 = toc_tbl.cell(idx, 1)
        set_cell_margins(c0, 35, 35, 50, 50)
        set_cell_margins(c1, 35, 35, 50, 50)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        if title[0].isdigit() or title.startswith("Certificate") or title.startswith("Abstract") or title.startswith("Bibliography") or title.startswith("Appendix"):
            r0.bold = True
            r0.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        else:
            r0.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCTION
    # =========================================================================
    add_heading_1(doc, "1. INTRODUCTION")

    add_heading_2(doc, "1.1 Meaning of Quantum Computing")
    add_body_paragraph(
        doc,
        "Quantum Computing is an advanced subfield of computer science and quantum information science that studies systems "
        "utilizing the counter-intuitive principles of quantum mechanics to store, transmit, and compute data. While classical "
        "computers rely on binary microelectronic switches (transistors) that represent data strictly as electrical voltage states "
        "corresponding to discrete 0 or 1 values, quantum computers process data using subatomic systems—such as superconducting "
        "circuits, trapped ions, or polarized photons—governed by quantum wave mechanics."
    )
    add_body_paragraph(
        doc,
        "In quantum computational theory, the basic unit of information is the Quantum Bit or Qubit. Qubits exploit quantum phenomena "
        "including superposition, quantum entanglement, and quantum interference to evaluate multidimensional solution spaces simultaneously. "
        "This allows quantum architectures to solve certain computational classes that are mathematically intractable for classical von Neumann computers."
    )

    add_heading_2(doc, "1.2 Classical Bits versus Quantum Qubits")
    add_body_paragraph(
        doc,
        "To comprehend the profound paradigm shift introduced by quantum computing, it is essential to contrast the physical and "
        "mathematical behavior of a classical bit with a quantum qubit:"
    )

    embed_figure(
        doc,
        'assets/quantum_bloch_sphere_superposition.png',
        "Conceptual comparison between deterministic Classical Bits and probabilistic Quantum Qubits on the Bloch Sphere.",
        "1.1",
        width_in=6.4
    )

    # Comparison Table
    tbl_bits = doc.add_table(rows=6, cols=3)
    tbl_bits_cols = [Inches(1.8), Inches(2.3), Inches(2.4)]
    b_headers = ["Attribute", "Classical Bit", "Quantum Qubit"]
    for idx, h in enumerate(b_headers):
        tbl_bits.rows[0].cells[idx].paragraphs[0].text = h
    
    b_rows = [
        ("Fundamental State", "Deterministic: Strictly 0 or 1", "Superposition: |ψ⟩ = α|0⟩ + β|1⟩"),
        ("Mathematical Domain", "Discrete Boolean space {0, 1}", "Continuous Complex Hilbert Space ℂ²"),
        ("N-Element Capacity", "Stores 1 out of 2^N states at a time", "Simultaneously holds all 2^N state amplitudes"),
        ("State Visualization", "Binary toggle switch (Off / On)", "Bloch Sphere surface coordinate (θ, φ)"),
        ("Measurement Effect", "Non-destructive; state remains unchanged", "Destructive; collapses wavefunction to |0⟩ or |1⟩")
    ]
    for r_i, row in enumerate(b_rows, start=1):
        for c_i, val in enumerate(row):
            tbl_bits.rows[r_i].cells[c_i].paragraphs[0].text = val
    format_table(tbl_bits, tbl_bits_cols)

    add_heading_2(doc, "1.3 Why Quantum Computing Matters")
    add_body_paragraph(
        doc,
        "Modern civilization depends upon classical high-performance computing (HPC) for atmospheric modeling, aerodynamic design, and financial trading. "
        "However, classical computers face computational brick walls when attempting to simulate natural quantum phenomena. As Nobel laureate Richard Feynman "
        "famously observed in 1981, nature at its microscopic scale does not obey classical physics; therefore, simulating molecular structures, chemical catalysts, "
        "and subatomic interactions requires a computer that natively operates on quantum mechanics."
    )
    add_body_paragraph(
        doc,
        "Furthermore, many critical industrial and computational problems belong to NP-Hard or exponential complexity classes. For example, factoring a 2048-bit "
        "RSA prime number requires classical supercomputers hundreds of millions of years of brute-force sieve processing. A fault-tolerant quantum computer "
        "running Shor's Algorithm can theoretically accomplish this task in several hours, presenting both unprecedented breakthroughs for science and urgent "
        "disruptions for cybersecurity."
    )

    add_heading_2(doc, "1.4 Objectives of the Study")
    add_bullet_point(doc, "To articulate the core principles of quantum mechanics (superposition, entanglement, interference) in computational terminology.", "1. Theoretical Foundation: ")
    add_bullet_point(doc, "To chart the historical progression of quantum computing from early quantum information theory to modern cloud-accessible NISQ processors.", "2. Historical Analysis: ")
    add_bullet_point(doc, "To demystify the multi-layer physical architecture of quantum systems, including dilution refrigeration, microwave control lines, and transmon qubits.", "3. Physical Architecture: ")
    add_bullet_point(doc, "To evaluate landmark quantum algorithms (Shor's, Grover's) and quantify their computational speedups over classical algorithms.", "4. Algorithmic Speedup: ")
    add_bullet_point(doc, "To survey real-world industrial use cases in cryptography, drug discovery, finance, and quantum machine learning.", "5. Practical Applications: ")
    add_bullet_point(doc, "To examine current hardware limitations (decoherence, noise) and identify academic/career opportunities for computer applications graduates.", "6. Future Perspectives: ")

    add_heading_2(doc, "1.5 Scope of the Report")
    add_body_paragraph(
        doc,
        "This seminar report provides an academic and technical overview tailored for undergraduate students of Computer Applications. "
        "While rigorous in its explanation of linear algebraic representations (Dirac bra-ket notation, unitary matrices) and hardware engineering, "
        "it emphasizes computational concepts, algorithmic logic, and software-level implications rather than advanced theoretical quantum electrodynamics."
    )

    doc.add_page_break()

    # =========================================================================
    # 2. HISTORY AND EVOLUTION
    # =========================================================================
    add_heading_1(doc, "2. HISTORY AND EVOLUTION OF QUANTUM COMPUTING")

    add_heading_2(doc, "2.1 Early Foundations & Feynman's 1981 Vision")
    add_body_paragraph(
        doc,
        "The conceptual genesis of quantum computing emerged from the intersection of quantum physics and information theory in the early 1980s. "
        "In 1981, physicist Richard Feynman delivered his landmark keynote address titled “Simulating Physics with Computers” at the First Conference on "
        "the Physics of Computation held at MIT. Feynman noted that classical computers experience exponential slowdowns when simulating quantum systems "
        "because describing N interacting quantum particles requires tracking 2^N complex probability parameters. Feynman proposed that building a computer "
        "out of quantum mechanical components would allow natural, polynomial-time simulations of nature."
    )

    add_heading_2(doc, "2.2 The Universal Quantum Turing Machine")
    add_body_paragraph(
        doc,
        "In 1985, British physicist David Deutsch at the University of Oxford formalized Feynman's conceptual vision by defining the Universal Quantum Turing "
        "Machine (QTM). Deutsch proved that a quantum computer could simulate any physical process governed by unitary quantum mechanics, laying the mathematical "
        "foundations for quantum complexity theory and quantum logic gates."
    )

    add_heading_2(doc, "2.3 Breakthrough Algorithms: Shor and Grover")
    add_body_paragraph(
        doc,
        "For nearly a decade, quantum computing remained largely a theoretical curiosity. This changed dramatically in the mid-1990s through two monumental breakthroughs:"
    )
    add_bullet_point(
        doc, 
        "In 1994, mathematician Peter Shor at Bell Laboratories published an algorithm for prime integer factorization and discrete logarithms with polynomial "
        "time complexity O((log N)^3). Because modern global cryptographic infrastructure (RSA, Diffie-Hellman, ECC) relies on the classical intractability of "
        "factoring large numbers, Shor's algorithm proved that a scalable quantum computer could compromise public-key encryption.", 
        "• Shor's Algorithm (1994): "
    )
    add_bullet_point(
        doc, 
        "In 1996, Lov Grover at Bell Laboratories invented a quantum algorithm for searching unstructured databases containing N elements in O(sqrt(N)) time, "
        "representing a quadratic speedup over classical linear search O(N). Grover's algorithm proved that quantum computers offer significant advantages "
        "across general search and optimization domains.", 
        "• Grover's Algorithm (1996): "
    )

    add_heading_2(doc, "2.4 The NISQ Era & Quantum Supremacy Milestones")
    add_body_paragraph(
        doc,
        "In 2018, theoretical physicist John Preskill coined the term 'Noisy Intermediate-Scale Quantum' (NISQ) to describe the contemporary era of quantum hardware. "
        "NISQ processors feature 50 to 1,000+ noisy physical qubits without full fault tolerance. In October 2019, Google Quantum AI achieved 'Quantum Supremacy' "
        "(Quantum Advantage) using its 53-qubit Sycamore processor, completing a synthetic sampling benchmark in 200 seconds that would have required classical "
        "supercomputers thousands of years. Subsequent breakthroughs by IBM (Eagle 127-qubit, Osprey 433-qubit, and Condor 1,121-qubit) have demonstrated rapid hardware scaling."
    )

    # Timeline Table
    p_tt = doc.add_paragraph()
    p_tt.paragraph_format.space_before = Pt(6)
    r_tt = p_tt.add_run("Table 2.1: Key Historical Milestones in Quantum Computing")
    r_tt.bold = True
    r_tt.font.size = Pt(10)
    r_tt.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    tbl_time = doc.add_table(rows=7, cols=3)
    tbl_time_cols = [Inches(1.2), Inches(2.2), Inches(3.1)]
    for idx, h in enumerate(["Year", "Pioneering Entity", "Historical Scientific Significance"]):
        tbl_time.rows[0].cells[idx].paragraphs[0].text = h
    
    t_rows = [
        ("1981", "Richard Feynman (MIT)", "Proposed using quantum mechanical phenomena to simulate quantum physics."),
        ("1985", "David Deutsch (Oxford)", "Formulated the mathematical model of the Universal Quantum Turing Machine."),
        ("1994", "Peter Shor (Bell Labs)", "Developed polynomial-time quantum prime factorization algorithm."),
        ("1996", "Lov Grover (Bell Labs)", "Demonstrated quadratic acceleration for unstructured database search."),
        ("2016", "IBM Quantum", "Launched IBM Quantum Experience, offering world's first cloud-accessible quantum processor."),
        ("2019", "Google AI (Sycamore)", "Demonstrated Quantum Supremacy on 53 superconducting qubits in 200 seconds.")
    ]
    for r_i, row in enumerate(t_rows, start=1):
        for c_i, val in enumerate(row):
            tbl_time.rows[r_i].cells[c_i].paragraphs[0].text = val
    format_table(tbl_time, tbl_time_cols)

    doc.add_page_break()

    # =========================================================================
    # 3. MECHANISMS AND CORE PRINCIPLES
    # =========================================================================
    add_heading_1(doc, "3. MECHANISMS AND CORE PRINCIPLES OF QUANTUM COMPUTING")

    add_heading_2(doc, "3.1 Quantum Superposition and the Bloch Sphere")
    add_body_paragraph(
        doc,
        "Superposition is the physical principle allowing a quantum system to exist in a linear combination of multiple states simultaneously. "
        "In Dirac bra-ket notation, a single qubit state |ψ⟩ is expressed as:\n"
        "    |ψ⟩ = α|0⟩ + β|1⟩\n"
        "where α and β are complex probability amplitudes satisfying the normalization constraint |α|² + |β|² = 1. "
        "The probability of measuring the qubit in state |0⟩ is |α|², and the probability of measuring |1⟩ is |β|²."
    )
    add_body_paragraph(
        doc,
        "Geometrically, an isolated two-level qubit is represented on the surface of a unit sphere known as the Bloch Sphere. "
        "The state vector is parameterized using spherical angles θ and φ:\n"
        "    |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ) sin(θ/2)|1⟩\n"
        "The north pole corresponds to computational basis state |0⟩ (θ = 0), the south pole corresponds to |1⟩ (θ = π), "
        "and points along the equator represent equal superpositions (such as |+⟩ = (|0⟩ + |1⟩)/√2 and |-⟩ = (|0⟩ - |1⟩)/√2)."
    )

    add_heading_2(doc, "3.2 Quantum Entanglement and Non-Locality")
    add_body_paragraph(
        doc,
        "Quantum Entanglement is a profound correlation between two or more qubits where the quantum state of each particle cannot be "
        "described independently of the others, regardless of spatial separation. Described famously by Albert Einstein as 'spooky action at a distance' "
        "(EPR Paradox), entangled states form the computational fabric of quantum parallelism."
    )
    add_body_paragraph(
        doc,
        "The canonical maximally entangled two-qubit states are known as the four Bell States (EPR pairs):\n"
        "    |Φ⁺⟩ = (|00⟩ + |11⟩) / √2\n"
        "    |Φ⁻⟩ = (|00⟩ - |11⟩) / √2\n"
        "    |Ψ⁺⟩ = (|01⟩ + |10⟩) / √2\n"
        "    |Ψ⁻⟩ = (|01⟩ - |10⟩) / √2\n"
        "Measuring one entangled qubit instantaneously determines the state of the paired qubit with 100% correlation."
    )

    add_heading_2(doc, "3.3 Quantum Interference & Phase Manipulation")
    add_body_paragraph(
        doc,
        "Because quantum probability amplitudes are complex numbers (possessing both magnitude and phase), they exhibit wave-like interference. "
        "Constructive interference enhances the probability amplitudes of the correct computational solution, while destructive interference cancels "
        "out the probability amplitudes of incorrect trajectories. Quantum algorithms are engineered so that when a measurement is performed, "
        "the probability of observing the correct output approaches 1."
    )

    add_heading_2(doc, "3.4 Measurement and Wavefunction Collapse")
    add_body_paragraph(
        doc,
        "According to the Copenhagen interpretation and quantum measurement postulates, an unobserved qubit evolves deterministically under "
        "unitary transformations. However, the moment a physical measurement is conducted, the delicate superposition wavefunction abruptly "
        "collapses into one of the classical basis states (|0⟩ or |1⟩). Quantum programmers cannot directly inspect intermediate superpositions "
        "without triggering collapse; algorithms must extract information strategically through global phase interference."
    )

    add_heading_2(doc, "3.5 Quantum Logic Gates and Reversible Operations")
    add_body_paragraph(
        doc,
        "Unlike classical logic gates (such as AND, OR) which destroy input information and generate heat, quantum logic operations must be "
        "strictly unitary (U†U = I) and reversible. The primary quantum gates include:"
    )
    add_bullet_point(doc, "Performs a 180° rotation around the X-axis of the Bloch sphere, inverting |0⟩ to |1⟩ and |1⟩ to |0⟩ (quantum NOT gate).", "• Pauli-X Gate (NOT): ")
    add_bullet_point(doc, "Transforms computational basis states into equal superpositions: H|0⟩ = (|0⟩ + |1⟩)/√2 and H|1⟩ = (|0⟩ - |1⟩)/√2. Essential for initiating quantum parallelism.", "• Hadamard Gate (H): ")
    add_bullet_point(doc, "Rotates the phase of the |1⟩ state by e^(iφ) while leaving |0⟩ unchanged (e.g., Z gate introduces a 180° phase flip).", "• Phase Shift Gates (Z, S, T): ")
    add_bullet_point(doc, "A two-qubit gate that flips the target qubit if and only if the control qubit is in state |1⟩. Crucial for generating entangled Bell states.", "• Controlled-NOT Gate (CNOT): ")

    doc.add_page_break()

    # =========================================================================
    # 4. ARCHITECTURE OF QUANTUM COMPUTING
    # =========================================================================
    add_heading_1(doc, "4. ARCHITECTURE OF QUANTUM COMPUTING SYSTEMS")

    add_heading_2(doc, "4.1 Overview of Physical Quantum Architecture")
    add_body_paragraph(
        doc,
        "A functioning quantum computer is not a standalone desktop machine; it is a complex, multi-tiered cyber-physical installation "
        "comprising classical supercomputing clusters, microwave pulse electronics, multi-stage cryogenic refrigeration units, and a "
        "quantum processor chip situated at near-absolute zero temperatures."
    )

    embed_figure(
        doc,
        'assets/quantum_system_architecture.png',
        "Multi-Tier Architecture of a Quantum Computer: from classical software down to dilution refrigeration and QPU hardware.",
        "4.1",
        width_in=6.4
    )

    add_heading_2(doc, "4.2 Extreme Cryogenics & Dilution Refrigeration (15 mK)")
    add_body_paragraph(
        doc,
        "Superconducting quantum processors require near-complete eradication of ambient thermal noise to protect fragile quantum superpositions. "
        "Thermal energy at room temperature (300 Kelvin) contains sufficient kinetic agitation to instantly decohere superconducting qubits. "
        "To prevent this, the quantum chip is housed at the base of a specialized Dilution Refrigerator."
    )
    add_body_paragraph(
        doc,
        "The dilution refrigerator uses a closed-cycle isotopic mixture of Helium-3 and Helium-4. By circulating these isotopes across progressive "
        "cooling stages (50K Flange -> 4K Plate -> 0.8K Still -> 100mK Cold Plate), the system achieves a base plate temperature of approximately "
        "15 milliKelvin (-273.135 °C). This is over 100 times colder than the vacuum of deep interstellar space (2.7 Kelvin)."
    )

    add_heading_2(doc, "4.3 Leading Physical Qubit Modalities")
    add_body_paragraph(
        doc,
        "Global researchers are exploring several physical implementations to engineer reliable qubits:"
    )
    add_bullet_point(doc, "Lithographically fabricated circuits using aluminum or niobium with Josephson Junctions acting as non-linear inductors. Utilized by IBM, Google, and Rigetti. Fast gate operations (~20–100 nanoseconds), but sensitive to thermal noise.", "1. Superconducting Transmon Qubits: ")
    add_bullet_point(doc, "Individual charged ions (e.g., Ytterbium or Barium) trapped in electromagnetic fields in ultra-high vacuum and manipulated using focused laser pulses. Utilized by IonQ and Quantinuum. Exceptional coherence times (seconds to minutes) and pristine gate fidelities, but slower gate execution.", "2. Trapped-Ion Qubits: ")
    add_bullet_point(doc, "Qubits encoded into the polarization, path, or squeeze states of single photons. Utilized by PsiQuantum and Xanadu. Operates at room temperature and exhibits zero magnetic interference, but photon-photon interactions require complex non-linear optics.", "3. Photonic Quantum Computing: ")
    add_bullet_point(doc, "Individual electron spins trapped inside silicon quantum dots or semiconductor heterostructures. High compatibility with existing semiconductor manufacturing foundries.", "4. Silicon Spin Qubits: ")

    add_heading_2(doc, "4.4 Quantum Decoherence & Error Correction (QEC)")
    add_body_paragraph(
        doc,
        "The principal obstacle confronting quantum computing is Quantum Decoherence—the rapid loss of quantum information caused by environmental "
        "interactions (stray magnetic fields, cosmic rays, thermal fluctuations). In modern NISQ systems, qubit coherence lasts only 50 to 200 microseconds."
    )
    add_body_paragraph(
        doc,
        "To achieve fault-tolerant computing, researchers utilize Quantum Error Correction (QEC) codes, such as the Surface Code. In QEC, quantum "
        "information is not stored on a single physical qubit; instead, it is distributed non-locally across an array of hundreds or thousands of "
        "entangled physical qubits to synthesize one pristine 'Logical Qubit' protected against environmental bit-flip and phase-flip errors."
    )

    doc.add_page_break()

    # =========================================================================
    # 5. QUANTUM ALGORITHMS & APPLICATIONS
    # =========================================================================
    add_heading_1(doc, "5. QUANTUM ALGORITHMS AND REAL-WORLD APPLICATIONS")

    add_heading_2(doc, "5.1 Shor's Algorithm and Cryptographic Vulnerabilities")
    add_body_paragraph(
        doc,
        "Modern digital commerce relies entirely on asymmetric public-key cryptography (RSA-2048, Elliptic Curve Cryptography - ECC) to secure "
        "online banking, HTTPS web communications, and government intelligence. These ciphers depend on the classical difficulty of finding prime factors "
        "of large composite numbers. Peter Shor proved that a quantum algorithm utilizing the Quantum Fourier Transform (QFT) transforms factorization "
        "into an efficient period-finding problem solvable in O((log N)^3) polynomial time."
    )

    embed_figure(
        doc,
        'assets/quantum_algorithms_speedup.png',
        "Computational complexity speedup: Shor's exponential acceleration versus Grover's quadratic search speedup.",
        "5.1",
        width_in=6.4
    )

    add_body_paragraph(
        doc,
        "This existential security threat has sparked global development of Post-Quantum Cryptography (PQC). In 2024, the US National Institute of "
        "Standards and Technology (NIST) finalized the world's first post-quantum encryption standards (ML-KEM, ML-DSA) based on lattice mathematics "
        "impervious to quantum attacks."
    )

    add_heading_2(doc, "5.2 Grover's Algorithm for Accelerated Database Search")
    add_body_paragraph(
        doc,
        "Searching an unsorted database containing N records classically requires O(N) operations. Grover's algorithm utilizes quantum amplitude "
        "amplification to isolate the target element in O(√N) iterations. For a database of 1 trillion items, classical search requires 500 billion checks; "
        "Grover's algorithm locates the solution in approximately 1 million operations."
    )

    add_heading_2(doc, "5.3 Transformative Industrial Applications")
    add_bullet_point(
        doc,
        "Simulating molecular binding affinities for drug molecules and chemical catalysts (such as the Haber-Bosch nitrogen fixation process). "
        "Accurate quantum simulation can revolutionize pharmaceutical discovery by synthesizing customized cancer therapeutics in days rather than decades.",
        "• Molecular Chemistry & Drug Discovery: "
    )
    add_bullet_point(
        doc,
        "Financial institutions (JPMorgan Chase, Goldman Sachs) utilize Quantum Monte Carlo algorithms to execute high-speed risk analysis, option "
        "pricing, and portfolio arbitrage with quadratic speedups over classical algorithms.",
        "• Financial Modeling & Portfolio Optimization: "
    )
    add_bullet_point(
        doc,
        "Solving complex NP-Hard combinatorial problems such as the Traveling Salesperson Problem (TSP), airport gate scheduling, and global maritime "
        "shipping logistics using Quantum Approximate Optimization Algorithms (QAOA).",
        "• Supply Chain & Route Logistics: "
    )
    add_bullet_point(
        doc,
        "Parameterized quantum circuits (variational quantum classifiers) map high-dimensional data into exponentially large Hilbert spaces for enhanced "
        "feature separation and pattern recognition.",
        "• Quantum Machine Learning (QML): "
    )

    doc.add_page_break()

    # =========================================================================
    # 6. FUTURE SCOPE AND CHALLENGES
    # =========================================================================
    add_heading_1(doc, "6. FUTURE SCOPE AND CHALLENGES")

    add_heading_2(doc, "6.1 Engineering Bottlenecks")
    add_body_paragraph(
        doc,
        "Despite extraordinary theoretical promises, transition from experimental prototypes to practical commercial utility faces three bottlenecks:"
    )
    add_bullet_point(doc, "Current physical qubits exhibit two-qubit gate error rates around 0.1% to 1%. Fault-tolerant computing requires error rates below 0.01%.", "1. Gate Fidelity & Noise: ")
    add_bullet_point(doc, "Transmitting individual microwave coaxial lines to every qubit inside a dilution refrigerator becomes physically impossible at scale (the 'wiring bottleneck'). Control electronics must be miniaturized onto cryogenic silicon chips.", "2. Control Wiring Interconnects: ")
    add_bullet_point(doc, "Bridging the gap between 1,000 noisy physical qubits today and the 1,000,000 physical qubits required to yield 1,000 logical error-corrected qubits.", "3. Scaling to Logical Qubits: ")

    add_heading_2(doc, "6.2 National Quantum Mission (NQM) - India's Initiative")
    add_body_paragraph(
        doc,
        "In April 2023, the Union Cabinet of India approved the National Quantum Mission (NQM) with a budgetary outlay of ₹6,003 crore (approx. $730M USD) "
        "spanning 2023 to 2031. Coordinated by the Department of Science and Technology (DST), the mission aims to develop intermediate-scale quantum "
        "computers with 50 to 1,000 physical qubits, establish satellite-based quantum secure communication networks over 2,000 kilometers, and nurture "
        "indigenous quantum hardware development across premier Indian academic and research institutions."
    )

    add_heading_2(doc, "6.3 Career Pathways for BCA and IT Graduates")
    add_body_paragraph(
        doc,
        "Quantum computing is rapidly moving from pure physics laboratories to mainstream enterprise software development. "
        "BCA students possess strong foundational programming and mathematical training that can be directly adapted for quantum careers:"
    )
    add_bullet_point(doc, "Writing, transpiling, and testing quantum circuits using Python SDKs like Qiskit, Cirq, and PennyLane on real cloud hardware.", "• Quantum Software Developer: ")
    add_bullet_point(doc, "Developing classical software infrastructures, APIs, and middleware to manage hybrid classical-quantum cloud jobs.", "• Quantum DevOps / Cloud Engineer: ")
    add_bullet_point(doc, "Auditing enterprise security architectures and upgrading organizational encryption protocols to Post-Quantum Cryptography (PQC).", "• Post-Quantum Cybersecurity Analyst: ")

    doc.add_page_break()

    # =========================================================================
    # 7. CONCLUSION
    # =========================================================================
    add_heading_1(doc, "7. CONCLUSION")
    add_body_paragraph(
        doc,
        "Quantum Computing marks the beginning of the second quantum revolution—transitioning quantum physics from a descriptive observational science "
        "into an active computational tool. By exploiting superposition, entanglement, and quantum interference, quantum processors achieve computational "
        "parallelism fundamentally unattainable by binary silicon transistors."
    )
    add_body_paragraph(
        doc,
        "While full-scale fault-tolerant quantum supercomputers capable of executing Shor's algorithm on RSA-2048 keys remain an active research challenge "
        "estimated for the 2030s, the current NISQ era provides fertile ground for hybrid classical-quantum algorithms in chemistry, optimization, and AI. "
        "For students and future computer applications professionals at ITM College of Science and Management, acquiring quantum programming skills represents "
        "an invaluable competitive advantage in shaping the next frontier of global computing."
    )

    add_callout(
        doc,
        "“Quantum computing is not the next generation of classical computing; it is an entirely new dimension of human capability.”",
        title="CONCLUDING INSIGHT"
    )

    doc.add_page_break()

    # =========================================================================
    # BIBLIOGRAPHY / REFERENCES
    # =========================================================================
    add_heading_1(doc, "BIBLIOGRAPHY / REFERENCES")

    refs = [
        "[1] R. P. Feynman, “Simulating physics with computers,” International Journal of Theoretical Physics, vol. 21, no. 6/7, pp. 467–488, 1982.",
        "[2] D. Deutsch, “Quantum theory, the Church–Turing principle and the universal quantum computer,” Proc. Royal Society London A, vol. 400, pp. 97–117, 1985.",
        "[3] P. W. Shor, “Algorithms for quantum computation: discrete logarithms and factoring,” in Proc. 35th Annual Symposium on Foundations of Computer Science (FOCS), 1994, pp. 124–134.",
        "[4] L. K. Grover, “A fast quantum mechanical algorithm for database search,” in Proc. 28th Annual ACM Symposium on Theory of Computing (STOC), 1996, pp. 212–219.",
        "[5] M. A. Nielsen and I. L. Chuang, Quantum Computation and Quantum Information, Cambridge University Press, 10th Anniversary Edition, 2010.",
        "[6] J. Preskill, “Quantum computing in the NISQ era and beyond,” Quantum, vol. 2, p. 79, 2018.",
        "[7] F. Arute et al. (Google Quantum AI), “Quantum supremacy using a programmable superconducting processor,” Nature, vol. 574, pp. 505–510, 2019.",
        "[8] IBM Quantum, “Qiskit: An Open-source Software Development Kit for Working with Quantum Computers,” 2024. [Online]. Available: https://qiskit.org",
        "[9] National Institute of Standards and Technology (NIST), “Post-Quantum Cryptography Standardization Process,” 2024. [Online]. Available: https://csrc.nist.gov/projects/post-quantum-cryptography",
        "[10] Department of Science and Technology (DST), Government of India, “National Quantum Mission (NQM) Operational Framework,” 2023. [Online]. Available: https://dst.gov.in"
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(10)
        r_ref.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_page_break()

    # =========================================================================
    # APPENDIX: GLOSSARY OF QUANTUM TERMS
    # =========================================================================
    add_heading_1(doc, "APPENDIX: GLOSSARY OF QUANTUM COMPUTING TERMS")

    glossary = [
        ("Qubit", "The basic unit of quantum information, analogous to classical bit, represented by a two-state quantum system."),
        ("Superposition", "The ability of a quantum system to exist simultaneously in a linear combination of multiple basis states."),
        ("Entanglement", "A quantum phenomenon where two or more particles become inextricably linked regardless of spatial distance."),
        ("Bloch Sphere", "A geometrical sphere representation of pure single-qubit quantum states on complex coordinates (θ, φ)."),
        ("Quantum Interference", "The constructive or destructive interaction of complex probability amplitudes in quantum algorithms."),
        ("Wavefunction Collapse", "The irreversible transition of a quantum state into a single definite basis state upon classical observation."),
        ("NISQ Era", "Noisy Intermediate-Scale Quantum; the current era of processors with 50-1000+ qubits lacking full error correction."),
        ("Quantum Decoherence", "The gradual decay and loss of quantum phase information caused by thermal or magnetic environmental noise."),
        ("Dilution Refrigerator", "A cryogenic device that utilizes helium-3/helium-4 mixtures to cool quantum chips down to 15 milliKelvin."),
        ("Transmon Qubit", "A type of superconducting qubit engineered with a Josephson junction designed to resist charge noise."),
        ("Shor's Algorithm", "A quantum algorithm capable of finding the prime factors of an integer in polynomial time O((log N)³)."),
        ("Grover's Algorithm", "A quantum search algorithm providing quadratic speedup O(√N) over classical unstructured database search."),
        ("Logical Qubit", "A pristine, error-corrected virtual qubit synthesized from an ensemble of physical qubits via quantum error correction."),
        ("Post-Quantum Cryptography", "New cryptographic algorithms (e.g., lattice-based) secure against attacks by both classical and quantum computers.")
    ]

    tbl_gl = doc.add_table(rows=len(glossary)+1, cols=2)
    tbl_gl_cols = [Inches(2.0), Inches(4.5)]
    for idx, h in enumerate(["Term", "Definition & Conceptual Meaning"]):
        tbl_gl.rows[0].cells[idx].paragraphs[0].text = h

    for r_i, (term, mean) in enumerate(glossary, start=1):
        tbl_gl.rows[r_i].cells[0].paragraphs[0].text = term
        tbl_gl.rows[r_i].cells[1].paragraphs[0].text = mean
        tbl_gl.rows[r_i].cells[0].paragraphs[0].runs[0].bold = True
    format_table(tbl_gl, tbl_gl_cols)

    output_path = "Quantum_Computing_Seminar_Report.docx"
    doc.save(output_path)
    print(f"Report saved successfully as '{output_path}'")

if __name__ == '__main__':
    build_quantum_report()

