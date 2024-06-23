# RPUM (Realtime Port Utilisation Monitor) v1.0


**Author:** Simon Cottrill

[https://github.com/tastyworm/realtime_port_utilisation_monitor](https://github.com/tastyworm/realtime_port_utilisation_monitor)

## Change History

| Version | Date       | Author          | Changes                                        |
|---------|------------|-----------------|------------------------------------------------|
| 1.0     | 2024-06-21 | Simon Cottrill  | Initial release                                |

## Description ##

This is a very simple utility built in Python with the Streamlit framework that provides a visualisation of the ```netstat -an``` command on Windows.

### Features ###
- 'time-series' chart displaying the number of ports in different states.
- 'last result' column chart displaying the most recent count for each state
- .CSV dump of the date and associated counts every second.

### Pre-Requisites ###
- Python
- Poetry (installed using ```pip install poetry```)

### Installation ###
1. From the root folder of this repository and type 'poetry update'

### How to start the application ###
1. Start the application by running ```streamlit run rpum.py```
1. A browser window should open, but if it doesn't go to the URL provided after starting rpum.


![RPUM](https://github.com/tastyworm/realtime_port_utilisation_monitor/blob/main/readme_images/rpum_screenshot.png?raw=true)
