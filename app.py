import streamlit as st
import streamlit.components.v1 as components
import base64
import random
import smtplib
from email.mime.text import MIMEText
from db import init_db, execute_query, get_secret

st.set_page_config(
    page_title="Abhishek Singh | Systems & Automation Architect",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

try:
    init_db()
except Exception:
    pass

# Helper to send Email OTP for password reset
def send_reset_email(to_email, otp_code):
    smtp_email = get_secret("SMTP_EMAIL", "")
    smtp_password = get_secret("SMTP_APP_PASSWORD", "")
    if not smtp_email or not smtp_password:
        return False, "SMTP credentials missing in Streamlit secrets."
    
    msg = MIMEText(f"Hello Abhishek,\n\nYour OTP to reset your Portfolio Admin Password is: {otp_code}\n\nDo not share this OTP with anyone.")
    msg['Subject'] = "Portfolio Admin - Password Reset OTP"
    msg['From'] = smtp_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, [to_email], msg.as_string())
        return True, "OTP successfully sent to your email."
    except Exception as e:
        return False, f"Email delivery error: {e}"

# UI Styling
st.markdown("""
<style>
    .stApp { background-color: #050811; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .project-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
    }
    .badge {
        background: #1e1b4b;
        color: #818cf8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
        border: 1px solid #312e81;
    }
    .metric-card {
        background: #090d16;
        border-radius: 8px;
        padding: 14px;
        border-left: 3px solid #6366f1;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# 3D Interactive Three.js Hero
three_html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { margin: 0; overflow: hidden; background: #050811; }
    canvas { display: block; width: 100vw; height: 260px; }
    #tagline {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        pointer-events: none;
    }
    h1 { margin: 0; font-size: 1.9rem; font-weight: 800; letter-spacing: -0.5px; }
    p { margin: 4px 0 0; font-size: 0.85rem; color: #818cf8; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
  <div id="tagline">
    <h1>ABHISHEK SINGH</h1>
    <p>B2B Automation • Shop-Floor Systems • AI Pipelines</p>
  </div>
  <canvas id="canvas"></canvas>
  <script>
    const canvas = document.getElementById('canvas');
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, 260);
    renderer.setPixelRatio(window.devicePixelRatio);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 260, 0.1, 1000);
    camera.position.z = 20;

    const geometry = new THREE.TorusKnotGeometry(5.5, 1.6, 100, 16);
    const material = new THREE.MeshStandardMaterial({
      color: 0x4f46e5,
      wireframe: true,
      emissive: 0x312e81,
      emissiveIntensity: 0.5
    });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    const light = new THREE.PointLight(0x818cf8, 2, 50);
    light.position.set(10, 10, 10);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x0f172a, 2));

    let mouseX = 0, mouseY = 0;
    window.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX - window.innerWidth / 2) * 0.001;
        mouseY = (e.clientY - 130) * 0.001;
    });

    function animate() {
      requestAnimationFrame(animate);
      mesh.rotation.x += 0.003 + mouseY * 0.02;
      mesh.rotation.y += 0.005 + mouseX * 0.02;
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / 260;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, 260);
    });
  </script>
</body>
</html>
"""
components.html(three_html, height=270)

# Sidebar
with st.sidebar:
    st.header("⚡ System Navigation")
    view_panel = st.radio("Navigation Panel", ["Public Portfolio", "Admin Console"])
    st.divider()
    st.markdown("""
    **Direct Channels:**
    - 💼 [GitHub Profile](https://github.com/abhibhdauriya)
    - 📷 [Instagram Portfolio](https://instagram.com)
    - 📺 [YouTube Channel](https://youtube.com)
    """)

# ----------------- ADMIN PANEL -----------------
if view_panel == "Admin Console":
    st.subheader("🛡️ Executive Admin Dashboard")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    # Fetch stored password & email from DB
    pass_res = execute_query("SELECT value FROM settings WHERE key = 'admin_pass'")
    current_admin_pass = pass_res[0][0] if pass_res else "Abhi#Enterprise2026"
    
    email_res = execute_query("SELECT value FROM settings WHERE key = 'admin_email'")
    current_admin_email = email_res[0][0] if email_res else "admin@example.com"

    if not st.session_state.admin_logged_in:
        col_login, col_forgot = st.columns([1.2, 1])

        with col_login:
            st.markdown("#### Login to Console")
            entered_pass = st.text_input("Enter Passkey", type="password")
            if st.button("Unlock Admin Session", use_container_width=True):
                if entered_pass == current_admin_pass:
                    st.session_state.admin_logged_in = True
                    st.balloons()
                    st.toast("🎉 Logged In Successfully!", icon="✅")
                    st.rerun()
                else:
                    st.error("Incorrect Passkey. Please try again.")

        with col_forgot:
            with st.expander("Forgot Password / Recovery via Email"):
                recovery_email = st.text_input("Registered Email Address")
                if st.button("Request Reset OTP"):
                    if recovery_email.strip().lower() == current_admin_email.strip().lower():
                        otp = str(random.randint(100000, 999999))
                        st.session_state.reset_otp = otp
                        st.session_state.otp_target_email = recovery_email
                        success, msg = send_reset_email(recovery_email, otp)
                        if success:
                            st.success(msg)
                        else:
                            st.warning(f"Could not send email automatically: {msg}. (Development Hint: Use OTP: {otp})")
                    else:
                        st.error("Email does not match registered admin email.")

                if "reset_otp" in st.session_state:
                    entered_otp = st.text_input("Enter 6-digit OTP")
                    new_rec_pass = st.text_input("Set New Password", type="password")
                    if st.button("Verify OTP & Update Password"):
                        if entered_otp == st.session_state.reset_otp and len(new_rec_pass) >= 4:
                            execute_query("UPDATE settings SET value = ? WHERE key = 'admin_pass'", [new_rec_pass])
                            del st.session_state.reset_otp
                            st.success("Password changed successfully! You can now log in.")
                            st.rerun()
                        else:
                            st.error("Invalid OTP or password too short.")

    else:
        # LOGGED IN ADMIN ACTIONS
        c_head1, c_head2 = st.columns([3, 1])
        c_head1.success("Authorized Admin Session Active")
        if c_head2.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()

        admin_tabs = st.tabs(["➕ Add New Project", "📝 Manage Existing Projects", "🔑 Change Password & Email"])

        # TAB 1: ADD PROJECT
        with admin_tabs[0]:
            with st.form("add_project_form"):
                st.markdown("##### 1. Basic Details")
                ca, cb = st.columns(2)
                p_title = ca.text_input("Project / Pipeline Title*")
                p_cat = cb.selectbox("Category", [
                    "Manufacturing & CNC Tracking",
                    "Excel VBA Macro Engines",
                    "Web Dashboards & Streamlit",
                    "AI Document & Statement Parsing"
                ])
                p_video = st.text_input("Reel / Video URL (YouTube Link or Direct MP4)")
                p_prob = st.text_area("The Operational Problem (Bottleneck)*")
                p_sol = st.text_area("The Solution & Business Impact*")
                p_tech = st.text_input("Tech Stack Tags (e.g., Python, Excel VBA, Turso, Streamlit)")
                
                st.markdown("##### 2. Direct Links & Phone Contact")
                cc, cd, ce = st.columns(3)
                p_live = cc.text_input("Live Deployed Web URL")
                p_git = cd.text_input("GitHub Repo URL")
                p_phone = ce.text_input("Direct Contact / WhatsApp (+91XXXXXXXXXX)")

                st.markdown("##### 3. Direct File Attachments (Excel / VBA Macro .xlsm)")
                cf, cg = st.columns(2)
                raw_file = cf.file_uploader("Upload Raw Excel File (.xlsx, .csv)", type=["xlsx", "xls", "csv"])
                vba_file = cg.file_uploader("Upload VBA Macro-Enabled File (.xlsm, .xlsx)", type=["xlsm", "xlsx", "xls"])

                btn_add = st.form_submit_button("🚀 Deploy Project to Turso Cloud DB", use_container_width=True)
                if btn_add and p_title and p_prob and p_sol:
                    raw_b64 = base64.b64encode(raw_file.read()).decode("utf-8") if raw_file else ""
                    raw_name = raw_file.name if raw_file else ""
                    
                    vba_b64 = base64.b64encode(vba_file.read()).decode("utf-8") if vba_file else ""
                    vba_name = vba_file.name if vba_file else ""

                    execute_query("""
                    INSERT INTO projects 
                    (title, category, video_url, problem, solution, tech_stack, live_link, github_link, phone_contact, excel_raw_name, excel_raw_data, excel_proc_name, excel_proc_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [p_title, p_cat, p_video, p_prob, p_sol, p_tech, p_live, p_git, p_phone, raw_name, raw_b64, vba_name, vba_b64])
                    st.success(f"Project '{p_title}' added successfully!")
                    st.rerun()

        # TAB 2: MANAGE & EDIT / DELETE PROJECTS
        with admin_tabs[1]:
            st.markdown("##### Existing Database Projects")
            projects = execute_query("SELECT id, title, category, video_url, problem, solution, tech_stack, live_link, github_link, phone_contact FROM projects ORDER BY id DESC")
            
            if not projects or len(projects) == 0:
                st.info("No custom projects in database yet.")
            else:
                for row in projects:
                    (pid, title, cat, video, prob, sol, tech, live, git, phone) = row
                    with st.expander(f"📦 ID #{pid} - {title} ({cat})"):
                        with st.form(f"edit_form_{pid}"):
                            e_title = st.text_input("Title", value=title)
                            e_cat = st.selectbox("Category", [
                                "Manufacturing & CNC Tracking",
                                "Excel VBA Macro Engines",
                                "Web Dashboards & Streamlit",
                                "AI Document & Statement Parsing"
                            ], index=0)
                            e_video = st.text_input("Video URL", value=video or "")
                            e_prob = st.text_area("Problem", value=prob)
                            e_sol = st.text_area("Solution", value=sol)
                            e_tech = st.text_input("Tech Stack", value=tech or "")
                            
                            c_e1, c_e2, c_e3 = st.columns(3)
                            e_live = c_e1.text_input("Live Link", value=live or "")
                            e_git = c_e2.text_input("GitHub Link", value=git or "")
                            e_phone = c_e3.text_input("Phone/WhatsApp", value=phone or "")

                            col_u1, col_u2 = st.columns(2)
                            btn_update = col_u1.form_submit_button("💾 Save Changes", use_container_width=True)
                            if btn_update:
                                execute_query("""
                                UPDATE projects 
                                SET title=?, category=?, video_url=?, problem=?, solution=?, tech_stack=?, live_link=?, github_link=?, phone_contact=?
                                WHERE id=?
                                """, [e_title, e_cat, e_video, e_prob, e_sol, e_tech, e_live, e_git, e_phone, pid])
                                st.success("Updated successfully!")
                                st.rerun()
                        
                        # Delete action outside form to prevent accidental triggers
                        if st.button(f"🗑️ Delete Project #{pid}", key=f"del_{pid}", use_container_width=True):
                            execute_query("DELETE FROM projects WHERE id = ?", [pid])
                            st.warning(f"Project #{pid} deleted.")
                            st.rerun()

        # TAB 3: PASSWORD & SETTINGS
        with admin_tabs[2]:
            st.markdown("##### 🔐 Update Admin Security Credentials")
            old_p = st.text_input("Current Passkey", type="password")
            new_p = st.text_input("New Passkey", type="password")
            new_email = st.text_input("Recovery Email Address", value=current_admin_email)
            
            if st.button("Apply New Credentials", use_container_width=True):
                if old_p == current_admin_pass:
                    if len(new_p) >= 4:
                        execute_query("UPDATE settings SET value = ? WHERE key = 'admin_pass'", [new_p])
                        execute_query("UPDATE settings SET value = ? WHERE key = 'admin_email'", [new_email])
                        st.success("Credentials updated successfully!")
                        st.rerun()
                    else:
                        st.error("New password must be at least 4 characters.")
                else:
                    st.error("Current password incorrect.")

# ----------------- USER PUBLIC VIEW -----------------
else:
    records = []
    try:
        records = execute_query("SELECT id, title, category, video_url, problem, solution, tech_stack, live_link, github_link, phone_contact, excel_raw_name, excel_raw_data, excel_proc_name, excel_proc_data FROM projects ORDER BY id DESC")
    except Exception:
        pass

    if not records or len(records) == 0:
        records = [[
            0,
            "Shop-Floor Multi-Machine Visibility Engine (TRD 10X/30X/50X)",
            "Manufacturing & CNC Tracking",
            "",
            "28 CNC cutting machines faced manual reporting latency of 4 hours per shift and Excel file-locking errors.",
            "Architected a dual-layer system: Local VBA client feeding a centralized SQLite database with automated OEE calculation.",
            "Excel VBA, Python, OpenPyXL, SQLite, Streamlit",
            "https://streamlit.io",
            "https://github.com/abhibhdauriya",
            "+919876543210",
            "", "", "", ""
        ]]

    for r in records:
        (p_id, title, cat, video, problem, solution, tech, live, git, phone, r_name, r_data, v_name, v_data) = r

        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <span class="badge">{cat}</span>
                <h3 style="margin: 8px 0; color: #f8fafc;">{title}</h3>
            </div>
            """, unsafe_allow_html=True)

            col_media, col_desc = st.columns([1, 1.2])

            with col_media:
                if video:
                    if "youtube" in video or "youtu.be" in video:
                        st.video(video)
                    else:
                        st.markdown(f"""
                        <video width="100%" height="280" controls style="border-radius: 8px; border: 1px solid #1e293b;">
                            <source src="{video}" type="video/mp4">
                        </video>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="height: 180px; background: #090d16; border: 1px dashed #334155; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8;">
                        ⚡ System Architecture & Code Pipeline
                    </div>
                    """, unsafe_allow_html=True)

                # Direct File Download Triggers
                if (r_data and r_name) or (v_data and v_name):
                    st.write("**Direct File Downloads:**")
                    fcol1, fcol2 = st.columns(2)
                    if r_data and r_name:
                        raw_bytes = base64.b64decode(r_data)
                        fcol1.download_button(
                            label=f"📥 Raw Data ({r_name})",
                            data=raw_bytes,
                            file_name=r_name,
                            use_container_width=True
                        )
                    if v_data and v_name:
                        vba_bytes = base64.b64decode(v_data)
                        fcol2.download_button(
                            label=f"📊 VBA Tool ({v_name})",
                            data=vba_bytes,
                            file_name=v_name,
                            use_container_width=True
                        )

            with col_desc:
                st.markdown(f"""
                <div class="metric-card">
                    <strong style="color: #f87171;">Problem:</strong><br>
                    <span style="color: #cbd5e1; font-size: 0.92rem;">{problem}</span>
                </div>
                <div class="metric-card">
                    <strong style="color: #34d399;">Solution & Impact:</strong><br>
                    <span style="color: #cbd5e1; font-size: 0.92rem;">{solution}</span>
                </div>
                """, unsafe_allow_html=True)

                if tech:
                    st.write("**Tech Stack:**")
                    badges = " ".join([f'<span class="badge">{t.strip()}</span>' for t in tech.split(",") if t.strip()])
                    st.markdown(badges, unsafe_allow_html=True)

                st.write("")
                b1, b2, b3 = st.columns(3)
                if live:
                    b1.link_button("🚀 Live App", live, use_container_width=True)
                if git:
                    b2.link_button("💻 GitHub Repo", git, use_container_width=True)
                if phone:
                    clean_phone = phone.replace("+", "").replace(" ", "")
                    b3.link_button("📱 WhatsApp / Call", f"https://wa.me/{clean_phone}", use_container_width=True)

            st.divider()
