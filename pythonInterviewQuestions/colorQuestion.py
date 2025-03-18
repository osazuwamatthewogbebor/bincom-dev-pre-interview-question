import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
from collections import Counter
import webcolors
import psycopg2


# color names not recognised by matplotlib

custom_colours = {
    "ARSH": (0.7, 0.75, 0.71),
    "CREAM": (1.0, 0.99, 0.82),
    "BLEW": (0, 0, 1.0)
}


def get_html_colour_data():
    # read table data from html file
    table_df = pd.read_html("./python_class_question.html")[0]

    # get the colours in a list

    colours = table_df['COLOURS'].tolist()
    cleaned_colours = []

    for colour_group in colours:
        for colour in colour_group.split(", "):
            cleaned_colours.append(colour)

    return cleaned_colours


def get_colour_rgb():
    # mean, median mode and variance can only be found for numerical data
    # converting colours to RGB values

    rgb_values = np.array([custom_colours[colour] if colour in custom_colours else mcolors.to_rgb(colour) for colour in
                           colour_list])

    reds = rgb_values[:, 0]
    greens = rgb_values[:, 1]
    blues = rgb_values[:, 2]

    return reds, greens, blues


def statistics_calculation():
    # statistics calculation
    red_values, green_values, blue_values = get_colour_rgb()

    mean_rgb = (round(float(np.mean(red_values)), 2), round(float(np.mean(green_values)), 2),
                round(float(np.mean(blue_values)), 2))
    median_rgb = (round(float(np.median(red_values)), 2), round(float(np.median(green_values)), 2),
                  round(float(np.median(blue_values)), 2))
    mode_colour, modal_freq = colour_counts.most_common(1)[0]
    variance_rgb = (round(float(np.var(red_values)), 2), round(float(np.var(green_values)), 2),
                    round(float(np.var(blue_values)), 2))

    mean_colour = get_colour_name(mean_rgb)
    median_colour = get_colour_name(median_rgb)
    variance_colour = get_colour_name(variance_rgb)

    # probability of choosing a red

    probability_red = colour_counts["RED"]/len(colour_counts)

    return mean_colour, median_colour, mode_colour, variance_colour, probability_red


def get_colour_name(colour_rgb):
    try:
        colour_name = webcolors.rgb_to_name(colour_rgb)
        print(f"Colour Name: {colour_name}")
        return colour_name
    except ValueError:
        return f"No Exact match found for rgb {colour_rgb}"


def solution():
    # Solutions to questions

    mean, median, mode, variance, probability = statistics_calculation()
    print(f"1. Mean colour: {mean}")
    print(f"2. Most Worn Colour: {mode}")
    print(f"3. Median colour: {median}")
    print(f"4. Variance colour: {variance}")
    print(f"5. Probability of getting a red: {probability:.2f}")


def create_connection(dict_colour_counts):
    # Connecting to database

    host_name = "localhost"
    db_name = "postgres"
    user = "postgres"
    password = ",.123Favour$"
    port = 5432

    conn = psycopg2.connect(host=host_name, dbname=db_name, user=user, password=password, port=port)

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS colour_data (
        id SERIAL PRIMARY KEY,
        Colour VARCHAR(255),
        Frequency INT
        )
        """)

    for key in dict_colour_counts:
        colour = key
        freq = dict_colour_counts[key]
        cur.execute(f"INSERT INTO colour_data (Colour, Frequency) VALUES ('{colour}', {freq})")

    cur.execute("""SELECT * FROM colour_data""")

    print("6. ")
    for row in cur.fetchall():
        print(row)

    conn.commit()

    cur.close()
    conn.close()

# Main running
colour_list = get_html_colour_data()
colour_counts = Counter(colour_list)
solution()
create_connection(colour_counts)
