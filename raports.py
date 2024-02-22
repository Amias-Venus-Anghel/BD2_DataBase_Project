import mysql.connector
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def call_stored_procedure(procedure_name):
    # Initialize connection to None
    connection = None

    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Daria1907<3',
            database='bd2',
            port=3306
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object
            cursor = connection.cursor()

            try:
                # Call the stored procedure
                if procedure_name == "GameSelection":
                    # check if values are valid
                    game_duration = input1_entry.get()
                    player_count = input2_entry.get()
                    if game_duration.isdigit() and player_count.isdigit():
                        cursor.callproc(procedure_name, [game_duration, player_count])
                    else:
                        result_label.config(text="Invalid values")
                        return
                elif procedure_name == "VanzariProducatoriTop":
                    min_rating = input3_entry.get()
                    if min_rating.isdigit():
                        cursor.callproc(procedure_name, [min_rating])
                    else:
                        result_label.config(text="Invalid values")
                        return
                else:
                    cursor.callproc(procedure_name)

                result_label.config(text=f"{procedure_name}")

                fetched_data = []  # collect all resulting data
                for result in cursor.stored_results():
                    dataframe = result.fetchall()
                    fetched_data.extend(dataframe)

                    column_names = [i for i in result.column_names]

                # Convert fetched_data to a DataFrame
                results = pd.DataFrame(fetched_data, columns=column_names)

                plot_data(results, procedure_name)

            except mysql.connector.Error as err:
                print(f"Error calling stored procedure: {err}")

            finally:
                # Close the cursor
                cursor.close()

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

    finally:
        # Close the connection
        if connection:
            connection.close()
            print('Connection closed')


def plot_data(results, procedure_name):

    if procedure_name == "GameSelection":
        game_selection_plot(results)
    elif procedure_name == "VanzariProducatoriTop":
        vanzari_prod_top_plot(results)
    elif procedure_name == "SoloGamesFromProducer":
        solo_games_producer_plot(results)


def solo_games_producer_plot(results):
    # Ensure count is numeric
    results['count'] = pd.to_numeric(results['count'], errors='coerce')

    # Create the main window for plotting
    plot_window = tk.Toplevel()
    plot_window.geometry("1000x600")

    # Create a Figure and Axes for plotting
    fig, ax = plt.subplots(figsize=(8, 8))

    # Get unique producers and assign a color to each
    unique_producers = results['nume'].unique()
    producer_colors = plt.cm.viridis(np.linspace(0, 1, len(unique_producers)))

    # Plot a bar chart with differently colored columns for each producer
    for producer, color in zip(unique_producers, producer_colors):
        producer_data = results[results['nume'] == producer]
        ax.bar(producer_data['nume'], producer_data['count'], label=f"{producer}", color=color)

    # Set labels and title
    ax.set_ylabel('Jocuri Solo')
    ax.set_xlabel('Producatori')
    ax.set_title('Solo Games by Producer')

    # Display legend with color coding
    ax.legend(title="Producer", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax.set_xticks([])

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def vanzari_prod_top_plot(results):
    # Ensure vanzari is numeric
    results['vanzari'] = pd.to_numeric(results['vanzari'], errors='coerce')

    # Create the main window for plotting
    plot_window = tk.Toplevel()
    plot_window.geometry("1000x600")

    # Create a Figure and Axes for plotting
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot a pie chart with only percentage and exemplare_disponibile labels
    wedges, texts, autotexts = ax.pie(
        results['vanzari'],
        labels=results.apply(lambda row: f"{row['vanzari']} vanzari totale", axis=1),
        autopct='%1.1f%%',
        startangle=90
    )

    ax.set_title('Sales of Producers for top genders')

    # Display legend with both gen and producator
    legend_labels = [f"jocuri {row['gen']} de la {row['producator']}" for index, row in
                     results.iterrows()]
    ax.legend(wedges, legend_labels, title="Games", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


def game_selection_plot(results):
    # Ensure exemplare_disponibile is numeric
    results['exemplare_disponibile'] = pd.to_numeric(results['exemplare_disponibile'], errors='coerce')

    # Create the main window for plotting
    plot_window = tk.Toplevel()
    plot_window.geometry("1000x600")

    # Create a Figure and Axes for plotting
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot a pie chart with only percentage and exemplare_disponibile labels
    wedges, texts, autotexts = ax.pie(
        results['exemplare_disponibile'],
        labels=results.apply(lambda row: f"{row['exemplare_disponibile']} available", axis=1),
        autopct='%1.1f%%',
        startangle=90
    )

    ax.set_title('Game selection')

    # Display legend with both nume and producator
    legend_labels = [f"{row['nume']} - {row['producator']}" for index, row in
                     results.iterrows()]
    ax.legend(wedges, legend_labels, title="Games", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("GameStoreDataBase")
    root.geometry("400x400")

    button1 = tk.Button(root, text="GameSelection", command=lambda: call_stored_procedure('GameSelection'))
    button3 = tk.Button(root, text="VanzariProducatoriTop", command=lambda: call_stored_procedure('VanzariProducatoriTop'))
    button2 = tk.Button(root, text="SoloGamesFromProducer", command=lambda: call_stored_procedure('SoloGamesFromProducer'))

    result_label = tk.Label(root, text="Result will be shown in new window.")

    # Add two input fields under the first button
    input1_label = tk.Label(root, text="Maximum Duration")
    input2_label = tk.Label(root, text="Player Count")
    input1_entry = tk.Entry(root)
    input2_entry = tk.Entry(root)

    # Add another input field under the third button
    input3_label = tk.Label(root, text="Minimum Rating")
    input3_entry = tk.Entry(root)

    # Pack buttons and labels
    button1.pack(pady=10)
    input1_label.pack()
    input1_entry.pack()
    input2_label.pack()
    input2_entry.pack()

    button2.pack(pady=10)

    button3.pack(pady=10)
    input3_label.pack()
    input3_entry.pack()

    result_label.pack(pady=10)

    root.mainloop()
