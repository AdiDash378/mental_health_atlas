"""Mental Health Atlas - college Python mini-project.

Run with:  python app.py   then open http://localhost:8000
Uses only: pandas, numpy, matplotlib and Python's built-in http.server.
"""
import os
import html
from urllib.parse import urlparse, parse_qs, urlencode
from http.server import BaseHTTPRequestHandler, HTTPServer

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # draw charts into files, no window needed
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 1. Folders and constants
# ---------------------------------------------------------------
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_FOLDER, "data")
CHART_FOLDER = os.path.join(BASE_FOLDER, "charts")
STATIC_FOLDER = os.path.join(BASE_FOLDER, "static")
TEMPLATE_FILE = os.path.join(BASE_FOLDER, "templates", "layout.html")

CONDITIONS = ["Depressive disorders", "Anxiety disorders", "Bipolar disorder",
              "Schizophrenia", "Eating disorders"]
GREEN, SAGE, ACCENT, CHARCOAL = "#2f5d46", "#a9b8a0", "#b5683a", "#2b2d2a"
LINE_COLORS = [GREEN, ACCENT, "#7d9a78", CHARCOAL, "#d4a373"]

# key, file name, title, description (what each CSV contains)
DATASETS = [
    ("prevalence", "1_prevalence.csv", "Prevalence of mental illnesses",
     "Share of population with each of five disorders, by country and year (1990-2019)."),
    ("burden", "2_burden_dalys.csv", "Disease burden (DALYs)",
     "Years of healthy life lost per 100,000 people for each disorder, by country and year."),
    ("coverage_dep", "3_coverage_depression.csv", "Data coverage: major depression",
     "Percentage of adults in each world region covered by primary data on major depression (2008)."),
    ("coverage_all", "4_coverage_all.csv", "Data coverage: all disorders",
     "Same idea as file 3, but for six disorders (2008)."),
    ("treatment", "5_treatment_gap.csv", "Anxiety treatment gap",
     "Share of people with anxiety disorders who got adequate, other, or no treatment."),
    ("symptoms", "6_symptoms_us.csv", "Depressive symptoms in the US",
     "How often US adults reported each depressive symptom (2014)."),
    ("countries_data", "7_countries_with_data.csv", "Countries with primary data",
     "Number of countries with primary prevalence data for each disorder (2019)."),
]


# ---------------------------------------------------------------
# 2. Loading and cleaning the CSV files
# ---------------------------------------------------------------
def load_all_data():
    """Read every CSV file into a dictionary of DataFrames."""
    all_data = {}
    for key, file_name, title, description in DATASETS:
        path = os.path.join(DATA_FOLDER, file_name)
        all_data[key] = pd.read_csv(path)

    # Files 1 and 2 have very long column names, so we shorten them.
    all_data["prevalence"] = all_data["prevalence"].rename(columns={
        all_data["prevalence"].columns[3]: "Schizophrenia",
        all_data["prevalence"].columns[4]: "Depressive disorders",
        all_data["prevalence"].columns[5]: "Anxiety disorders",
        all_data["prevalence"].columns[6]: "Bipolar disorder",
        all_data["prevalence"].columns[7]: "Eating disorders"})
    all_data["burden"] = all_data["burden"].rename(columns={
        all_data["burden"].columns[3]: "Depressive disorders",
        all_data["burden"].columns[4]: "Schizophrenia",
        all_data["burden"].columns[5]: "Bipolar disorder",
        all_data["burden"].columns[6]: "Eating disorders",
        all_data["burden"].columns[7]: "Anxiety disorders"})

    # The Schizophrenia column in file 4 is read as text, so convert it to numbers.
    all_data["coverage_all"]["Schizophrenia"] = pd.to_numeric(
        all_data["coverage_all"]["Schizophrenia"], errors="coerce")
    return all_data


def only_countries(table):
    """Keep rows of real countries (they have a country code).
    Regions such as 'World' have a code starting with OWID or no code."""
    rows = table[table["Code"].notna()]
    rows = rows[~rows["Code"].astype(str).str.startswith("OWID")]
    return rows


DATA = load_all_data()
COUNTRY_PREV = only_countries(DATA["prevalence"])
COUNTRY_BURDEN = only_countries(DATA["burden"])
COUNTRY_NAMES = sorted(COUNTRY_PREV["Entity"].unique())


# ---------------------------------------------------------------
# 3. Chart helpers (Matplotlib)
# ---------------------------------------------------------------
def start_chart(width=8, height=4.2):
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor("#faf6ee")
    ax.set_facecolor("#faf6ee")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#e1dccf", linewidth=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def finish_chart(fig, file_name, title):
    fig.suptitle(title, x=0.01, ha="left", fontsize=12, color=GREEN, family="serif")
    fig.tight_layout()
    path = os.path.join(CHART_FOLDER, file_name)
    fig.savefig(path, dpi=110, facecolor=fig.get_facecolor())
    plt.close(fig)
    return file_name


def chart_trend_lines():
    """Average prevalence of each condition across countries, per year."""
    yearly = COUNTRY_PREV.groupby("Year")[CONDITIONS].mean()
    fig, ax = start_chart()
    for i in range(len(CONDITIONS)):
        ax.plot(yearly.index, yearly[CONDITIONS[i]], label=CONDITIONS[i],
                color=LINE_COLORS[i], linewidth=2)
    ax.set_ylabel("% of population")
    ax.legend(frameon=False, fontsize=8)
    return finish_chart(fig, "trend_lines.png", "Average prevalence across countries, 1990-2019")


def chart_change_bars():
    """Percentage change in average prevalence between first and last year."""
    yearly = COUNTRY_PREV.groupby("Year")[CONDITIONS].mean()
    first = yearly.iloc[0]
    last = yearly.iloc[-1]
    change = (last - first) / first * 100
    fig, ax = start_chart()
    bar_colors = []
    for value in change:
        if value >= 0:
            bar_colors.append(ACCENT)
        else:
            bar_colors.append(GREEN)
    ax.bar(CONDITIONS, change, color=bar_colors)
    ax.axhline(0, color=CHARCOAL, linewidth=0.8)
    ax.set_ylabel("% change")
    plt.setp(ax.get_xticklabels(), rotation=15, fontsize=8)
    return finish_chart(fig, "change_bars.png", "Change in average prevalence, 1990 to 2019")


def chart_country_lines(countries, condition):
    fig, ax = start_chart()
    for i in range(len(countries)):
        rows = COUNTRY_PREV[COUNTRY_PREV["Entity"] == countries[i]]
        ax.plot(rows["Year"], rows[condition], label=countries[i],
                color=LINE_COLORS[i], linewidth=2)
    ax.set_ylabel("% of population")
    ax.legend(frameon=False)
    name = "cl_" + "_".join(countries).replace(" ", "") + "_" + condition.replace(" ", "") + ".png"
    return finish_chart(fig, name, condition + ": prevalence over time")


def chart_country_burden(countries):
    """Grouped bars: 2019 DALY rate of each condition for the chosen countries."""
    fig, ax = start_chart(9, 4.4)
    positions = np.arange(len(CONDITIONS))
    bar_width = 0.8 / len(countries)
    for i in range(len(countries)):
        rows = COUNTRY_BURDEN[(COUNTRY_BURDEN["Entity"] == countries[i]) & (COUNTRY_BURDEN["Year"] == 2019)]
        values = rows[CONDITIONS].values[0]
        ax.bar(positions + i * bar_width, values, bar_width, label=countries[i], color=LINE_COLORS[i])
    ax.set_xticks(positions + bar_width * (len(countries) - 1) / 2)
    ax.set_xticklabels(CONDITIONS, fontsize=8)
    ax.set_ylabel("DALYs per 100,000")
    ax.legend(frameon=False)
    name = "cb_" + "_".join(countries).replace(" ", "") + ".png"
    return finish_chart(fig, name, "Disease burden by condition, 2019")


def chart_condition_bars(table, title, ylabel, file_name):
    """Horizontal bars of the 2019 average of each condition."""
    latest = table[table["Year"] == 2019]
    averages = latest[CONDITIONS].mean().sort_values()
    fig, ax = start_chart(8, 3.4)
    ax.barh(averages.index, averages.values, color=GREEN)
    ax.grid(axis="x", color="#e1dccf")
    ax.grid(axis="y", visible=False)
    ax.set_xlabel(ylabel)
    return finish_chart(fig, file_name, title)


def chart_top_countries(condition):
    latest = COUNTRY_PREV[COUNTRY_PREV["Year"] == 2019]
    top = latest.sort_values(condition, ascending=False).head(10)
    top = top.iloc[::-1]
    fig, ax = start_chart(8, 4)
    ax.barh(top["Entity"], top[condition], color=ACCENT)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("% of population")
    name = "top_" + condition.replace(" ", "") + ".png"
    return finish_chart(fig, name, "Ten highest countries: " + condition + " (2019)")


def chart_stacked(table, columns, colors, title, file_name):
    """Horizontal stacked bars, one bar per row (used for files 5 and 6)."""
    fig, ax = start_chart(9, 0.45 * len(table) + 1.8)
    left = np.zeros(len(table))
    for i in range(len(columns)):
        values = table[columns[i]].values
        ax.barh(table["Entity"], values, left=left, color=colors[i], label=columns[i].replace(", conditional", ""))
        left = left + values
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("% of people")
    ax.legend(frameon=False, fontsize=8, ncol=len(columns), loc="upper center", bbox_to_anchor=(0.5, -0.18))
    return finish_chart(fig, file_name, title)


def chart_countries_with_data():
    table = DATA["countries_data"].sort_values("Number of countries with primary data on prevalence of mental disorders")
    fig, ax = start_chart(8, 4.8)
    ax.barh(table["Entity"], table.iloc[:, 3], color=SAGE)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Number of countries with primary data")
    return finish_chart(fig, "countries_with_data.png", "Where is the data actually measured? (2019)")


# ---------------------------------------------------------------
# 4. HTML helpers
# ---------------------------------------------------------------
def esc(value):
    return html.escape(str(value))


def show_number(value):
    """Format floats nicely, leave other values as text."""
    if isinstance(value, (float, np.floating)):
        if pd.isna(value):
            return ""
        return "{:.2f}".format(value)
    return esc(value)


def table_html(table):
    out = '<div class="tablewrap"><table><tr>'
    for column in table.columns:
        out += "<th>" + esc(column) + "</th>"
    out += "</tr>"
    for index in range(len(table)):
        out += "<tr>"
        for value in table.iloc[index]:
            out += "<td>" + show_number(value) + "</td>"
        out += "</tr>"
    out += "</table></div>"
    return out


def select_html(name, label, options, selected):
    out = '<div><label>' + label + '</label><select name="' + name + '">'
    for option in options:
        mark = ""
        if str(option) == str(selected):
            mark = " selected"
        out += '<option value="' + esc(option) + '"' + mark + ">" + esc(option) + "</option>"
    return out + "</select></div>"


def figure_html(file_name, caption):
    return ('<figure><img src="/charts/' + file_name + '" alt="' + esc(caption) +
            '"><figcaption>' + esc(caption) + "</figcaption></figure>")


def stat_html(number, label):
    return '<div class="stat"><b>' + esc(number) + "</b><span>" + esc(label) + "</span></div>"


NAV_ITEMS = [("/", "Home"), ("/explore", "Dataset Explorer"), ("/trends", "Trends"),
             ("/countries", "Countries"), ("/conditions", "Conditions"), ("/about", "About")]


def build_page(title, current_path, content):
    """Put the page content inside templates/layout.html."""
    with open(TEMPLATE_FILE, encoding="utf-8") as file:
        layout = file.read()
    nav = ""
    for path, name in NAV_ITEMS:
        css = ""
        if path == current_path:
            css = ' class="active"'
        nav += '<a href="' + path + '"' + css + ">" + name + "</a>"
    layout = layout.replace("{{title}}", title)
    layout = layout.replace("{{nav}}", nav)
    return layout.replace("{{content}}", content)


# ---------------------------------------------------------------
# 5. Pages
# ---------------------------------------------------------------
def home_page(params):
    total_rows = 0
    for key in DATA:
        total_rows = total_rows + len(DATA[key])
    latest = COUNTRY_PREV[COUNTRY_PREV["Year"] == 2019]
    avg_dep = latest["Depressive disorders"].mean()
    avg_anx = latest["Anxiety disorders"].mean()
    top_anx = latest.sort_values("Anxiety disorders", ascending=False).iloc[0]
    years = COUNTRY_PREV["Year"]

    content = '<p class="kicker">Data analysis project</p>'
    content += "<h1>Mental Health Atlas: Exploring Mental Health Through Data</h1>"
    content += ('<p class="lead">How common are depression, anxiety and other mental disorders around the world, '
                "how have they changed since 1990, and how much of the picture do we actually measure? "
                "This site answers these questions using seven CSV files from the Kaggle Mental Health dataset.</p>")
    content += '<a class="button" href="/explore">Explore the data</a>'
    content += '<div class="stats">'
    content += stat_html(len(DATA), "CSV files analysed")
    content += stat_html("{:,}".format(total_rows), "rows of data in total")
    content += stat_html(len(COUNTRY_NAMES), "countries in the prevalence file")
    content += stat_html(str(years.min()) + "-" + str(years.max()), "years covered")
    content += "</div>"
    content += "<h2>A few numbers from 2019</h2><div class=\"stats\">"
    content += stat_html("{:.2f}%".format(avg_dep), "average depressive disorder prevalence across countries")
    content += stat_html("{:.2f}%".format(avg_anx), "average anxiety disorder prevalence across countries")
    content += stat_html(top_anx["Entity"], "highest anxiety prevalence ({:.2f}%)".format(top_anx["Anxiety disorders"]))
    content += "</div>"
    content += "<h2>What you can explore</h2><div class=\"grid\">"
    content += '<div><h3><a href="/explore">Dataset Explorer</a></h3><p>Browse, search and filter every row of all seven files.</p></div>'
    content += '<div><h3><a href="/trends">Trends</a></h3><p>How average prevalence changed between 1990 and 2019.</p></div>'
    content += '<div><h3><a href="/countries">Countries</a></h3><p>Pick up to three countries and compare them.</p></div>'
    content += '<div><h3><a href="/conditions">Conditions</a></h3><p>Compare disorders, find the highest countries, see the treatment gap.</p></div>'
    content += "</div>"
    content += '<h2>About the dataset</h2><p>The files come from Our World in Data, using estimates of the Global Burden of Disease study. Two files are large country-by-year tables; the other five are small tables about data coverage, treatment and symptoms. See the <a href="/about">About page</a> for details and limitations.</p>'
    return build_page("Home", "/", content)


def explore_page(params):
    keys = []
    for item in DATASETS:
        keys.append(item[0])
    chosen_key = params.get("d", "prevalence")
    if chosen_key not in keys:
        chosen_key = "prevalence"
    table = DATA[chosen_key]
    search = params.get("q", "").strip()
    entity = params.get("entity", "All")
    year = params.get("year", "All")
    page_number = int(params.get("page", "1")) if params.get("page", "1").isdigit() else 1

    # Filters
    if entity != "All":
        table = table[table["Entity"] == entity]
    if year != "All":
        table = table[table["Year"] == int(year)]
    if search != "":
        keep = pd.Series(False, index=table.index)
        for column in table.columns:
            found = table[column].astype(str).str.contains(search, case=False, regex=False)
            keep = keep | found
        table = table[keep]

    rows_per_page = 20
    total_pages = max(1, int(np.ceil(len(table) / rows_per_page)))
    page_number = min(max(page_number, 1), total_pages)
    shown = table.iloc[(page_number - 1) * rows_per_page: page_number * rows_per_page]

    content = "<h1>Dataset Explorer</h1>"
    content += "<p>All seven CSV files, exactly as loaded by Python. Choose a file, then search or filter.</p>"
    content += "<h2>The files</h2>" + files_table()
    # Form
    dataset_options = []
    for item in DATASETS:
        dataset_options.append(item[0])
    entity_options = ["All"] + sorted(DATA[chosen_key]["Entity"].unique())
    year_options = ["All"] + sorted(DATA[chosen_key]["Year"].unique())
    content += '<form class="filters" method="get" action="/explore">'
    content += select_html("d", "Dataset", dataset_options, chosen_key)
    content += select_html("entity", "Entity", entity_options, entity)
    content += select_html("year", "Year", year_options, year)
    content += '<div><label>Search any text</label><input type="text" name="q" value="' + esc(search) + '"></div>'
    content += '<button class="button" type="submit">Apply</button></form>'
    content += "<p><b>" + str(len(table)) + "</b> rows match. Page " + str(page_number) + " of " + str(total_pages) + ".</p>"
    content += table_html(shown)
    base_query = {"d": chosen_key, "entity": entity, "year": year, "q": search}
    content += '<p class="pager">'
    if page_number > 1:
        content += '<a href="/explore?' + urlencode(dict(base_query, page=page_number - 1)) + '">&larr; Previous</a>'
    if page_number < total_pages:
        content += '<a href="/explore?' + urlencode(dict(base_query, page=page_number + 1)) + '">Next &rarr;</a>'
    content += "</p>"
    return build_page("Dataset Explorer", "/explore", content)


def files_table():
    """A summary table: one row per CSV file."""
    summary = []
    for key, file_name, title, description in DATASETS:
        table = DATA[key]
        summary.append({"Key": key, "Title": title, "Description": description,
                        "Rows": len(table), "Columns": len(table.columns)})
    return table_html(pd.DataFrame(summary))


def trends_page(params):
    yearly = COUNTRY_PREV.groupby("Year")[CONDITIONS].mean()
    first_year, last_year = yearly.index[0], yearly.index[-1]

    # Find the condition with the biggest percentage change
    biggest_name = ""
    biggest_change = 0
    for condition in CONDITIONS:
        change = (yearly[condition].iloc[-1] - yearly[condition].iloc[0]) / yearly[condition].iloc[0] * 100
        if abs(change) >= abs(biggest_change):
            biggest_name = condition
            biggest_change = change

    selected_years = [1990, 2000, 2010, 2019]
    snapshot = yearly.loc[selected_years].round(3).reset_index()

    content = "<h1>Mental Health Trends</h1>"
    content += "<p>Source: file 1. We average each country's value for every year, so each country counts equally.</p>"
    content += figure_html(chart_trend_lines(), "Depressive and anxiety disorders are far more common than the other three conditions.")
    content += "<h2>How much did each condition change?</h2>"
    content += figure_html(chart_change_bars(), "Percentage change in the cross-country average, " + str(first_year) + " to " + str(last_year) + ".")
    content += '<div class="note"><b>Observation.</b> The largest change is for ' + biggest_name.lower() + ": {:+.1f}% between ".format(biggest_change) + str(first_year) + " and " + str(last_year) + ". Most averages move slowly because these values are age-standardised.</div>"
    content += "<h2>Yearly averages (% of population)</h2>" + table_html(snapshot)
    return build_page("Trends", "/trends", content)


def countries_page(params):
    defaults = ["India", "United States", "Japan"]
    chosen = []
    for i in range(3):
        name = params.get("c" + str(i + 1), defaults[i])
        if name not in COUNTRY_NAMES:
            name = COUNTRY_NAMES[i]
        if name not in chosen:
            chosen.append(name)
    condition = params.get("condition", "Depressive disorders")
    if condition not in CONDITIONS:
        condition = CONDITIONS[0]

    content = "<h1>Country Comparison</h1>"
    content += "<p>Choose up to three countries (pick the same one twice to compare fewer) and a condition.</p>"
    content += '<form class="filters" method="get" action="/countries">'
    for i in range(3):
        picked = chosen[i] if i < len(chosen) else chosen[0]
        content += select_html("c" + str(i + 1), "Country " + str(i + 1), COUNTRY_NAMES, picked)
    content += select_html("condition", "Condition", CONDITIONS, condition)
    content += '<button class="button" type="submit">Compare</button></form>'
    content += figure_html(chart_country_lines(chosen, condition), "Source: file 1 (prevalence).")

    # 2019 table and observation
    latest = COUNTRY_PREV[(COUNTRY_PREV["Year"] == 2019) & (COUNTRY_PREV["Entity"].isin(chosen))]
    values = latest[condition].values
    highest = latest.sort_values(condition, ascending=False).iloc[0]["Entity"]
    gap = np.max(values) - np.min(values)
    content += '<div class="note"><b>Observation.</b> In 2019, ' + esc(highest) + " had the highest " + condition.lower() + " prevalence of the selected countries. The gap between highest and lowest is {:.2f} percentage points.</div>".format(gap)
    content += "<h2>Prevalence in 2019 (% of population)</h2>"
    content += table_html(latest[["Entity", "Year"] + CONDITIONS])
    content += "<h2>Disease burden</h2>"
    content += figure_html(chart_country_burden(chosen), "Source: file 2. DALYs measure years of healthy life lost.")
    return build_page("Countries", "/countries", content)


def conditions_page(params):
    condition = params.get("condition", "Depressive disorders")
    if condition not in CONDITIONS:
        condition = CONDITIONS[0]

    content = "<h1>Conditions and Disorders</h1>"
    content += "<h2>How common is each condition?</h2>"
    content += figure_html(chart_condition_bars(COUNTRY_PREV, "Average prevalence, 2019", "% of population", "cond_prev.png"), "Source: file 1.")
    content += "<h2>How heavy is the burden?</h2>"
    content += figure_html(chart_condition_bars(COUNTRY_BURDEN, "Average disease burden, 2019", "DALYs per 100,000", "cond_burden.png"), "Source: file 2. Burden takes into account both illness and disability.")
    content += "<h2>Which countries are highest?</h2>"
    content += '<form class="filters" method="get" action="/conditions">'
    content += select_html("condition", "Condition", CONDITIONS, condition)
    content += '<button class="button" type="submit">Show</button></form>'
    content += figure_html(chart_top_countries(condition), "Source: file 1, 2019 values.")
    latest = COUNTRY_PREV[COUNTRY_PREV["Year"] == 2019]
    top = latest.sort_values(condition, ascending=False).head(10)
    content += table_html(top[["Entity", condition]])

    content += "<h2>The anxiety treatment gap</h2>"
    gap_table = DATA["treatment"].sort_values("Untreated, conditional")
    content += figure_html(chart_stacked(
        gap_table, ["Potentially adequate treatment, conditional", "Other treatments, conditional", "Untreated, conditional"],
        [GREEN, SAGE, ACCENT], "Treatment received by people with anxiety disorders", "gap.png"),
        "Source: file 5. Each bar is a country or study area; the year of the survey varies (2002-2017).")
    average_untreated = DATA["treatment"]["Untreated, conditional"].mean()
    content += '<div class="note"><b>Observation.</b> On average {:.1f}% of people with anxiety disorders in these surveys received no treatment.</div>'.format(average_untreated)

    content += "<h2>Depressive symptoms in the US</h2>"
    symptoms = DATA["symptoms"].sort_values("Not at all", ascending=False)
    content += figure_html(chart_stacked(
        symptoms, ["Nearly every day", "More than half the days", "Several days", "Not at all"],
        [ACCENT, "#d4a373", SAGE, "#e6eadc"], "How often US adults reported each symptom", "symptoms.png"),
        "Source: file 6 (2014 survey).")
    return build_page("Conditions", "/conditions", content)


def about_page(params):
    zero_regions = []
    coverage = DATA["coverage_dep"]
    for index in range(len(coverage)):
        if coverage["Major depression"].iloc[index] == 0:
            zero_regions.append(coverage["Entity"].iloc[index])

    content = "<h1>About the Project</h1>"
    content += "<h2>Description</h2><p><b>Mental Health Atlas</b> is a Python mini-project that reads seven CSV files from the Kaggle Mental Health dataset, calculates statistics with Pandas and NumPy, draws charts with Matplotlib, and serves everything as HTML pages through Python's built-in HTTP server.</p>"
    content += "<h2>Objectives</h2><ul><li>Study how common mental disorders are and how this changed from 1990 to 2019.</li><li>Compare countries and conditions using real data.</li><li>Show how much of the world's data is actually measured.</li><li>Apply Python files, functions, loops, NumPy and Matplotlib from our syllabus.</li></ul>"
    content += "<h2>Dataset</h2>" + files_table()
    content += "<p>Files 1 and 2 are the main country-by-year tables. File 3 repeats the major depression column of file 4, so we treat them as coverage tables only and do not combine them.</p>"
    content += "<h2>Python concepts used</h2><ul><li>Variables, data types, operators, if/else, for loops</li><li>User-defined functions (every page and chart is a function)</li><li>File handling (CSV files, the HTML layout file, saving chart images)</li><li>Modules: os, html, urllib, http.server, pandas, numpy, matplotlib</li><li>NumPy: array maths, min/max, ceil, arange</li><li>Matplotlib: line, bar, grouped and stacked charts</li></ul>"
    content += "<h2>Limitations</h2>"
    content += figure_html(chart_countries_with_data(), "Source: file 7. Many values are modelled estimates, not direct measurements.")
    content += "<ul><li>The prevalence and burden values are modelled estimates (Global Burden of Disease), not a census of diagnoses.</li>"
    content += "<li>Regions with no primary data on major depression in 2008: " + esc(", ".join(zero_regions)) + ".</li>"
    content += "<li>Files 5 and 6 are small surveys from different years and places, so they should not be generalised.</li>"
    content += "<li>Differences between countries can reflect diagnosis, stigma and access to care, not only illness.</li></ul>"
    content += '<div class="warn"><b>Disclaimer.</b> This website is for educational data analysis only. It is not intended for medical diagnosis. If you are struggling, please talk to a qualified professional.</div>'
    return build_page("About", "/about", content)


ROUTES = {"/": home_page, "/explore": explore_page, "/trends": trends_page,
          "/countries": countries_page, "/conditions": conditions_page, "/about": about_page}


# ---------------------------------------------------------------
# 6. The HTTP server
# ---------------------------------------------------------------
class AtlasHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        params = {}
        for key in query:
            params[key] = query[key][0]

        if url.path in ROUTES:
            page_function = ROUTES[url.path]
            self.send_bytes(page_function(params).encode("utf-8"), "text/html; charset=utf-8")
        elif url.path.startswith("/static/"):
            self.send_file(os.path.join(STATIC_FOLDER, url.path[len("/static/"):]), STATIC_FOLDER)
        elif url.path.startswith("/charts/"):
            self.send_file(os.path.join(CHART_FOLDER, url.path[len("/charts/"):]), CHART_FOLDER)
        else:
            self.send_bytes(b"<h1>404 - page not found</h1>", "text/html", 404)

    def send_file(self, path, allowed_folder):
        path = os.path.abspath(path)
        if not path.startswith(allowed_folder) or not os.path.isfile(path):
            self.send_bytes(b"Not found", "text/plain", 404)
            return
        if path.endswith(".css"):
            kind = "text/css"
        else:
            kind = "image/png"
        with open(path, "rb") as file:
            self.send_bytes(file.read(), kind)

    def send_bytes(self, content, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main():
    os.makedirs(CHART_FOLDER, exist_ok=True)
    server = HTTPServer(("localhost", 8000), AtlasHandler)
    print("Mental Health Atlas running at http://localhost:8000  (Ctrl+C to stop)")
    server.serve_forever()


if __name__ == "__main__":
    main()
