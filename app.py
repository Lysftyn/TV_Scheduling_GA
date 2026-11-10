
import streamlit as st
import pandas as pd
import random
from pathlib import Path
from collections import Counter

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Genetic Algorithm",
    layout="wide"
)

st.header("Genetic Algorithm", divider="gray")

# ==========================================
# 2. CUSTOM CSS - MINIMAL LIGHT THEME
# ==========================================

st.markdown("""
<style>
    .stApp {
        background-color: #F7F9FC;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #243B53;
    }

    .description {
        color: #64748B;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .section-title {
        color: #243B53;
        font-size: 21px;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    .info-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .card-label {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 7px;
    }

    .card-value {
        color: #243B53;
        font-size: 27px;
        font-weight: 700;
    }

    .stButton > button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
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
        raise ValueError("The CSV file does not contain valid program ratings.")

    program_column = df.columns[0]

    ratings = {}

    for _, row in df.iterrows():

        program = str(row[program_column]).strip()

        ratings[program] = {}

        for column in df.columns[1:]:

            hour = int(str(column).replace("Hour", "").strip())

            ratings[program][hour] = float(row[column])

    return ratings


# Check CSV file

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
# 11. WEBSITE HEADER
# ==========================================

st.markdown("""
<div class="description">
    An intelligent TV program scheduling system using
    Genetic Algorithm to find an optimal broadcasting schedule
    based on program ratings.
</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================
# 12. SIDEBAR - PARAMETER SETTINGS
# ==========================================

st.sidebar.title("GA Settings")

st.sidebar.markdown(
    "Adjust the Genetic Algorithm parameters below."
)

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

st.sidebar.markdown("**Algorithm Configuration**")

st.sidebar.write(f"Generations: {GEN}")
st.sidebar.write(f"Population Size: {POP}")
st.sidebar.write(f"Elitism Size: {EL_S}")

st.sidebar.caption(
    "Adjust the parameters and click Generate Schedule "
    "to obtain a new schedule."
)


# ==========================================
# 13. PROGRAM INFORMATION
# ==========================================

st.markdown(
    '<div class="section-title">System Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-label">Total Programs</div>
            <div class="card-value">{len(all_programs)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-label">Available Time Slots</div>
            <div class="card-value">{len(all_time_slots)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="info-card">
            <div class="card-label">Scheduling Method</div>
            <div class="card-value" style="font-size:21px;">
                Genetic Algorithm
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# 14. GENERATE SCHEDULE BUTTON
# ==========================================

st.markdown(
    '<div class="section-title">Generate TV Schedule</div>',
    unsafe_allow_html=True
)

st.write(
    "Click the button below to generate an optimized "
    "TV program schedule using the selected parameters."
)

if st.button("Generate Schedule"):

    with st.spinner("Generating the optimal schedule..."):

        random.seed()

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

    st.divider()

    st.markdown(
        '<div class="section-title">Scheduling Results</div>',
        unsafe_allow_html=True
    )

    # Result metrics

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Ratings",
            f"{total_rating:.2f}"
        )

    with col2:

        st.metric(
            "Total Programs",
            len(set(final_schedule))
        )

    with col3:

        st.metric(
            "Time Slots",
            len(final_schedule)
        )

    # Display used parameters

    st.caption(
        f"Parameters used: CO_R = {used_co_r:.2f} "
        f"| MUT_R = {used_mut_r:.2f}"
    )

    # Schedule table

    st.markdown(
        '<div class="section-title">Final TV Program Schedule</div>',
        unsafe_allow_html=True
    )

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

    st.dataframe(
        schedule_df,
        use_container_width=True,
        hide_index=True
    )

    # Program frequency

    st.markdown(
        '<div class="section-title">Program Frequency</div>',
        unsafe_allow_html=True
    )

    frequency = Counter(final_schedule)

    frequency_df = pd.DataFrame({
        "Program": all_programs,
        "Frequency": [
            frequency[program]
            for program in all_programs
        ]
    })

    col1, col2 = st.columns([1, 1.5])

    with col1:

        st.dataframe(
            frequency_df,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        st.bar_chart(
            frequency_df.set_index("Program"),
            y="Frequency"
        )

    # Schedule validation

    st.markdown(
        '<div class="section-title">Schedule Validation</div>',
        unsafe_allow_html=True
    )

    all_programs_included = (
        set(final_schedule) == set(all_programs)
    )

    correct_time_slots = (
        len(final_schedule) == len(all_time_slots)
    )

    col1, col2 = st.columns(2)

    with col1:

        if all_programs_included:

            st.success(
                "All programs are included in the schedule."
            )

        else:

            st.error(
                "Some programs are missing from the schedule."
            )

    with col2:

        if correct_time_slots:

            st.success(
                "All time slots have been assigned."
            )

        else:

            st.error(
                "The number of time slots is incorrect."
            )

    # Download schedule

    csv_data = schedule_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Schedule as CSV",
        data=csv_data,
        file_name="final_tv_schedule.csv",
        mime="text/csv"
    )

else:

    st.info(
        "No schedule has been generated yet. "
        "Adjust the GA parameters and click "
        "'Generate Schedule' to view the results."
    )


# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#94A3B8;
                font-size:13px; padding:10px;">
        TV Program Scheduling System | Genetic Algorithm
    </div>
    """,
    unsafe_allow_html=True
)
