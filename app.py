import csv
import random
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Genetic Algorithm"
)

st.header("Genetic Algorithm", divider="gray")

st.title("TV Program Scheduling using Genetic Algorithm")
st.write(
    "Adjust the Genetic Algorithm parameters and generate "
    "a TV program schedule for 18 time slots."
)


# --------------------------------------------------
# Load modified CSV
# --------------------------------------------------
CSV_FILE = Path(__file__).parent / "program_ratings_modified.csv"


def read_csv_to_dict(file_path):
    program_ratings = {}

    with open(file_path, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        for row in reader:
            if not row:
                continue

            program = row[0]
            program_ratings[program] = [float(value) for value in row[1:]]

    return program_ratings


if not CSV_FILE.exists():
    st.error(
        "The file 'program_ratings_modified.csv' was not found. "
        "Please place it in the same folder as app.py."
    )
    st.stop()

ratings = read_csv_to_dict(CSV_FILE)
all_programs = list(ratings.keys())
all_time_slots = list(range(6, 24))


# --------------------------------------------------
# Genetic Algorithm functions
# --------------------------------------------------
GEN = 100
POP = 50
EL_S = 2


def fitness_function(schedule):
    total_rating = 0

    for time_slot, program in enumerate(schedule):
        total_rating += ratings[program][time_slot]

    return total_rating


def create_initial_schedule():
    schedule = all_programs.copy()

    while len(schedule) < len(all_time_slots):
        schedule.append(random.choice(all_programs))

    random.shuffle(schedule)
    return schedule


def repair_schedule(schedule):
    schedule = schedule.copy()

    missing_programs = [
        program for program in all_programs
        if program not in schedule
    ]

    for missing_program in missing_programs:
        counts = {
            program: schedule.count(program)
            for program in all_programs
        }

        replaceable_positions = [
            i for i, program in enumerate(schedule)
            if counts[program] > 1
        ]

        if replaceable_positions:
            position = random.choice(replaceable_positions)
            schedule[position] = missing_program

    return schedule


def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 1)

    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]

    child1 = repair_schedule(child1)
    child2 = repair_schedule(child2)

    return child1, child2


def mutate(schedule):
    schedule = schedule.copy()

    counts = {
        program: schedule.count(program)
        for program in all_programs
    }

    replaceable_positions = [
        i for i, program in enumerate(schedule)
        if counts[program] > 1
    ]

    if replaceable_positions:
        position = random.choice(replaceable_positions)
        schedule[position] = random.choice(all_programs)

    return repair_schedule(schedule)


def genetic_algorithm(
    generations=GEN,
    population_size=POP,
    crossover_rate=0.8,
    mutation_rate=0.05,
    elitism_size=EL_S
):
    population = []

    while len(population) < population_size:
        population.append(create_initial_schedule())

    for _ in range(generations):
        population.sort(key=fitness_function, reverse=True)
        new_population = population[:elitism_size]

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1 = parent1.copy()
                child2 = parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)

            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    population.sort(key=fitness_function, reverse=True)
    return population[0]


# --------------------------------------------------
# Streamlit parameter input
# --------------------------------------------------
st.sidebar.header("Genetic Algorithm Parameters")

crossover_rate = st.sidebar.slider(
    "Crossover Rate (CO_R)",
    min_value=0.0,
    max_value=0.95,
    value=0.8,
    step=0.05
)

mutation_rate = st.sidebar.slider(
    "Mutation Rate (MUT_R)",
    min_value=0.01,
    max_value=0.05,
    value=0.05,
    step=0.01,
    format="%.2f"
)

st.sidebar.write(f"CO_R: **{crossover_rate:.2f}**")
st.sidebar.write(f"MUT_R: **{mutation_rate:.2f}**")

st.caption(
    "Fixed GA settings: GEN = 100, POP = 50, EL_S = 2. "
    "CO_R and MUT_R can be adjusted using the sliders."
)

if st.button("Generate Schedule", type="primary"):
    with st.spinner("Generating the schedule..."):
        final_schedule = genetic_algorithm(
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate
        )

    total_rating = fitness_function(final_schedule)

    schedule_data = []
    for time_slot, program in zip(all_time_slots, final_schedule):
        schedule_data.append(
            {
                "Time Slot": f"{time_slot:02d}:00",
                "Program": program
            }
        )

    schedule_df = pd.DataFrame(schedule_data)

    st.subheader("Generated TV Schedule")
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)

    st.metric("Total Ratings", f"{total_rating:.4f}")

    frequency_data = [
        {
            "Program": program,
            "Frequency": final_schedule.count(program)
        }
        for program in all_programs
    ]

    st.subheader("Program Frequency")
    st.dataframe(
        pd.DataFrame(frequency_data),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Scheduling Constraint Check")
    col1, col2, col3 = st.columns(3)
    col1.metric("Different Programs", len(set(final_schedule)))
    col2.metric("Total Time Slots", len(final_schedule))
    col3.metric(
        "All Programs Included",
        "Yes" if all(program in final_schedule for program in all_programs) else "No"
    )
else:
    st.info(
        "Choose CO_R and MUT_R from the sidebar, then click "
        "'Generate Schedule' to display the schedule."
    )
