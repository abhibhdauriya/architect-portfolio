import streamlit as st
import streamlit.components.v1 as components
import base64
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

def get_db_setting(key, fallback=""):
    try:
        rows, err = execute_query("SELECT value FROM settings WHERE key = ?", [key])
        if rows and len(rows) > 0 and len(rows[0]) > 0 and rows[0][0]:
            return rows[0][0]
    except Exception:
        pass
    return fallback

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

# 3D Three.js Interactive Canvas
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

current_admin_pass = get_db_setting("admin_pass", "Abhi#Enterprise2026")
current_admin_email = get_db_setting("admin_email", "singha36161@gmail.com")
current_global_phone = get_db_setting("whatsapp_phone", "+918810915344")
resume_data_b64 = get_db_setting("resume_data", "")
resume_file_name = get_db_setting("resume_name", "Abhishek_Singh_Resume.pdf")

# Header Actions
hcol1, hcol2 = st.columns([1, 1])
with hcol1:
    clean_p = current_global_phone.replace("+", "").replace(" ", "")
    st.link_button(f"💬 WhatsApp ({current_global_phone})", f"https://wa.me/{clean_p}", use_container_width=True)
with hcol2:
    if resume_data_b64:
        try:
            res_bytes = base64.b64decode(resume_data_b64)
            st.download_button(
                label=f"📄 Download CV ({resume_file_name})",
                data=res_bytes,
                file_name=resume_file_name,
                mime="application/pdf",
                use_container_width=True
            )
        except Exception:
            st.button("📄 Resume Not Found", disabled=True, use_container_width=True)
    else:
        st.info("Upload resume from Admin Panel")

# Sidebar
with st.sidebar:
    st.header("⚡ System Navigation")
    view_panel = st.radio("Navigation Panel", ["Public Portfolio", "Admin Console"])
    st.divider()
    st.markdown(f"""
    **Contact:**
    - ✉️ {current_admin_email}
    - 📱 {current_global_phone}
    - 💼 [GitHub Profile](https://github.com/abhibhdauriya)
    """)

# ----------------- ADMIN PANEL -----------------
if view_panel == "Admin Console":
    st.subheader("🛡️ Executive Admin Dashboard")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.markdown("#### Login to Console")
        entered_pass = st.text_input("Enter Passkey", type="password")
        if st.button("Unlock Admin Session", use_container_width=True):
            if entered_pass == current_admin_pass:
                st.session_state.admin_logged_in = True
                st.toast("🎉 Logged In Successfully!", icon="✅")
                st.balloons()
                st.rerun()
            else:
                st.error("Incorrect Passkey.")
    else:
        c_head1, c_head2 = st.columns([3, 1])
        c_head1.success("Authorized Admin Session Active")
        if c_head2.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()

        admin_tabs = st.tabs(["➕ Add New Project", "📝 Manage Projects", "📄 Upload Resume", "⚙️ Phone & Security"])

        # TAB 1: ADD PROJECT
        with admin_tabs[0]:
            st.markdown("##### 1. Basic Project Details")
            ca, cb = st.columns(2)
            p_title = ca.text_input("Project / Pipeline Title*", key="add_p_title")
            p_cat = cb.selectbox("Category", [
                "Manufacturing & CNC Tracking",
                "Excel VBA Macro Engines",
                "Web Dashboards & Streamlit",
                "AI Document & Statement Parsing"
            ], key="add_p_cat")
            p_video = st.text_input("Reel / Video URL (Instagram Reel, YouTube, or MP4)", key="add_p_video")
            p_prob = st.text_area("The Operational Problem (Bottleneck)*", key="add_p_prob")
            p_sol = st.text_area("The Solution & Business Impact*", key="add_p_sol")
            p_tech = st.text_input("Tech Stack Tags", value="Python, Streamlit, Advanced Excel, ERP (Nexs), Grafana", key="add_p_tech")
            
            st.markdown("##### 2. Direct Links & Phone Contact")
            cc, cd, ce = st.columns(3)
            p_live = cc.text_input("Live Deployed URL", key="add_p_live")
            p_git = cd.text_input("GitHub URL", key="add_p_git")
            p_phone = ce.text_input("Contact WhatsApp", value=current_global_phone, key="add_p_phone")

            st.markdown("##### 3. Excel Attachments")
            cf, cg = st.columns(2)
            raw_file = cf.file_uploader("Upload Raw Excel", type=["xlsx", "xls", "csv"], key="raw_file_input")
            vba_file = cg.file_uploader("Upload VBA Macro File", type=["xlsm", "xlsx", "xls"], key="vba_file_input")

            if st.button("🚀 Deploy Project to Turso Cloud DB", use_container_width=True, type="primary"):
                if not p_title.strip() or not p_prob.strip() or not p_sol.strip():
                    st.error("Kripya Title, Problem aur Solution fill karein.")
                else:
                    raw_b64 = base64.b64encode(raw_file.read()).decode("utf-8") if raw_file else ""
                    raw_name = raw_file.name if raw_file else ""
                    
                    vba_b64 = base64.b64encode(vba_file.read()).decode("utf-8") if vba_file else ""
                    vba_name = vba_file.name if vba_file else ""

                    res, err = execute_query("""
                    INSERT INTO projects 
                    (title, category, video_url, problem, solution, tech_stack, live_link, github_link, phone_contact, excel_raw_name, excel_raw_data, excel_proc_name, excel_proc_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [p_title, p_cat, p_video, p_prob, p_sol, p_tech, p_live, p_git, p_phone, raw_name, raw_b64, vba_name, vba_b64])
                    
                    if err:
                        st.error(f"Turso DB Error: {err}")
                    else:
                        st.toast("🎉 Project Turso Database par deploy ho gaya!", icon="✅")
                        st.success(f"Project '{p_title}' live ho chuka hai!")
                        st.balloons()

        # TAB 2: MANAGE & EDIT
        with admin_tabs[1]:
            st.markdown("##### Existing Database Projects")
            projects, err = execute_query("SELECT id, title, category, video_url, problem, solution, tech_stack, live_link, github_link, phone_contact FROM projects ORDER BY id DESC")
            
            if not projects or len(projects) == 0:
                st.info("Database me abhi koi custom project nahi hai.")
            else:
                for row in projects:
                    (pid, title, cat, video, prob, sol, tech, live, git, phone) = row
                    with st.expander(f"📦 ID #{pid} - {title}"):
                        e_title = st.text_input(f"Title #{pid}", value=title)
                        e_cat = st.selectbox(f"Category #{pid}", [
                            "Manufacturing & CNC Tracking",
                            "Excel VBA Macro Engines",
                            "Web Dashboards & Streamlit",
                            "AI Document & Statement Parsing"
                        ], index=0)
                        e_video = st.text_input(f"Video URL #{pid}", value=video or "")
                        e_prob = st.text_area(f"Problem #{pid}", value=prob)
                        e_sol = st.text_area(f"Solution #{pid}", value=sol)
                        e_tech = st.text_input(f"Tech Stack #{pid}", value=tech or "")
                        e_live = st.text_input(f"Live Link #{pid}", value=live or "")
                        e_git = st.text_input(f"GitHub Link #{pid}", value=git or "")
                        e_phone = st.text_input(f"Phone #{pid}", value=phone or current_global_phone)

                        c_u1, c_u2 = st.columns(2)
                        if c_u1.button(f"💾 Save Changes #{pid}", key=f"save_{pid}", use_container_width=True):
                            _, upd_err = execute_query("""
                            UPDATE projects 
                            SET title=?, category=?, video_url=?, problem=?, solution=?, tech_stack=?, live_link=?, github_link=?, phone_contact=?
                            WHERE id=?
                            """, [e_title, e_cat, e_video, e_prob, e_sol, e_tech, e_live, e_git, e_phone, pid])
                            if upd_err:
                                st.error(f"Update failed: {upd_err}")
                            else:
                                st.toast("Changes Saved Successfully!", icon="✅")
                                st.rerun()

                        if c_u2.button(f"🗑️ Delete Project #{pid}", key=f"del_{pid}", use_container_width=True):
                            execute_query("DELETE FROM projects WHERE id = ?", [pid])
                            st.toast("Project Deleted!", icon="🗑️")
                            st.rerun()

        # TAB 3: RESUME
        with admin_tabs[2]:
            st.markdown("##### 📄 Upload Resume PDF")
            uploaded_pdf = st.file_uploader("Upload PDF CV", type=["pdf"], key="admin_resume_upload")
            if uploaded_pdf and st.button("Set as Active Resume", use_container_width=True):
                res_b64 = base64.b64encode(uploaded_pdf.read()).decode("utf-8")
                execute_query("INSERT OR REPLACE INTO settings (key, value) VALUES ('resume_data', ?)", [res_b64])
                execute_query("INSERT OR REPLACE INTO settings (key, value) VALUES ('resume_name', ?)", [uploaded_pdf.name])
                st.toast("Resume Uploaded Successfully!", icon="✅")
                st.success("Resume updated on Public Portfolio.")
                st.rerun()

        # TAB 4: SETTINGS
        with admin_tabs[3]:
            st.markdown("##### ⚙️ Contact & Credentials")
            new_phone = st.text_input("WhatsApp Number", value=current_global_phone)
            new_email = st.text_input("Notification Email", value=current_admin_email)
            if st.button("Save Contact Details", use_container_width=True):
                execute_query("INSERT OR REPLACE INTO settings (key, value) VALUES ('whatsapp_phone', ?)", [new_phone])
                execute_query("INSERT OR REPLACE INTO settings (key, value) VALUES ('admin_email', ?)", [new_email])
                st.toast("Contact details updated!", icon="✅")
                st.rerun()

            st.divider()
            old_p = st.text_input("Current Passkey", type="password")
            new_p = st.text_input("New Passkey", type="password")
            if st.button("Update Passkey", use_container_width=True):
                if old_p == current_admin_pass:
                    if len(new_p) >= 4:
                        execute_query("INSERT OR REPLACE INTO settings (key, value) VALUES ('admin_pass', ?)", [new_p])
                        st.toast("Passkey Changed!", icon="🔐")
                        st.rerun()
                    else:
                        st.error("Min 4 characters required.")
                else:
                    st.error("Current password incorrect.")

# ----------------- USER PUBLIC VIEW -----------------
else:
    records, err = execute_query("SELECT id, title, category, video_url, problem, solution, tech_stack, live_link, github_link, phone_contact, excel_raw_name, excel_raw_data, excel_proc_name, excel_proc_data FROM projects ORDER BY id DESC")

    if not records or len(records) == 0:
        records = [[
            1,
            "Lenskart Dispatch Handover & Operations MIS Dashboard",
            "Web Dashboards & Streamlit",
            "",
            "At Lenskart Bhiwadi facility handling ~35,000+ units daily, shift handovers suffered from manual logging delays, double-scanning errors, and packet mismatches.",
            "Engineered a real-time Streamlit analytics engine tracking Scanned, Soft, Missing, and Excess units. Delivered 100% NDD target compliance and eliminated end-of-shift reporting delays.",
            "Python, Streamlit, Advanced Excel, ERP (Nexs), Grafana",
            "https://abhishek-handover-dashboard.streamlit.app/",
            "https://github.com/abhibhdauriya",
            current_global_phone,
            "", "", "", ""
        ]]

    for r in records:
        (p_id, title, cat, video, problem, solution, tech, live, git, phone, r_name, r_data, v_name, v_data) = r
        project_phone = phone if phone else current_global_phone

        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <span class="badge">{cat}</span>
                <h3 style="margin: 8px 0; color: #f8fafc;">{title}</h3>
            </div>
            """, unsafe_allow_html=True)

            col_media, col_desc = st.columns([1, 1.2])

            with col_media:
                if video and video.strip():
                    v_url = video.strip()
                    # 1. Instagram Reel Embed (Fixes Black Screen CORS Error)
                    if "instagram.com" in v_url:
                        clean_insta = v_url.split("?")[0].rstrip("/")
                        if not clean_insta.endswith("/embed"):
                            clean_insta = f"{clean_insta}/embed"
                        components.iframe(clean_insta, height=480, scrolling=False)
                    
                    # 2. YouTube Video / Short
                    elif "youtube.com" in v_url or "youtu.be" in v_url:
                        st.video(v_url)
                    
                    # 3. Direct MP4 Video
                    else:
                        st.markdown(f"""
                        <video width="100%" height="280" controls style="border-radius: 8px; border: 1px solid #1e293b;">
                            <source src="{v_url}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="height: 180px; background: #090d16; border: 1px dashed #334155; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8;">
                        ⚡ System Architecture & Code Pipeline
                    </div>
                    """, unsafe_allow_html=True)

                if (r_data and r_name) or (v_data and v_name):
                    st.write("**Data Artifacts & Downloads:**")
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
                
                clean_item_phone = project_phone.replace("+", "").replace(" ", "")
                b3.link_button("💬 WhatsApp", f"https://wa.me/{clean_item_phone}", use_container_width=True)

            st.divider()

    # Footer Direct Contact
    st.markdown("### 📬 Get In Touch / Send a Direct Message")
    with st.container():
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        c_name = st.text_input("Aapka Naam*", key="cnt_name")
        c_email = st.text_input("Aapka Email*", key="cnt_email")
        c_msg = st.text_area("Message / Requirement*", key="cnt_msg")
        if st.button("✉️ Send Message to Abhishek", use_container_width=True):
            if not c_name or not c_email or not c_msg:
                st.error("Kripya saare fields bharein.")
            else:
                st.toast("Message Received!", icon="🚀")
                st.success(f"Dhanyawad {c_name}! Aapka message receive ho chuka hai.")
        st.markdown('</div>', unsafe_allow_html=True)
