# 🧭 Smart Travelling Plan – Travel Itinerary Generator

A data-driven Flask web app that generates optimized travel itineraries based on city, duration, and category preferences using a dataset of tourist places. It uses KMeans clustering to group nearby attractions and visualizes routes on interactive maps with Folium.

---

## 🚀 Features

- Recommends top tourist places using real travel dataset (ratings, votes, categories)
- Groups nearby places with KMeans for efficient day-wise planning
- Generates daily itineraries with interactive Folium maps
- Fully responsive UI with dynamic filtering and smooth user flow

---

## 💻 Usage

### 1. Clone the repository
```
git clone https://github.com/AkshithaPerumala/Smart_Travelling_Plan.git
cd Smart_Travelling_Plan
```

### 2. Install required packages
```
pip install flask pandas scikit-learn folium
```

### 3. Run the Flask app
```
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000/
```

---

## ⚙️ How It Works

1. Select a city, preferred categories, number of days, and places per day.
2. The app filters and ranks places based on ratings and votes.
3. KMeans clustering groups nearby attractions for optimized daily travel.
4. The system generates a personalized day-wise itinerary with interactive maps.

---

## 📸 Screenshots

> Enter city name, select categories, specify number of places per day and number of days.

![Travel Itinerary Planner](https://github.com/AkshithaPerumala/Smart_Travelling_Plan/blob/main/s1.png)

> List of suggested places with details and clustered locations.

![Day1 Output](https://github.com/AkshithaPerumala/Smart_Travelling_Plan/blob/main/s2.png)

![Day2 Output](https://github.com/AkshithaPerumala/Smart_Travelling_Plan/blob/main/s3.png)

---

