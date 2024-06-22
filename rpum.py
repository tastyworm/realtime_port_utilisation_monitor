import streamlit as st
import subprocess
import time
import pandas as pd
from datetime import datetime
import os
import shutil
import sys


timing_interval = 5 

# Make the st page wide
st.set_page_config(layout="wide")

# CSV file setup
csv_file_name = 'port_utilisation_data.csv'
file_exists = os.path.isfile(csv_file_name)

# If the file exists, delete it to ensure the data is fresh
if file_exists:
    os.remove(csv_file_name)

# Function to get port states using netstat
def get_port_states():
    # Execute netstat command and capture the output
    result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
    output = result.stdout

    # Initialize a dictionary to hold the count of each state
    state_counts = {
        'ESTABLISHED': 0,
        'TIME_WAIT': 0,
        'CLOSE_WAIT': 0,
        'LISTENING': 0,
        'SYN_SENT': 0,
        'SYN_RECEIVED': 0,
        'FIN_WAIT_1': 0,
        'FIN_WAIT_2': 0,
        'CLOSED': 0,
        'CLOSING': 0,
        'LAST_ACK': 0,
        'UNKNOWN': 0  
    }

    # Process each line of the netstat output
    for line in output.splitlines():
        # Split the line into parts
        parts = line.split()
        # Check if the line contains a state we are interested in
        if parts and parts[-1] in state_counts:
            # Increment the count for this state
            state_counts[parts[-1]] += 1

    return state_counts



# Initialize a list to store the data temporarily
temp_data = []
bar_temp_data = []

# Streamlit app setup
st.title('Real-time Port Utilization Chart')
chart = st.empty()
bar_chart = st.empty()

# Define the CSV file name
csv_file_name = 'port_utilization_data.csv'

# Run the loop to collect data
start_time = time.time()
while True:
    states = get_port_states()
    nowYMDHMS = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime object
    nowHMS = datetime.now().strftime('%H:%M:%S')  # Format the datetime object
    nowHM = datetime.now().strftime('%H:%M')  # Format the datetime object
    
    temp_data.append({
        'Timestamp': nowHMS,
        'ESTABLISHED': states.get('ESTABLISHED', 0),
        'TIME_WAIT': states.get('TIME_WAIT', 0),
        'CLOSE_WAIT': states.get('CLOSE_WAIT', 0),
        'LISTENING': states.get('LISTENING', 0),
        'SYN_SENT': states.get('SYN_SENT', 0),
        'SYN_RECEIVED': states.get('SYN_RECEIVED', 0),
        'FIN_WAIT_1': states.get('FIN_WAIT_1', 0),
        'FIN_WAIT_2': states.get('FIN_WAIT_2', 0),
        'CLOSED': states.get('CLOSED', 0),
        'CLOSING': states.get('CLOSING', 0),
        'LAST_ACK': states.get('LAST_ACK', 0),
        'UNKNOWN': states.get('UNKNOWN', 0)
    })

    bar_temp_data.append({
        'ESTABLISHED': states.get('ESTABLISHED', 0),
        'TIME_WAIT': states.get('TIME_WAIT', 0),
        'CLOSE_WAIT': states.get('CLOSE_WAIT', 0),
        'LISTENING': states.get('LISTENING', 0),
        'SYN_SENT': states.get('SYN_SENT', 0),
        'SYN_RECEIVED': states.get('SYN_RECEIVED', 0),
        'FIN_WAIT_1': states.get('FIN_WAIT_1', 0),
        'FIN_WAIT_2': states.get('FIN_WAIT_2', 0),
        'CLOSED': states.get('CLOSED', 0),
        'CLOSING': states.get('CLOSING', 0),
        'LAST_ACK': states.get('LAST_ACK', 0),
        'UNKNOWN': states.get('UNKNOWN', 0)
    })
  

    # Update the DataFrame and chart at regular intervals
    if time.time() - start_time > 5:
        # Convert the collected data to a DataFrame
        data = pd.DataFrame(temp_data)
        bar_data = pd.DataFrame(bar_temp_data).T

        # Ensure 'Timestamp' is in datetime format
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%H:%M:%S', errors='coerce')

        # Sort the DataFrame by 'Timestamp' to ensure the x-axis increases with time
        data.sort_values('Timestamp', inplace=True)

        # Set 'Timestamp' as the index
        data.set_index('Timestamp', inplace=True)

        # Update the chart
        chart.line_chart(data)

        # Check if the CSV file exists to determine whether to write the header
        file_exists = os.path.isfile(csv_file_name)

        # Append the new data to the CSV file
        # If the file does not exist, write the header, otherwise skip the header
        data.to_csv(csv_file_name, mode='a', header=not file_exists)

        bar_temp_data.pop()

        # Update the bar chart to show only the most recent row of data
        bar_chart.bar_chart(bar_data[1])
        
    time.sleep(timing_interval)