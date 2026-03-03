# 🧭 Smart Travelling Plan – Travel Itinerary Generator

A data-driven Flask web app that generates optimized travel itineraries based on city, duration and category preferences using a dataset of tourist places. It uses KMeans clustering to group nearby attractions and visualizes routes on interactive maps with Folium.

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
git clone https://github.com/Apoorva-Satakolla/Smart_Travelling_Plan.git
cd Smart_Travelling_Plan
```
### 2. Run the Flask app
```
python new1.py
```

### 3. How It Works

1. Select a city, preferred categories and number of places per day

2. The app filters and ranks places, then clusters them using KMeans

3. Displays a personalized day-wise plan along with map visualizations



## 📸 Screenshots

> Enter city name, select categories, specify no. of places per day and no. of days.
![Travel Itinerary Planner](https://github.com/Apoorva-Satakolla/Smart_Travelling_Plan/blob/cbd6f90b36abbd2a365e7477203c5da04831ec7a/s1.png)

> List of suggested places with details and location clusters.
![Day1 Output](https://github.com/Apoorva-Satakolla/Smart_Travelling_Plan/blob/cbd6f90b36abbd2a365e7477203c5da04831ec7a/s2.png)
![Day2 Output](https://github.com/Apoorva-Satakolla/Smart_Travelling_Plan/blob/cbd6f90b36abbd2a365e7477203c5da04831ec7a/s3.png)

