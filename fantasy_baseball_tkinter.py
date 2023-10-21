import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def hitteraverage(csvfile, p_h_option, player):
    if p_h_option == "Hitter":
        with open(csvfile, 'r') as file:
            reader = csv.DictReader(file)

            player_stats = {}
            for row in reader:
                player_name = row["\ufeffPlayer"]
                player_stats[player_name] = row
        if player in player_stats:
            stats = player_stats[player]
            hits = int(player_stats[player]['H'])
            runs = int(player_stats[player]["R"])
            walks = int(player_stats[player]["BB"])
            strikeouts = int(player_stats[player]["SO"])
            games = int(player_stats[player]["G"])
            doubles = int(player_stats[player]["2B"])
            triples = int(player_stats[player]["3B"])
            homeruns = int(player_stats[player]["HR"])
            rbi = int(player_stats[player]["RBI"])
            stolenbases = int(player_stats[player]["SB"])
            hitbypitch = int(player_stats[player]["HBP"])
            singles = hits - (doubles + triples + homeruns)

            # Fantasy values
            fdoubles = doubles * 2
            ftriples = triples * 4
            fhomeruns = homeruns * 5
            fstrikeouts = strikeouts * -0.75

            avg = round(
                (
                        (
                                fdoubles
                                + singles
                                + fhomeruns
                                + fstrikeouts
                                + stolenbases
                                + hitbypitch
                                + rbi
                                + runs
                                + walks
                                + ftriples
                        )
                        / games
                ),
                2,
            )

            # Format the stats neatly
            stats_str = f"Hits: {hits} "
            stats_str += f"Average: {avg} "
            stats_str += f"Runs: {runs} "
            stats_str += f"Walks: {walks} "
            stats_str += f"Strikeouts: {strikeouts} "
            stats_str += f"Games: {games} "
            stats_str += f"Doubles: {doubles} "
            stats_str += f"Triples: {triples} "
            stats_str += f"Homeruns: {homeruns} "
            stats_str += f"RBI: {rbi} "
            stats_str += f"Stolen Bases: {stolenbases} "
            stats_str += f"Hit by Pitch: {hitbypitch} "

            # Update the return statement
            return [avg, stats_str]

        # Player not found, return None
        return None


def pitcheraverage(csvfile, p_h_option, player):
    if p_h_option == "Pitcher":
        with open(csvfile, 'r') as file:
            reader = csv.DictReader(file)

            player_stats = {}
            for row in reader:
                player_name = row["\ufeffPlayer"]
                player_stats[player_name] = row

        if player in player_stats:
            stats = player_stats[player]
            innings = float(player_stats[player]['IP'])
            earned_runs = int(player_stats[player]["ER"])
            wins = int(player_stats[player]["W"])
            losses = int(player_stats[player]["L"])
            saves = int(player_stats[player]["SV"])
            blown_saves = int(player_stats[player]["BS"])
            strikeouts = int(player_stats[player]["K"])
            hits = int(player_stats[player]["H"])
            walks = int(player_stats[player]["BB"])
            holds = int(player_stats[player]["HLD"])
            games = int(player_stats[player]["G"])

            # Fantasy values
            finnings = innings * 3
            fearned_runs = earned_runs * -2
            fwins = wins * 5
            fblown_saves = blown_saves * -2
            flosses = losses * -3
            fsaves = saves * 5
            fhits = hits * -1
            fwalks = walks * -1
            fholds = holds * 2

            avg = round(
                (
                        (
                                finnings
                                + fearned_runs
                                + fwins
                                + strikeouts
                                + fblown_saves
                                + flosses
                                + fsaves
                                + fhits
                                + fwalks
                                + fholds
                        )
                        / games
                ),
                2,
            )

            # Format the stats neatly
            stats_str = f"Innings: {innings} "
            stats_str += f"Earned Runs: {earned_runs} "
            stats_str += f"Wins: {wins} "
            stats_str += f"Losses: {losses} "
            stats_str += f"Saves: {saves} "
            stats_str += f"Blown Saves: {blown_saves} "
            stats_str += f"Strikeouts: {strikeouts} "
            stats_str += f"Hits: {hits} "
            stats_str += f"Walks: {walks} "
            stats_str += f"Holds: {holds} "
            stats_str += f"Games: {games} "

            # Update the return statement
            return [avg, stats_str]

        # Player not found, return None
        return None


def calculate_average_favg(csvfile):
    with open(csvfile, 'r') as file:
        reader = csv.DictReader(file)
        favg_values = [float(row['favg']) for row in reader]
    avg_favg = np.mean(favg_values)
    return avg_favg


def get_player_stats():
    p_h_option = position_var.get()
    player = player_entry.get()

    try:
        for widget in stats_frame.winfo_children():
            widget.destroy()

        for widget in pie_chart_frame.winfo_children():
            widget.destroy()

        for widget in bar_graph_frame.winfo_children():
            widget.destroy()

        k_percentages = []  # List to store K% values
        bb_percentages = []  # List to store BB% values
        fantasy_averages = []  # List to store fantasy averages
        years = []  # List to store years

        for year in range(2015, 2024):
            csvfile_hitter = f"mlbhitterstats{year}.csv"
            csvfile_pitcher = f"mlbpitcherstats{year}.csv"

            if os.path.isfile(csvfile_hitter):
                hitter_result = hitteraverage(csvfile_hitter, p_h_option, player)
                if hitter_result:
                    avg, stats_str = hitter_result
                    ttk.Label(
                        stats_frame,
                        text=f"{year} Hitter Fantasy Avg: {avg}",
                        style="StatsLabel.TLabel",
                    ).pack()
                    ttk.Label(
                        stats_frame,
                        text=stats_str,
                        style="StatsLabel.TLabel",
                        wraplength= 600,  # Increased wraplength to 600 pixels
                        justify="left",
                    ).pack()

                    # Calculate K% and BB%
                    with open(csvfile_hitter, "r") as file:
                        reader = csv.DictReader(file)
                        player_stats = {}
                        for row in reader:
                            player_name = row["\ufeffPlayer"]
                            player_stats[player_name] = row
                        if player in player_stats:
                            strikeouts = int(player_stats[player]["SO"])
                            at_bats = int(player_stats[player]["AB"])
                            walks = int(player_stats[player]["BB"])
                            k_percentages.append((strikeouts / at_bats) * 100)
                            bb_percentages.append((walks / at_bats) * 100)

                    # Append fantasy average and year to the lists
                    fantasy_averages.append(avg)
                    years.append(year)

            if os.path.isfile(csvfile_pitcher):
                pitcher_result = pitcheraverage(csvfile_pitcher, p_h_option, player)
                if pitcher_result:
                    avg, stats_str = pitcher_result
                    ttk.Label(
                        stats_frame,
                        text=f"{year} Pitcher Fantasy Avg: {avg}",
                        style="StatsLabel.TLabel",
                    ).pack()
                    ttk.Label(
                        stats_frame,
                        text=stats_str,
                        style="StatsLabel.TLabel",
                        wraplength=1500,  # Increased wraplength to 600 pixels
                        justify="left",
                    ).pack()

                    # Calculate K% and BB%
                    with open(csvfile_pitcher, "r") as file:
                        reader = csv.DictReader(file)
                        player_stats = {}
                        for row in reader:
                            player_name = row["\ufeffPlayer"]
                            player_stats[player_name] = row
                        if player in player_stats:
                            strikeouts = int(player_stats[player]["K"])
                            walks = int(player_stats[player]["BB"])
                            innings = float(player_stats[player]["IP"])
                            k_percentages.append(
                                (strikeouts / (strikeouts + walks + (innings * 3))) * 100
                            )
                            bb_percentages.append(
                                (walks / (strikeouts + walks + (innings * 3))) * 100
                            )

                    # Append fantasy average and year to the lists
                    fantasy_averages.append(avg)
                    years.append(year)

        if not stats_frame.winfo_children():
            messagebox.showerror(
                "Error",
                f"Player '{player}' not found in the specified years or CSV files not found.",
            )

        # Calculate the average K% out of all the years together
        if len(k_percentages) > 0:
            average_k_percent = sum(k_percentages) / len(k_percentages)
            ttk.Label(
                stats_frame,
                text=f"Average K%: {average_k_percent:.2f}",
                style="StatsLabel.TLabel",
            ).pack()

            # Create a figure for the K% pie chart
            figure_k = plt.Figure(figsize=(3, 3), dpi=80)
            ax_k = figure_k.add_subplot(111)
            labels_k = ["K%", "Other"]
            sizes_k = [average_k_percent, 100 - average_k_percent]
            ax_k.pie(sizes_k, labels=labels_k, autopct="%1.1f%%", startangle=90)
            ax_k.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

            # Create the canvas to display the K% pie chart
            canvas_k = FigureCanvasTkAgg(figure_k, master=pie_chart_frame)
            canvas_k.draw()
            canvas_k.get_tk_widget().pack()

        # Calculate the average BB% out of all the years together
        if len(bb_percentages) > 0:
            average_bb_percent = sum(bb_percentages) / len(bb_percentages)
            ttk.Label(
                stats_frame,
                text=f"Average BB%: {average_bb_percent:.2f}",
                style="StatsLabel.TLabel",
            ).pack()

            # Create a figure for the BB% pie chart
            figure_bb = plt.Figure(figsize=(3, 3), dpi=80)
            ax_bb = figure_bb.add_subplot(111)
            labels_bb = ["BB%", "Other"]
            sizes_bb = [average_bb_percent, 100 - average_bb_percent]
            ax_bb.pie(sizes_bb, labels=labels_bb, autopct="%1.1f%%", startangle=90)
            ax_bb.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

            # Create the canvas to display the BB% pie chart
            canvas_bb = FigureCanvasTkAgg(figure_bb, master=pie_chart_frame)
            canvas_bb.draw()
            canvas_bb.get_tk_widget().pack()

        # Calculate and display the average favg value
        csvfile_player = f"{player}.csv"
        if os.path.isfile(csvfile_player):
            avg_favg = calculate_average_favg(csvfile_player)
            avg_favg_label = ttk.Label(
                stats_frame,
                text=f"Average favg: {avg_favg}",
                style="StatsLabel.TLabel",
            )
            avg_favg_label.pack()

        # Create the bar graph of fantasy averages
        if fantasy_averages:
            plt.figure(figsize=(8, 4))
            plt.bar(years, fantasy_averages)
            plt.xlabel("Year")
            plt.ylabel("Fantasy Average")
            plt.title("Fantasy Average Over the Years")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Create the canvas to display the bar graph
            canvas = FigureCanvasTkAgg(plt.gcf(), master=bar_graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create the main window
window = tk.Tk()
window.title("Kent's Fantasy CheatCode")
window.configure(bg="black")

# Set styles
style = ttk.Style()
style.configure("StatsLabel.TLabel", background="coral", font=("Arial", 14))

# Create a scrollable frame
canvas = tk.Canvas(window, bg="light salmon")
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create and configure the widgets
title_label = tk.Label(
    scrollable_frame,
    text="Kent's Better Algorithm",
    font=("Havelinca", 20, "bold"),
    bg="coral",
)
title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

player_frame = tk.Frame(scrollable_frame, bg="coral")
player_frame.grid(row=1, column=0, padx=20, pady=20, sticky=tk.NW)

position_label = tk.Label(player_frame, text="Position:", bg="light salmon")
position_label.grid(row=0, column=0, sticky=tk.E)

position_var = tk.StringVar(player_frame)
position_var.set("Hitter")

position_menu = tk.OptionMenu(player_frame, position_var, "Hitter", "Pitcher")
position_menu.grid(row=0, column=1, sticky=tk.W)

player_label = tk.Label(player_frame, text="Player Name:", bg="light salmon")
player_label.grid(row=1, column=0, sticky=tk.E)

player_entry = tk.Entry(player_frame)
player_entry.grid(row=1, column=1, sticky=tk.W)

get_stats_button = tk.Button(
    player_frame,
    text="Get Player Stats",
    command=get_player_stats,
    bg="light green",
    activebackground="lime green",
)
get_stats_button.grid(row=2, columnspan=2, pady=10)

stats_frame = tk.Frame(scrollable_frame, bg="mint cream", padx=10, pady=10)
stats_frame.grid(row=1, column=1, padx=20, pady=20, sticky=tk.NSEW)

# Add a vertical scrollbar to the stats frame to handle potential overflow of content
stats_scrollbar = ttk.Scrollbar(stats_frame)
stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget to display player stats
stats_text = tk.Text(
    stats_frame,
    wrap=tk.WORD,
    font=("Arial", 14),
    bg="light green",
    yscrollcommand=stats_scrollbar.set,
    width=60,  # Adjust the width to make the stats box bigger
)
stats_text.pack(fill=tk.BOTH, expand=True)

# Configure the scrollbar to scroll the stats_text widget
stats_scrollbar.config(command=stats_text.yview)


pie_chart_frame = tk.Frame(scrollable_frame, bg="mint cream")
pie_chart_frame.grid(row=2, column=0, padx=20, pady=20, sticky=tk.NW)

bar_graph_frame = tk.Frame(scrollable_frame, bg="mint cream")
bar_graph_frame.grid(row=2, column=1, padx=20, pady=20, sticky=tk.NW)

# Set row and column weights for dynamic resizing
scrollable_frame.grid_rowconfigure(1, weight=1)
scrollable_frame.grid_columnconfigure(1, weight=1)

# Start the main event loop
window.mainloop()