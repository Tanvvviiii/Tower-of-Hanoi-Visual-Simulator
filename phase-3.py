import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time

st.set_page_config(
    page_title="Tower of Hanoi | Visual Simulator",
    page_icon="🗼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d1b, #11152b, #17132e);
    color: #f8fafc;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, p, label, span {
    color: #f1f5f9;
}

.main-title {
    font-size: 40px;
    font-weight: 850;
    text-align: center;
    background: linear-gradient(90deg, #22d3ee, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 15px 0 5px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 30px;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1c2540, #171b32);
    border: 1px solid #35416a;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 20px #00000040;
}

[data-testid="stMetricLabel"] {
    color: #a5b4fc !important;
}

[data-testid="stMetricValue"] {
    color: #22d3ee !important;
    font-weight: bold;
}

.stButton > button {
    background: linear-gradient(90deg, #6d28d9, #2563eb);
    color: white;
    border: 1px solid #818cf8;
    border-radius: 12px;
    padding: 10px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    border: 1px solid #22d3ee;
    color: #22d3ee;
    transform: translateY(-2px);
}

section[data-testid="stSidebar"] {
    background: #10172a;
    border-right: 1px solid #35416a;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #06b6d4, #8b5cf6);
}

.info-card {
    background: #1c2540;
    border: 1px solid #39466b;
    border-radius: 15px;
    padding: 18px;
    margin: 8px 0;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🗼 TOWER OF HANOI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive Puzzle • Algorithm Visualization • '
    'Smart Move Tracking</div>',
    unsafe_allow_html=True
)

def solve_hanoi(n, source, auxiliary, destination, moves):
    if n == 1:
        moves.append((1, source, destination))
        return

    solve_hanoi(n - 1, source, destination, auxiliary, moves)
    moves.append((n, source, destination))
    solve_hanoi(n - 1, auxiliary, source, destination, moves)

def initialize_game(n):
    moves = []
    solve_hanoi(n, "A", "B", "C", moves)

    st.session_state.moves = moves
    st.session_state.disk_count = n
    st.session_state.step = 0

def get_rods(n, moves, step):
    rods = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": []
    }

    for disk, source, destination in moves[:step]:
        rods[source].pop()
        rods[destination].append(disk)

    return rods

def draw_towers(n, rods, step, total):
    fig, ax = plt.subplots(figsize=(11, 5.5))

    fig.patch.set_facecolor("#11152b")
    ax.set_facecolor("#11152b")

    positions = {"A": 1.5, "B": 4.5, "C": 7.5}

    colors = [
        "#22d3ee", "#a78bfa", "#f472b6", "#fbbf24",
        "#34d399", "#fb7185", "#818cf8", "#38bdf8"
    ]

    ax.set_xlim(0, 9)
    ax.set_ylim(0, n + 2)

    for rod, x in positions.items():

        ax.add_patch(Rectangle(
            (x - 0.045, 0.55),
            0.09, n + 0.55,
            color="#94a3b8"
        ))

        ax.add_patch(Rectangle(
            (x - 1.2, 0.4),
            2.4, 0.15,
            color="#64748b"
        ))

        for level, disk in enumerate(rods[rod]):
            width = 0.38 + disk * 0.19

            ax.add_patch(Rectangle(
                (x - width / 2, 0.65 + level * 0.48),
                width, 0.43,
                facecolor=colors[(disk - 1) % len(colors)],
                edgecolor="white",
                linewidth=1.3
            ))

            ax.text(
                x,
                0.86 + level * 0.48,
                str(disk),
                ha="center",
                va="center",
                color="#10172a",
                fontsize=11,
                fontweight="bold"
            )

        ax.text(
            x, 0.05,
            f"ROD {rod}",
            ha="center",
            color="#22d3ee",
            fontsize=13,
            fontweight="bold"
        )

    ax.set_title(
        f"MOVEMENT VISUALIZATION  |  {step} / {total}",
        color="#e2e8f0",
        fontsize=15,
        fontweight="bold",
        pad=20
    )

    ax.axis("off")
    fig.tight_layout()

    return fig

if "disk_count" not in st.session_state:
    initialize_game(3)

st.sidebar.markdown("## ⚙️ GAME SETTINGS")

disk_count = st.sidebar.slider(
    "🔵 Select Number of Disks",
    1, 8,
    st.session_state.disk_count
)

speed = st.sidebar.slider(
    "⚡ Animation Speed",
    0.1, 1.5,
    0.5,
    0.1
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 OBJECTIVE")
st.sidebar.info(
    "Move all disks from Rod A to Rod C "
    "using Rod B without breaking the rules."
)

if disk_count != st.session_state.disk_count:
    initialize_game(disk_count)

moves = st.session_state.moves
step = st.session_state.step
minimum_moves = 2 ** disk_count - 1

st.markdown("### 📊 GAME STATISTICS")

c1, c2, c3 = st.columns(3)

c1.metric("🔵 TOTAL DISKS", disk_count)
c2.metric("🎯 MINIMUM MOVES", minimum_moves)
c3.metric("⚡ CURRENT MOVE", step)

st.progress(step / minimum_moves)

st.markdown("### 🎮 LIVE PUZZLE VISUALIZATION")

rods = get_rods(disk_count, moves, step)

fig = draw_towers(disk_count, rods, step, minimum_moves)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

if step == minimum_moves:
    st.success("🏆 CONGRATULATIONS! PUZZLE COMPLETED!")
elif step == 0:
    st.info("🚀 Ready to start! All disks are on Rod A.")
else:
    disk, source, destination = moves[step - 1]
    st.info(
        f"Last move: Disk {disk} moved from Rod "
        f"{source} to Rod {destination}"
    )

st.markdown("### 🎛️ MOVEMENT CONTROLS")

b1, b2, b3, b4 = st.columns(4)

with b1:
    if st.button("⏮ PREVIOUS", use_container_width=True):
        st.session_state.step = max(0, step - 1)
        st.rerun()

with b2:
    if st.button("NEXT ⏭", use_container_width=True):
        st.session_state.step = min(minimum_moves, step + 1)
        st.rerun()

with b3:
    if st.button("▶ PLAY ANIMATION", use_container_width=True):
        for current in range(step + 1, minimum_moves + 1):
            st.session_state.step = current

            current_rods = get_rods(
                disk_count, moves, current
            )

            current_fig = draw_towers(
                disk_count, current_rods,
                current, minimum_moves
            )

            placeholder = st.empty()
            placeholder.pyplot(
                current_fig, use_container_width=True
            )
            plt.close(current_fig)

            time.sleep(speed)

        st.rerun()

with b4:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.step = 0
        st.rerun()

st.markdown("---")

st.markdown("### 📘 RULES OF THE PUZZLE")

r1, r2 = st.columns(2)

with r1:
    st.markdown("""
    <div class="info-card">
    <b>01. One Disk</b><br>
    Move only one disk at a time.
    </div>
    <div class="info-card">
    <b>02. Top Disk</b><br>
    Only the top disk can be moved.
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="info-card">
    <b>03. Size Rule</b><br>
    Never place a larger disk on a smaller disk.
    </div>
    <div class="info-card">
    <b>04. Final Goal</b><br>
    Transfer every disk from Rod A to Rod C.
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 🧠 MINIMUM MOVE FORMULA")

st.latex(r"\text{Minimum Moves} = 2^n - 1")

st.markdown(
    f"""
    <div class="info-card">
    <h3 style="color:#22d3ee;">Calculation</h3>
    Number of disks = {disk_count}<br>
    Minimum moves = 2<sup>{disk_count}</sup> - 1<br>
    <h2 style="color:#a78bfa;">Answer = {minimum_moves} Moves</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="footer">TOWER OF HANOI VISUAL SIMULATOR '
    '| Python & Streamlit Project</div>',
    unsafe_allow_html=True
)
