
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class FlightAnalysisVisuals:
    def __init__(self):
        # Constants and settings for the visuals
        self.initial_altitude = 6400  # in feet
        self.final_altitude = 971  # in feet (at the impact site)
        self.max_descent_rate = 11900  # in feet per minute
        self.max_groundspeed = 228  # in knots
        self.feet_to_miles = 1 / 5280
        self.knots_to_mph = 1.15078

        # Approximate coordinates for visualization purposes
        self.dkx_lat, self.dkx_lon = 35.9639, -83.8749  # DKX
        self.crash_lat, self.crash_lon = 35.2500, -86.8481  # Crash site
        self.suz_lat, self.suz_lon = 34.5906, -92.4794  # SUZ

        # Data for common fatal mistakes made by pilots
        self.mistakes_data = {
            "Mistake": [
                "Pilot Disorientation and Confusion",
                "Inappropriate Passenger Interference",
                "Neglect of Standard Operating Procedures",
                "Failure to Respond to ATC Instructions",
                "Erratic Flight Path with Altitude Oscillations",
                "Rapid and Uncontrolled Descent"
            ],
            "Severity": [5, 4, 6, 3, 2, 1]  # Severity ranking
        }

    def plot_uncontrolled_descent(self):
        # Calculating descent angle
        groundspeed_mph = self.max_groundspeed * self.knots_to_mph
        descent_rate_mph = self.max_descent_rate / 60 * self.feet_to_miles * 60
        descent_angle = np.degrees(np.arctan2(descent_rate_mph, groundspeed_mph))

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot([0, groundspeed_mph], [self.initial_altitude, self.final_altitude], label='Flight Path', color='blue')
        plt.scatter([0], [self.initial_altitude], color='red')  # Starting point
        plt.scatter([groundspeed_mph], [self.final_altitude], color='green')  # Impact point

        plt.title('Side View of the Uncontrolled Descent')
        plt.xlabel('Horizontal Distance (mph)')
        plt.ylabel('Altitude (ft)')
        plt.legend()
        plt.annotate(f'Descent Angle: {descent_angle:.2f}°', 
                     xy=(groundspeed_mph / 2, (self.initial_altitude + self.final_altitude) / 2), 
                     xytext=(groundspeed_mph / 3, (self.initial_altitude + self.final_altitude) / 2 + 1000),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.grid(True)
        plt.show()

    def plot_flight_path(self):
        # Plotting
        plt.figure(figsize=(10, 6))
        plt.scatter([self.dkx_lon, self.suz_lon, self.crash_lon], [self.dkx_lat, self.suz_lat, self.crash_lat], color=['blue', 'green', 'red'])
        plt.text(self.dkx_lon, self.dkx_lat, 'DKX (Start)', verticalalignment='bottom', horizontalalignment='right')
        plt.text(self.suz_lon, self.suz_lat, 'SUZ (Destination)', verticalalignment='bottom', horizontalalignment='right')
        plt.text(self.crash_lon, self.crash_lat, 'Crash Site', verticalalignment='bottom', horizontalalignment='right')
        plt.plot([self.dkx_lon, self.crash_lon], [self.dkx_lat, self.crash_lat], label='Flight Path', color='orange', linestyle='--')
        plt.title('Approximate Flight Path')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_simulated_altitude_path(self):
        time = np.linspace(0, 70, 500)  # 70 minutes from takeoff to crash
        altitude = 6500 - (time**1.5) + 500 * np.sin(time / 4)
        altitude = np.maximum(altitude, 971)
        last_minutes = time > 65
        altitude[last_minutes] = np.linspace(altitude[last_minutes][0], 971, sum(last_minutes))

        plt.figure(figsize=(12, 6))
        plt.plot(time, altitude, label='Simulated Altitude', color='blue')
        plt.scatter(time[-1], altitude[-1], color='red')  # Crash point
        plt.title('Simulated Altitude-Based Flight Path with Oscillations')
        plt.xlabel('Time from Takeoff (Minutes)')
        plt.ylabel('Altitude (Feet)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_fatal_mistakes(self):
        df = pd.DataFrame(self.mistakes_data)
        df.sort_values("Severity", inplace=True)
        plt.figure(figsize=(10, 6))
        plt.barh(df["Mistake"], df["Severity"], color='skyblue')
        plt.xlabel('Severity (1 = Most Severe)')
        plt.title('Common Fatal Mistakes Made by Pilots Ranked by Severity')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
        plt.show()

# Creating an instance of the class
visuals = FlightAnalysisVisuals()

# Generating the visuals
visuals.plot_uncontrolled_descent()
visuals.plot_flight_path()
visuals.plot_simulated_altitude_path()
visuals.plot_fatal_mistakes()
