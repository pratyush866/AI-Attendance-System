# 🚀 Streamlit Community Cloud Live Deployment Guide
### AI-Based Smart Student Attendance System (Orbitals Team)
**Institution:** ITM College of Science and Management, GIDA, Gorakhpur  
**Course:** BCA Final Year Project (2026–2027)

---

## 🌟 Overview
This system is configured to deploy directly to **Streamlit Community Cloud** (`share.streamlit.io`) for free, public, 24/7 access on any smartphone, tablet, or laptop.

---

## 📋 Pre-Configured Cloud Files Included
1. **`packages.txt`**: Installs essential Debian Linux libraries (`cmake`, `libgl1`, `libglib2.0-0`, `libsndfile1`, `ffmpeg`).
2. **`requirements.txt`**: Pre-pinned Python packages with `numpy<2.0.0` and `dlib-bin` manylinux wheels.
3. **`.streamlit/config.toml`**: Production server settings (`headless = true`, port `8501`, light theme).
4. **Dual Database Engine**: Automatically uses Cloud Supabase if configured, or high-speed local SQLite replication.

---

## 🛠️ Step-by-Step Deployment Instructions

### Step 1: Open Streamlit Community Cloud
1. Go to [https://share.streamlit.io](https://share.streamlit.io) in your web browser.
2. Sign in with your **GitHub Account** (the account owning `pratyush866/AI-Attendance-System`).

### Step 2: Create a New App
1. Click the blue **"New app"** (or **"Create app"**) button at the top-right.
2. Choose **"I already have an app"** if prompted.

### Step 3: Configure App Settings
Fill in the deployment fields:
- **Repository:** `pratyush866/AI-Attendance-System`
- **Branch:** `main`
- **Main file path:** `app.py`
- **App URL (Custom Subdomain):** Choose a name like:
  `ai-attendance-itm.streamlit.app` or `orbitals-ai-attendance.streamlit.app`

### Step 4: Configure Secrets (Optional for Cloud Supabase)
If you want multi-device cloud synchronization across different networks:
1. Click **"Advanced settings..."** before deploying (or go to App Settings > Secrets afterwards).
2. Paste your Supabase credentials:
   ```toml
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your-supabase-anon-key"
   APP_DOMAIN = "https://your-custom-subdomain.streamlit.app"
   ```
*(Note: If you leave this empty, the application automatically runs on the high-performance local SQLite engine).*

### Step 5: Click Deploy!
1. Click the **"Deploy!"** button.
2. Watch the terminal build logs for ~2 minutes.
3. Once completed, your live application URL will be active! 🎉

---

## 📱 How to Use in a Real Classroom

### 👩‍🏫 For Teachers:
1. Open the live app URL on your phone or classroom laptop.
2. Click **Faculty Portal** $\rightarrow$ Login with your faculty credentials.
3. Select your **Subject & Section** $\rightarrow$ Click **"Launch Attendance Session"**.
4. The screen displays a **Dynamic 4-Digit Session PIN** and a **QR Code**.
5. Project the QR code on the projector or announce the 4-digit PIN in the room.
6. Once students submit their selfies, take a single **wide-angle classroom photo** of all seated students and upload it.
7. The AI will instantly cross-verify each selfie against the classroom photo.
8. Download the verified attendance **Excel/CSV report**.

### 👨‍🎓 For Students:
1. Scan the teacher's projected QR code or open `https://your-app.streamlit.app` on mobile.
2. Click **Student Portal** $\rightarrow$ Login (or auto-enrolled with student ID).
3. Enter the teacher's announced **4-digit session PIN**.
4. Snap a quick **live selfie** using your phone camera.
5. Once your face matches your registered biometric profile, your claim is submitted.
6. When the teacher uploads the classroom panoramic snapshot, your status automatically updates to **PRESENT**. If you tried to submit from the canteen or lawn, you are flagged as **PROXY / BUNK DETECTED**.

---

## 🛡️ Orbitals Project Team & Guidance
- **Pratyush Mishra** (Team Leader) — Roll No: `2514018680059`
- **Atul Upadhyay** — Roll No: `2514018680041`
- **Divyanshu Upadhyay** — Roll No: `2514018680045`
- **Adesh Bhatt** — Roll No: `2514018680026`
- **Mo Ashad** — Roll No: `2514018680055`
- **Supervised by:** **Ms. Vinita Yadav** (*Assistant Professor, Dept. of Computer Applications, ITM College*)
