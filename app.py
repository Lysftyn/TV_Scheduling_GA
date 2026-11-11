
import streamlit as st
import pandas as pd
import random
random.seed(42)

from pathlib import Path
from collections import Counter

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TV Program Scheduling",
    page_icon="📺",
    layout="wide"
)

# ==========================================
# 2. CUSTOM CSS - MODERN DASHBOARD
# ==========================================

st.markdown("""
<style>

/* ---------- GENERAL BACKGROUND ---------- */

.stApp {
    background-color: #F4F7FC;
}

[data-testid="stAppViewContainer"] {
    background-color: #F4F7FC;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ---------- TEXT ---------- */

h1, h2, h3, h4 {
    color: #172554 !important;
    font-weight: 700 !important;
}

p, label, li {
    color: #475569;
}

[data-testid="stMarkdownContainer"] p {
    color: #475569;
}

/* ---------- HERO HEADER ---------- */

.hero {
    background: linear-gradient(120deg, #172554 0%, #1D4ED8 100%);
    padding: 35px 38px;
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(30, 64, 175, 0.15);
}

.hero-label {
    color: #BFDBFE !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-title {
    color: #FFFFFF !important;
    font-size: 34px;
    font-weight: 800;
    margin: 0;
    line-height: 1.25;
}

.hero-description {
    color: #DBEAFE !important;
    font-size: 15px;
    margin-top: 12px;
    max-width: 700px;
    line-height: 1.6;
}

.hero-tag {
    display: inline-block;
    background-color: rgba(255,255,255,0.15);
    color: #FFFFFF !important;
    padding: 7px 13px;
    border-radius: 20px;
    font-size: 12px;
    margin-top: 18px;
}

/* ---------- SECTION HEADINGS ---------- */

.section-heading {
    color: #172554 !important;
    font-size: 21px;
    font-weight: 750;
    margin-top: 18px;
    margin-bottom: 5px;
}

.section-description {
    color: #64748B !important;
    font-size: 13px;
    margin-bottom: 18px;
}

/* ---------- STATISTIC CARDS ---------- */

.stat-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 15px;
    padding: 20px 22px;
    min-height: 115px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
}

.stat-label {
    color: #64748B !important;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}

.stat-value {
    color: #172554 !important;
    font-size: 29px;
    font-weight: 800;
}

.stat-note {
    color: #94A3B8 !important;
    font-size: 11px;
    margin-top: 5px;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172554 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #475569 !important;
}

/* ---------- BUTTONS ---------- */

.stButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid #2563EB !important;
    border-radius: 10px !important;
    min-height: 45px;
    font-weight: 700 !important;
}

.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background-color: #1D4ED8 !important;
    border-color: #1D4ED8 !important;
    color: #FFFFFF !important;
}

/* ---------- DOWNLOAD BUTTON ---------- */

[data-testid="stDownloadButton"] button {
    background-color: #172554 !important;
    color: #FFFFFF !important;
    border: 1px solid #172554 !important;
    border-radius: 10px !important;
    min-height: 45px;
    font-weight: 700 !important;
}

[data-testid="stDownloadButton"] button:hover {
    background-color: #1E40AF !important;
    color: #FFFFFF !important;
}

[data-testid="stDownloadButton"] button p,
[data-testid="stDownloadButton"] button span {
    color: #FFFFFF !important;
}

/* ---------- DATA TABLE ---------- */

[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
}

/* ---------- METRICS ---------- */

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 13px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
}

[data-testid="stMetricValue"] {
    color: #172554 !important;
}

/* ---------- TABS ---------- */

button[data-baseweb="tab"] {
    color: #64748B !important;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563EB !important;
}

/* ---------- STATUS CARDS ---------- */

.status-success {
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    border-radius: 12px;
    padding: 16px;
    color: #065F46 !important;
    font-weight: 650;
    margin-bottom: 10px;
}

.status-failure {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 12px;
    padding: 16px;
    color: #991B1B !important;
    font-weight: 650;
    margin-bottom: 10px;
}

.status-info {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 12px;
    padding: 18px;
    color: #1E40AF !important;
    font-weight: 700;
    margin-top: 12px;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #94A3B8 !important;
    font-size: 12px;
    padding: 20px 5px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD MODIFIED CSV FILE
# ==========================================

DATA_FILE = Path(__file__).parent / "program_ratings_modified.csv"


@st.cache_data
def load_ratings(file_path):

    df = pd.read_csv(file_path)

    if df.empty or len(df.columns) < 2:
        raise ValueError(
            "The CSV file does not contain valid program ratings."
        )

    program_column = df.columns[0]
    ratings = {}

    for _, row in df.iterrows():

        program = str(row[program_column]).strip()
        ratings[program] = {}

        for column in df.columns[1:]:

            hour = int(
                str(column).replace("Hour", "").strip()
            )

            ratings[program][hour] = float(row[column])

    return ratings


if not DATA_FILE.exists():

    st.error(
        "CSV file not found. Please make sure "
        "program_ratings_modified.csv is in the same repository "
        "as app.py."
    )

    st.stop()


try:

    ratings = load_ratings(str(DATA_FILE))

except Exception as error:

    st.error(f"Unable to load CSV file: {error}")
    st.stop()


all_programs = list(ratings.keys())
all_time_slots = sorted(ratings[all_programs[0]].keys())


# ==========================================
# 4. GENETIC ALGORITHM PARAMETERS
# ==========================================

GEN = 100
POP = 50
EL_S = 2


# ==========================================
# 5. FITNESS FUNCTION
# ==========================================

def fitness_function(schedule):

    total_rating = 0

    for index, program in enumerate(schedule):

        hour = all_time_slots[index]

        total_rating += ratings[program][hour]

    return total_rating


# ==========================================
# 6. CREATE INITIAL SCHEDULE
# ==========================================

def create_initial_schedule():

    schedule = all_programs.copy()

    while len(schedule) < len(all_time_slots):

        schedule.append(random.choice(all_programs))

    random.shuffle(schedule)

    return schedule


# ==========================================
# 7. REPAIR SCHEDULE
# ==========================================

def repair_schedule(schedule):

    schedule = schedule[:len(all_time_slots)]

    while len(schedule) < len(all_time_slots):

        schedule.append(random.choice(all_programs))

    counts = Counter(schedule)

    missing_programs = [
        program for program in all_programs
        if counts[program] == 0
    ]

    for missing_program in missing_programs:

        replaceable_positions = [
            index for index, program in enumerate(schedule)
            if counts[program] > 1
        ]

        if replaceable_positions:

            position = random.choice(replaceable_positions)
            old_program = schedule[position]

            schedule[position] = missing_program

            counts[old_program] -= 1
            counts[missing_program] += 1

    return schedule


# ==========================================
# 8. CROSSOVER
# ==========================================

def crossover(schedule1, schedule2, crossover_rate):

    child1 = schedule1.copy()
    child2 = schedule2.copy()

    if random.random() < crossover_rate:

        point = random.randint(1, len(schedule1) - 1)

        child1 = schedule1[:point] + schedule2[point:]
        child2 = schedule2[:point] + schedule1[point:]

    child1 = repair_schedule(child1)
    child2 = repair_schedule(child2)

    return child1, child2


# ==========================================
# 9. MUTATION
# ==========================================

def mutate(schedule, mutation_rate):

    schedule = schedule.copy()

    for index in range(len(schedule)):

        if random.random() < mutation_rate:

            another_position = random.randint(
                0, len(schedule) - 1
            )

            schedule[index], schedule[another_position] = (
                schedule[another_position],
                schedule[index]
            )

    return repair_schedule(schedule)


# ==========================================
# 10. GENETIC ALGORITHM
# ==========================================

def genetic_algorithm(crossover_rate, mutation_rate):

    population = [
        create_initial_schedule()
        for _ in range(POP)
    ]

    for generation in range(GEN):

        population = sorted(
            population,
            key=fitness_function,
            reverse=True
        )

        new_population = population[:EL_S]

        while len(new_population) < POP:

            parent1 = random.choice(population[:POP // 2])
            parent2 = random.choice(population[:POP // 2])

            child1, child2 = crossover(
                parent1,
                parent2,
                crossover_rate
            )

            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.append(child1)

            if len(new_population) < POP:
                new_population.append(child2)

        population = new_population

    best_schedule = max(
        population,
        key=fitness_function
    )

    return best_schedule

# ==========================================
# 11. HERO HEADER
# ==========================================

st.markdown(
    "<h1 style='color: blue;'>TV Program Scheduling</h1>",
    unsafe_allow_html=True
)

# ==========================================
# 12. SIDEBAR - GA SETTINGS
# ==========================================

st.sidebar.markdown("## ⚙️ GA Settings")

st.sidebar.caption(
    "Configure the parameters before generating your schedule."
)

st.sidebar.divider()

CO_R = st.sidebar.slider(
    "Crossover Rate (CO_R)",
    min_value=0.0,
    max_value=0.95,
    value=0.8,
    step=0.05
)

MUT_R = st.sidebar.slider(
    "Mutation Rate (MUT_R)",
    min_value=0.01,
    max_value=0.05,
    value=0.05,
    step=0.01
)

st.sidebar.divider()

st.sidebar.markdown("### Algorithm Configuration")

st.sidebar.markdown(
    f"""
    **Generations**

    {GEN}

    **Population Size**

    {POP}

    **Elitism Size**

    {EL_S}
    """
)

st.sidebar.divider()

st.sidebar.info(
    "Change the parameter values and click "
    "Generate Schedule to create a new result."
)


# ==========================================
# 13. SYSTEM OVERVIEW
# ==========================================

st.markdown(
    '<div class="section-heading">System Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'A quick overview of the scheduling dataset and algorithm.'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">📺 TOTAL PROGRAMS</div>
            <div class="stat-value">{len(all_programs)}</div>
            <div class="stat-note">Available TV programmes</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">🕒 TIME SLOTS</div>
            <div class="stat-value">{len(all_time_slots)}</div>
            <div class="stat-note">Available broadcasting hours</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">🧬 OPTIMIZATION METHOD</div>
            <div class="stat-value" style="font-size:23px;">
                Genetic Algorithm
            </div>
            <div class="stat-note">Evolutionary computing technique</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 14. GENERATE SCHEDULE
# ==========================================

st.markdown(
    '<div class="section-heading">Generate Your Schedule</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Run the Genetic Algorithm using your selected parameters.'
    '</div>',
    unsafe_allow_html=True
)

generate_col, info_col = st.columns([1, 2])

with generate_col:

    generate_clicked = st.button(
        "🚀 Generate Schedule",
        type="primary",
        use_container_width=True
    )

with info_col:

    st.caption(
        "The algorithm will evaluate different programme "
        "combinations and return the best schedule found."
    )


if generate_clicked:

    with st.spinner(
        "Running Genetic Algorithm... Please wait."
    ):

        random.seed(42)

        final_schedule = genetic_algorithm(
            crossover_rate=CO_R,
            mutation_rate=MUT_R
        )

        total_rating = fitness_function(final_schedule)

        st.session_state["final_schedule"] = final_schedule
        st.session_state["total_rating"] = total_rating
        st.session_state["used_co_r"] = CO_R
        st.session_state["used_mut_r"] = MUT_R


# ==========================================
# 15. DISPLAY RESULTS
# ==========================================

if "final_schedule" in st.session_state:

    final_schedule = st.session_state["final_schedule"]
    total_rating = st.session_state["total_rating"]

    used_co_r = st.session_state["used_co_r"]
    used_mut_r = st.session_state["used_mut_r"]

    frequency = Counter(final_schedule)

    all_programs_included = (
        set(final_schedule) == set(all_programs)
    )

    correct_time_slots = (
        len(final_schedule) == len(all_time_slots)
    )

    st.divider()

    st.markdown(
        '<div class="section-heading">📊 Scheduling Results</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'The results generated by the Genetic Algorithm.'
        '</div>',
        unsafe_allow_html=True
    )

    # RESULT METRICS

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Ratings",
            f"{total_rating:.2f}"
        )

    with col2:

        st.metric(
            "Programs Included",
            f"{len(set(final_schedule))}/{len(all_programs)}"
        )

    with col3:

        st.metric(
            "Time Slots Assigned",
            f"{len(final_schedule)}/{len(all_time_slots)}"
        )

    st.caption(
        f"Parameters used: CO_R = {used_co_r:.2f} "
        f"| MUT_R = {used_mut_r:.2f}"
    )

    # PREPARE SCHEDULE DATA

    schedule_data = []

    for index, program in enumerate(final_schedule):

        hour = all_time_slots[index]

        schedule_data.append({
            "Time Slot": f"{hour:02d}:00 - {hour + 1:02d}:00",
            "TV Program": program,
            "Program Rating": round(
                ratings[program][hour], 2
            )
        })

    schedule_df = pd.DataFrame(schedule_data)

    # PREPARE FREQUENCY DATA

    frequency_df = pd.DataFrame({
        "Program": all_programs,
        "Frequency": [
            frequency[program]
            for program in all_programs
        ]
    })

    # RESULT TABS

    tab1, tab2, tab3 = st.tabs([
        "📅 TV Schedule",
        "📈 Analytics",
        "✅ Validation"
    ])

    # --------------------------------------
    # TAB 1: SCHEDULE
    # --------------------------------------

    with tab1:

        st.markdown(
            '<div class="section-heading">'
            'Final TV Program Schedule</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'The assigned programme for each broadcasting time slot.'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            schedule_df,
            use_container_width=True,
            hide_index=True,
            height=620
        )

        csv_data = schedule_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Schedule as CSV",
            data=csv_data,
            file_name="final_tv_schedule.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )

    # --------------------------------------
    # TAB 2: ANALYTICS
    # --------------------------------------

    with tab2:

        st.markdown(
            '<div class="section-heading">'
            'Program Frequency Analysis</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Shows how many times each programme appears in the schedule.'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1.5])

        with col1:

            st.markdown("#### Frequency Summary")

            st.dataframe(
                frequency_df,
                use_container_width=True,
                hide_index=True,
                height=420
            )

        with col2:

            st.markdown("#### Programme Distribution")

            st.bar_chart(
                frequency_df.set_index("Program"),
                y="Frequency",
                use_container_width=True
            )

        st.divider()

        st.markdown("#### Program Rating by Time Slot")

        rating_chart_df = schedule_df[
            ["Time Slot", "Program Rating"]
        ].set_index("Time Slot")

        st.bar_chart(
            rating_chart_df,
            use_container_width=True
        )

    # --------------------------------------
    # TAB 3: VALIDATION
    # --------------------------------------

    with tab3:

        st.markdown(
            '<div class="section-heading">'
            'Schedule Validation</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Checks whether the generated schedule satisfies '
            'the scheduling requirements.'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            if all_programs_included:

                st.markdown(
                    """
                    <div class="status-success">
                        ✓ All programs are included.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="status-failure">
                        ✗ Some programs are missing.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col2:

            if correct_time_slots:

                st.markdown(
                    """
                    <div class="status-success">
                        ✓ All time slots are assigned.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="status-failure">
                        ✗ Some time slots are missing.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if all_programs_included and correct_time_slots:

            st.markdown(
                """
                <div class="status-info">
                    ✓ SCHEDULE VALID

                <div style="
                    font-size:13px;
                    font-weight:400;
                    margin-top:6px;">
                    All scheduling requirements are satisfied.
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.error(
                "Schedule Invalid. Please check the scheduling results."
            )

        st.markdown("#### Validation Summary")

        validation_df = pd.DataFrame({
            "Requirement": [
                "All programs are included",
                "All time slots are assigned"
            ],
            "Status": [
                "Passed" if all_programs_included else "Failed",
                "Passed" if correct_time_slots else "Failed"
            ]
        })

        st.dataframe(
            validation_df,
            use_container_width=True,
            hide_index=True
        )


# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div class="footer">
        TV PROGRAM SCHEDULING SYSTEM
        <br>
        Powered by Genetic Algorithm | Evolutionary Computing
    </div>
    """,
    unsafe_allow_html=True
)
