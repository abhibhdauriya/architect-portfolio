import streamlit as st
import streamlit.components.v1 as components
from db import init_db, execute_query

st.set_page_config(
    page_title="Automation & Systems Portfolio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_db()

st.markdown("""
<style>
    .stApp { background-color: #050811; color: #f1f5f9; }
    .project-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
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

# 3D Interactive Three.js Canvas
three_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; overflow: hidden; background: #050811; }
    canvas { display: block; width: 100vw; height: 300px; }
    #tagline {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: #ffffff;
        font-family: sans-serif;
        pointer-events: none;
    }
    h1 { margin: 0; font-size: 2rem; font-weight: 800; }
    p { margin: 6px 0 0; font-size: 0.9rem; color: #818cf8; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
  <div id="tagline">
    <h1>B2B AUTOMATION & SYSTEMS ARCHITECT</h1>
    <p>Shop-Floor Dashboards • Excel VBA Engines • AI Workflows</p>
  </div>
  <canvas id="canvas"></canvas>
  <script>
    const canvas = document.getElementById('canvas');
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, 300);
    renderer.setPixelRatio(window.devicePixelRatio);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 300, 0.1, 1000);
    camera.position.z = 20;

    const geometry = new THREE.TorusKnotGeometry(6, 1.8, 100, 16);
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
        mouseY = (e.clientY - 150) * 0.001;
    });

    function animate() {
      requestAnimationFrame(animate);
      mesh.rotation.x += 0.004 + mouseY * 0.03;
      mesh.rotation.y += 0.006 + mouseX * 0.03;
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / 300;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, 300);
    });
  </script>
</body>
</html>
"""
components.html(three_html, height=310)

with st.sidebar:
    st.header("⚡ System Control")
    view_panel = st.radio("Select View Mode", ["Portfolio (Public)", "Admin Console"])
    st.divider()
    st.markdown("""
    - ✉️ **Email:** contact@abhisheksingh.dev
    - 💼 [GitHub Profile](https://github.com)
    - 📷 [Instagram Portfolio](https://instagram.com)
    - 📺 [YouTube Channel](https://youtube.com)
    """)

if view_panel == "Admin Console":
    st.subheader("🛡️ Executive Admin Dashboard")
    entered_key = st.text_input("Enter Admin Security Key", type="password")
    admin_secret = st.secrets.get("ADMIN_KEY", "Abhi#Enterprise2026")

    if entered_key == admin_secret:
        st.success("Authenticated Session.")
        with st.form("new_project_entry"):
            col1, col2 = st.columns(2)
            p_title = col1.text_input("Project / Pipeline Title*")
            p_cat = col2.selectbox("Industry Category", [
                "Manufacturing & CNC Tracking",
                "Excel VBA Offline Systems",
                "Web Dashboards & Streamlit",
                "AI Document & Statement Parsing"
            ])
            p_video = st.text_input("Reel / Video Link (YouTube Embed or direct MP4 URL)")
            p_prob = st.text_area("Operational Bottleneck (The Problem)*")
            p_sol = st.text_area("Engineering Fix & Business Impact (The Solution)*")
            p_tech = st.text_input("Tech Stack Tags (e.g., Python, VBA, Streamlit, Turso)")
            
            c3, c4 = st.columns(2)
            p_live = c3.text_input("Live Deployed App URL")
            p_git = c4.text_input("GitHub Source Code URL")

            c5, c6 = st.columns(2)
            p_raw = c5.text_input("Raw Excel Dataset URL")
            p_proc = c6.text_input("VBA Processed Excel Download URL")

            btn_save = st.form_submit_button("Commit to Cloud Turso DB")
            if btn_save and p_title and p_prob and p_sol:
                execute_query("""
                INSERT INTO projects 
                (title, category, video_url, problem, solution, tech_stack, live_link, github_link, excel_raw_link, excel_proc_link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [p_title, p_cat, p_video, p_prob, p_sol, p_tech, p_live, p_git, p_raw, p_proc])
                st.success(f"Project '{p_title}' added successfully!")
                st.rerun()
    else:
        st.info("Input valid security key to modify database.")
else:
    records = execute_query("SELECT id, title, category, video_url, problem, solution, tech_stack, live_link, github_link, excel_raw_link, excel_proc_link FROM projects ORDER BY id DESC")

    if not records:
        records = [[
            0,
            "Shop-Floor Multi-Machine Visibility Engine (TRD 10X/30X/50X)",
            "Manufacturing & CNC Tracking",
            "",
            "28 CNC cutting machines faced manual reporting latency of 4 hours per shift and Excel file-locking errors.",
            "Architected a dual-layer system: Local VBA client feeding a centralized SQLite database with automated OEE calculation.",
            "Excel VBA, Python, OpenPyXL, SQLite, Streamlit",
            "https://streamlit.io",
            "https://github.com",
            "",
            ""
        ]]

    for r in records:
        (p_id, title, cat, video, problem, solution, tech, live, git, raw_xl, proc_xl) = r

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
                        <video width="100%" height="300" controls style="border-radius: 8px; border: 1px solid #1e293b;">
                            <source src="{video}" type="video/mp4">
                        </video>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="height: 180px; background: #090d16; border: 1px dashed #334155; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #64748b;">
                        ⚡ Architecture Showcase
                    </div>
                    """, unsafe_allow_html=True)
                
                st.write("**Data Files:**")
                dcol1, dcol2 = st.columns(2)
                if raw_xl:
                    dcol1.link_button("📥 Raw Excel", raw_xl, use_container_width=True)
                if proc_xl:
                    dcol2.link_button("📊 Processed VBA File", proc_xl, use_container_width=True)

            with col_desc:
                st.markdown(f"""
                <div class="metric-card">
                    <strong style="color: #f87171;">Problem:</strong><br>
                    <span style="color: #cbd5e1; font-size: 0.92rem;">{problem}</span>
                </div>
                <div class="metric-card">
                    <strong style="color: #34d399;">Solution:</strong><br>
                    <span style="color: #cbd5e1; font-size: 0.92rem;">{solution}</span>
                </div>
                """, unsafe_allow_html=True)

                st.write("**Tech Stack:**")
                badges = " ".join([f'<span class="badge">{t.strip()}</span>' for t in tech.split(",") if t.strip()])
                st.markdown(badges, unsafe_allow_html=True)

                st.write("")
                b1, b2 = st.columns(2)
                if live:
                    b1.link_button("🚀 Live App", live, use_container_width=True)
                if git:
                    b2.link_button("💻 GitHub Repository", git, use_container_width=True)

            st.divider()
