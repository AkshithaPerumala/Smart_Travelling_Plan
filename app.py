from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.cluster import KMeans
import folium
import os

app = Flask(__name__)

# ---------------------------------------------------
# Load Dataset (Portable Version - Works on Any PC)
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Placestestf.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

df = pd.read_csv(DATA_PATH, encoding="latin-1")

# ---------------------------------------------------
# Data Cleaning & Preparation
# ---------------------------------------------------
required_columns = [
    "City", "Place_Name", "latitude", "longitude",
    "Ratings", "votes", "Categories", "Place_desc"
]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

df = df.dropna(subset=["latitude", "longitude"])
df["Ratings"] = df["Ratings"].fillna(0)
df["votes"] = df["votes"].fillna(0)


# ---------------------------------------------------
# Score Calculation Logic
# ---------------------------------------------------
def calculate_weight(row):
    if row["Ratings"] > 0 and row["votes"] > 0:
        return (row["Ratings"] + (row["votes"] / 1000)) / 2
    elif row["Ratings"] > 0:
        return row["Ratings"]
    elif row["votes"] > 0:
        return row["votes"] / 1000
    return 0


df["Weight"] = df.apply(calculate_weight, axis=1)

min_weight = df["Weight"].min()
max_weight = df["Weight"].max()

if max_weight != min_weight:
    df["Score"] = 2.5 + (
        (df["Weight"] - min_weight) * (3.5 - 2.5)
        / (max_weight - min_weight)
    )
else:
    df["Score"] = 2.5


# ---------------------------------------------------
# Category Matching Function
# ---------------------------------------------------
def match_categories(categories_string, selected_categories):
    if pd.isna(categories_string):
        return False

    categories_list = categories_string.split(",")
    return any(
        cat.strip().lower() in category.strip().lower()
        for category in categories_list
        for cat in selected_categories
    )


# ---------------------------------------------------
# Recommendation Engine
# ---------------------------------------------------
def recommend_places(city, categories, num_days, places_per_day):
    city_places = df[df["City"] == city].sort_values(
        by=["Score"], ascending=False
    )

    primary_places = city_places[
        city_places["Categories"].apply(
            lambda x: match_categories(str(x), categories)
        )
    ]

    secondary_places = city_places[
        ~city_places["Categories"].apply(
            lambda x: match_categories(str(x), categories)
        )
    ]

    combined_places = pd.concat(
        [primary_places, secondary_places]
    ).drop_duplicates(subset=["Place_Name"])

    if combined_places.empty:
        return [], 0, []

    k = min(len(combined_places), 5)
    kmeans = KMeans(n_clusters=k, random_state=42)
    combined_places["Cluster"] = kmeans.fit_predict(
        combined_places[["latitude", "longitude"]]
    )

    clusters = combined_places.groupby("Cluster")
    itinerary = []
    maps = []
    selected_places = set()

    for day in range(num_days):
        daily_itinerary = []
        day_map = folium.Map(
            location=[
                combined_places["latitude"].mean(),
                combined_places["longitude"].mean(),
            ],
            zoom_start=12,
        )

        for cluster_id, cluster_data in clusters:
            available = cluster_data[
                ~cluster_data["Place_Name"].isin(selected_places)
            ].head(places_per_day)

            for place in available.to_dict("records"):
                folium.Marker(
                    location=[place["latitude"], place["longitude"]],
                    popup=place["Place_Name"],
                    icon=folium.Icon(color="red"),
                ).add_to(day_map)

            daily_itinerary.extend(available.to_dict("records"))
            selected_places.update(available["Place_Name"])

            if len(daily_itinerary) >= places_per_day:
                break

        if daily_itinerary:
            itinerary.append(daily_itinerary[:places_per_day])
            maps.append(day_map)

        combined_places = combined_places[
            ~combined_places["Place_Name"].isin(selected_places)
        ]
        clusters = combined_places.groupby("Cluster")

    return itinerary, len(itinerary), maps


# ---------------------------------------------------
# Routes
# ---------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    available_cities = df["City"].unique()

    if request.method == "POST":
        city = request.form["city"]
        selected_categories = request.form.getlist("categories")
        additional_categories = request.form.getlist("additional_categories")
        places_per_day = int(request.form["places_per_day"])
        num_days = int(request.form["num_days"])

        if additional_categories:
            selected_categories.extend(additional_categories)

        itinerary, available_days, maps = recommend_places(
            city, selected_categories, num_days, places_per_day
        )

        return render_template(
            "index.html",
            available_cities=available_cities,
            itinerary=itinerary,
            available_days=available_days,
            selected_categories=selected_categories,
            maps=maps,
        )

    return render_template("index.html", available_cities=available_cities)


@app.route("/get_categories", methods=["POST"])
def get_categories():
    data = request.get_json()
    city = data["city"]

    available_categories = (
        df[df["City"] == city]["Categories"]
        .dropna()
        .unique()
    )

    available_categories = [
        cat.strip()
        for sublist in available_categories
        for cat in sublist.split(",")
    ]

    return jsonify(list(set(available_categories)))


@app.route("/calculate_max_days", methods=["POST"])
def calculate_max_days():
    data = request.get_json()
    city = data["city"]
    selected_categories = data["selected_categories"]
    places_per_day = data["places_per_day"]

    total_places = df[
        (df["City"] == city)
        & (
            df["Categories"].apply(
                lambda x: match_categories(str(x), selected_categories)
            )
        )
    ].shape[0]

    max_days = -(-total_places // places_per_day)  # Ceiling division

    return jsonify(max_days=max_days)


@app.route("/map/<int:day>")
def show_map(day):
    itinerary, _, maps = recommend_places(
        request.args.get("city"),
        request.args.getlist("categories"),
        int(request.args.get("num_days")),
        int(request.args.get("places_per_day")),
    )

    if 0 < day <= len(maps):
        return render_template(
            "map.html",
            map_html=maps[day - 1].get_root().render(),
        )

    return "Map not available.", 404


# ---------------------------------------------------
# Run App
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)