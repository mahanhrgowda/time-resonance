import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz

# Title
st.title("Birth Date and Time Matcher with Triple Helix and Block Universe Theory")

# Input Section
st.header("Enter Birth Details")
col1, col2 = st.columns(2)

with col1:
    date1 = st.date_input("First Person's Birth Date", value=datetime(1993, 7, 12).date())
    time1 = st.time_input("First Person's Birth Time", value=datetime.strptime("12:26 PM", "%I:%M %p").time())
    tz1 = st.selectbox("First Person's Time Zone", pytz.all_timezones, index=pytz.all_timezones.index("Asia/Kolkata"))

with col2:
    date2 = st.date_input("Second Person's Birth Date", value=datetime(1993, 1, 1).date())
    time2 = st.time_input("Second Person's Birth Time", value=datetime.strptime("12:00 AM", "%I:%M %p").time())
    tz2 = st.selectbox("Second Person's Time Zone", pytz.all_timezones, index=pytz.all_timezones.index("UTC"))

# Convert to UTC
def to_utc(date, time, tz_name):
    tz = pytz.timezone(tz_name)
    dt = datetime.combine(date, time).replace(tzinfo=tz)
    return dt.astimezone(pytz.UTC)

dt1_utc = to_utc(date1, time1, tz1)
dt2_utc = to_utc(date2, time2, tz2)

# Reference date for seconds calculation (Jan 1, 1900, 00:00:00 UTC)
ref_date = datetime(1900, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
seconds1 = (dt1_utc - ref_date).total_seconds()
seconds2 = (dt2_utc - ref_date).total_seconds()

# Scale factor for Z-axis (adjust for precision, originally 7.44 years/Z, now seconds)
scale_factor = 7.44 * 365.25 * 24 * 3600  # Years to seconds, approx 234,436,800 seconds/Z
z1 = seconds1 / scale_factor
z2 = seconds2 / scale_factor

st.write(f"First Person's Z-value: {z1:.2f} (Seconds scaled)")
st.write(f"Second Person's Z-value: {z2:.2f} (Seconds scaled)")

# Calculate qualities and resonance
def get_dominant_energy(z):
    # Simplified: Based on phase, determine dominant energy (Śrī, Bhū, Nīlā)
    phase = np.sin(0.5 * z)  # Using helical phase
    if phase > 0.33: return "Śrī (Prosperity)"
    elif phase > -0.33: return "Bhū (Material)"
    else: return "Nīlā (Compassion)"

quality1 = get_dominant_energy(z1)
quality2 = get_dominant_energy(z2)

# Time resonance: Difference in seconds, normalized
time_diff = abs(seconds1 - seconds2) / (365.25 * 24 * 3600)  # Days difference
resonance_score = max(0, 1 - time_diff / 365.25)  # Score 0-1, 1 being same day

# Harmony: 3D distance in helical space, simplified
def get_helical_position(z):
    x = 0.5 * np.sin(0.5 * z)
    y = 0.25 * np.cos(0.5 * z)
    return x, y, z

x1, y1, _ = get_helical_position(z1)
x2, y2, _ = get_helical_position(z2)
spatial_dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
harmony_score = max(0, 1 - spatial_dist / 2)  # Score 0-1, normalized

st.header("Matching Results")
st.write(f"First Person's Dominant Quality: {quality1}")
st.write(f"Second Person's Dominant Quality: {quality2}")
st.write(f"Time Resonance Score (0-1, 1=high): {resonance_score:.2f} (Days apart: {time_diff:.2f})")
st.write(f"Harmony Score (0-1, 1=high): {harmony_score:.2f} (3D Distance: {spatial_dist:.2f})")

# 3D Plot using Plotly for interactivity
st.subheader("3D Helical Plot with Birth Positions")

# Generate helical paths
Z = np.linspace(-5000, 2100, 1000)  # Extended range for BCE and CE
phi = [0, 2*np.pi/3, 4*np.pi/3]  # Phase shifts for Śrī, Bhū, Nīlā
data = []
for i, color in enumerate(['yellow', 'orange', 'red']):
    X = 0.5 * np.sin(0.000001 * Z + phi[i])  # Small frequency for large range
    Y = 0.25 * np.cos(0.000001 * Z + phi[i])
    trace = go.Scatter3d(x=X, y=Y, z=Z, mode='lines', name=f'Devi {i+1}', line=dict(color=color))
    data.append(trace)

# Add birth markers
birth_markers = [
    go.Scatter3d(x=[0], y=[0], z=[z1], mode='markers+text', name='First Person',
                 marker=dict(symbol='circle', size=10, color='blue'),
                 text=[f'Birth 1: {dt1_utc.strftime("%Y-%m-%d %H:%M UTC")}'], textposition="top center"),
    go.Scatter3d(x=[0], y=[0], z=[z2], mode='markers+text', name='Second Person',
                 marker=dict(symbol='circle', size=10, color='green'),
                 text=[f'Birth 2: {dt2_utc.strftime("%Y-%m-%d %H:%M UTC")}'], textposition="top center")
]

data.extend(birth_markers)

fig = go.Figure(data=data)
fig.update_layout(scene=dict(xaxis_title='Time Strand (-1 to 1)',
                             yaxis_title='Cosmic Flow (-1 to -0.25)',
                             zaxis_title='Years Elapsed (Scaled)'),
                  title='Triple Helix Model with Birth Positions')
st.plotly_chart(fig)

# 2D Timeline Plot using Matplotlib
st.subheader("Timeline Plot with Birth Positions")

fig, ax = plt.subplots(figsize=(10, 6))
years1 = dt1_utc.year
years2 = dt2_utc.year
ax.plot([years1, years2], [0, 0], 'bo-', label='Births')
ax.plot(years1, 0, 'bo', label='First Person')
ax.plot(years2, 0, 'go', label='Second Person')
ax.text(years1, 0.1, f'Birth 1: {dt1_utc.strftime("%Y-%m-%d %H:%M UTC")}', rotation=45, fontsize=8)
ax.text(years2, 0.1, f'Birth 2: {dt2_utc.strftime("%Y-%m-%d %H:%M UTC")}', rotation=45, fontsize=8)
ax.set_xlabel('Year (CE)')
ax.set_ylabel('Convergence Level')
ax.set_title('Timeline of Birth Positions')
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Yantra Representation
st.subheader("Spiritual Yantra Representation")
st.write(f"The yantra, with a blue flame at the apex and Sanskrit text 'ॐ श्रीं भूं नीलां अग्निनाभिं प्रबोधय स्वाहा', symbolizes the spiritual convergence at both births. Imagine a triangular design with nodes for Śrī, Bhū, and Nīlā Devī, set against a starry background, highlighting their cosmic alignment at {dt1_utc.strftime('%Y-%m-%d %H:%M UTC')} and {dt2_utc.strftime('%Y-%m-%d %H:%M UTC')}, reflecting their qualities and harmony.")