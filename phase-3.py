import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import time

st.set_page_config(
    page_title="Tower of Hanoi Simulator",
    page_icon="🗼",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f2f7fb;
}
h1, h2, h3 {
    color: #164e63;
}
[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border-left: 4px solid #0891b2;
}
</style>
""", unsafe_allow_html=True)

st.title("🗼 Tower of Hanoi Visual Simulator")
st.write(
    "Explore the Tower of Hanoi puzzle with animated disk movements."
)

def solve_hanoi(n, source, auxiliary, destination, moves):
    if n == 1:
        moves.append((1, source, destination))
        return

    solve_hanoi(n - 1, source, destination, auxiliary, moves)
    moves.append((n, source, destination))
    solve_hanoi(n - 1, auxiliary, source, destination, moves)

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

def draw_towers(n, rods, step, total_moves):
    fig, ax = plt.subplots(figsize=(10, 5))

    rod_positions = {"A": 1, "B": 3, "C": 5}
    colors = ["#0ea5e9", "#22c55e", "#f97316",
              "#a855f7", "#eab308", "#ef4444",
              "#14b8a6", "#64748b"]

    ax.set_xlim(0, 6)
    ax.set_ylim(0, n + 2)
    ax.set_facecolor("#f8fafc")
    fig.patch.set_facecolor("#f8fafc")

    for rod, x in rod_positions.items():
        ax.add_patch(
            Rectangle((x - 0.04, 0.5), 0.08, n + 0.5,
                      color="#475569")
        )
        ax.text(x, 0.12, f"Rod {rod}",
                ha="center", fontsize=12, fontweight="bold")

        for level, disk in enumerate(rods[rod]):
            width = 0.35 + disk * 0.15
            color = colors[(disk - 1) % len(colors)]

            ax.add_patch(
                Rectangle(
                    (x - width / 2, 0.65 + level * 0.45),
                    width,
                    0.4,
                    facecolor=color,
                    edgecolor="#334155",
                    linewidth=1.2
                )
            )

            ax.text(
                x, 0.85 + level * 0.45, str(disk),
                ha="center", va="center",
                color="white", fontweight="bold"
            )

    ax.set_title(
        f"Tower of Hanoi — Move {step} of {total_moves}",
        fontsize=15, fontweight="bold", pad=15
    )
    ax.axis("off")
    fig.tight_layout()
    return fig

def initialize_game(n):
    moves = []
    solve_hanoi(n, "A", "B", "C", moves)
    st.session_state.moves = moves
    st.session_state.disk_count = n
    st.session_state.step = 0

if "disk_count" not in st.session_state:
    initialize_game(3)

st.sidebar.header("Game Settings")

disk_count = st.sidebar.slider(
    "Number of disks",
    min_value=1,
    max_value=8,
    value=st.session_state.disk_count
)

speed = st.sidebar.slider(
    "Animation delay (seconds)",
    min_value=0.1,
    max_value=1.5,
    value=0.5,
    step=0.1
)

if disk_count != st.session_state.disk_count:
    initialize_game(disk_count)

moves = st.session_state.moves
step = st.session_state.step
minimum_moves = 2 ** disk_count - 1

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Number of Disks", disk_count)
metric2.metric("Minimum Moves", minimum_moves)
metric3.metric("Current Move", step)

st.progress(step / minimum_moves)

chart_area = st.empty()
status_area = st.empty()

def show_current_state():
    rods = get_rods(
        st.session_state.disk_count,
        st.session_state.moves,
        st.session_state.step
    )

    fig = draw_towers(
        st.session_state.disk_count,
        rods,
        st.session_state.step,
        len(st.session_state.moves)
    )

    chart_area.pyplot(fig)
    plt.close(fig)

    if st.session_state.step == len(st.session_state.moves):
        status_area.success("🎉 Puzzle solved successfully!")
    elif st.session_state.step == 0:
        status_area.info("Start: All disks are on Rod A.")
    else:
        disk, source, destination = st.session_state.moves[
            st.session_state.step - 1
        ]
        status_area.info(
            f"Last move: Disk {disk} from Rod {source} to Rod {destination}"
        )

show_current_state()

st.subheader("🎮 Movement Controls")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⏮ Previous Move", use_container_width=True):
        st.session_state.step = max(0, st.session_state.step - 1)
        st.rerun()

with col2:
    if st.button("Next Move ⏭", use_container_width=True):
        st.session_state.step = min(
            len(st.session_state.moves),
            st.session_state.step + 1
        )
        st.rerun()

with col3:
    if st.button("▶ Play Animation", use_container_width=True):
        for current_step in range(
            st.session_state.step + 1,
            len(st.session_state.moves) + 1
        ):
            st.session_state.step = current_step
            show_current_state()
            time.sleep(speed)
        st.rerun()

with col4:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.step = 0
        st.rerun()

st.divider()

st.header("📘 Rules of Tower of Hanoi")

st.markdown("""
1. Only one disk can be moved at a time.
2. Only the top disk of a rod can be moved.
3. A larger disk cannot be placed on a smaller disk.
4. Move all disks from Rod A to Rod C using Rod B.
""")

st.header("🧠 Algorithm")

st.code("""
1. If there is one disk, move it to the destination.
2. Move n-1 disks from source to auxiliary.
3. Move the largest disk to destination.
4. Move n-1 disks from auxiliary to destination.
5. Repeat until all disks reach the destination.
""", language="text")

st.success(
    f"Minimum moves for {disk_count} disks: "
    f"2^{disk_count} - 1 = {minimum_moves}"
)

st.markdown("---")
st.caption("Tower of Hanoi Visual Simulator | Python Project")
