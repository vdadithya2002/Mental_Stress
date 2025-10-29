# ...existing code...
import pandas as pd
import folium
import numpy as np

def load_data(aqi_path="hyderabad_air_quality.csv",
              noise_path="hyderabad_noise.csv",
              green_path="hyderabad_green.csv"):
    """Load and return merged dataframe with stress_score and risk_level."""
    aqi = pd.read_csv(aqi_path)
    noise = pd.read_csv(noise_path)
    green = pd.read_csv(green_path)

    df = aqi.merge(noise[["zone", "noise_db"]], on="zone")
    df = df.merge(green[["zone", "ndvi"]], on="zone")

    df["stress_score"] = 0.5 * df["aqi"] + 0.3 * df["noise_db"] - 0.2 * df["ndvi"]

    df["risk_level"] = pd.cut(
        df["stress_score"],
        bins=[-np.inf, 50, 100, np.inf],
        labels=["Low", "Medium", "High"],
    )
    return df

def make_map(df, out_path="hyderabad_stress_zones.html",
             center=(17.3850, 78.4867), zoom_start=11):
    """Create and save a folium map from dataframe with lat/lon, risk_level."""
    m = folium.Map(location=list(center), zoom_start=zoom_start)
    for _, row in df.iterrows():
        color = (
            "green" if row["risk_level"] == "Low" else
            "orange" if row["risk_level"] == "Medium" else "red"
        )
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            fill=True,
            color=color,
            tooltip=f"{row['zone']}: {row['risk_level']} (Score: {row['stress_score']:.1f})"
        ).add_to(m)
    m.save(out_path)
    return m

if __name__ == "__main__":
    df = load_data()
    print(df)
    print(df[["zone", "stress_score", "risk_level"]])
    make_map(df)
# ...existing code...

# ...existing code...
import streamlit as st
from mental_stress import load_data

st.title("Hyderabad Stress Zone Dashboard")

df = load_data()

st.dataframe(df)

if {"lat", "lon"}.issubset(df.columns):
    st.map(df[["lat", "lon"]])
else:
    st.warning("Dataframe missing 'lat'/'lon' columns — map not shown.")
# ...existing code...