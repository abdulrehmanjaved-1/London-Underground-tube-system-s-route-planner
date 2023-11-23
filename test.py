import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class RoutePlanner:
    def __init__(self):
        # Initialize the graph to represent the tube system
        self.graph = nx.Graph()

    def add_station(self, station_name):
        # Add a station to the graph
        self.graph.add_node(station_name)

    def add_connection(self, station1, station2, duration):
        # Add a connection between two stations with the specified duration
        self.graph.add_edge(station1, station2, duration=duration)
        self.graph.add_edge(station2, station1, duration=duration)

    def find_route(self, start_station, destination_station):
        try:
            # Use Dijkstra's algorithm to find the shortest path
            shortest_path = nx.shortest_path(self.graph, source=start_station, target=destination_station, weight='duration')
            total_duration = sum(self.graph[shortest_path[i]][shortest_path[i+1]]['duration'] for i in range(len(shortest_path)-1))

            return shortest_path, total_duration
        except nx.NetworkXNoPath:
            raise ValueError("No path found between the specified stations.")
        except nx.NodeNotFound as e:
            raise ValueError(f"Invalid station names: {e}")

    def calculate_journey_times(self):
        # Calculate and store journey times between every station pair
        journey_times = []

        for station1 in self.graph.nodes:
            for station2 in self.graph.nodes:
                if station1 != station2:
                    try:
                        # Use Dijkstra's algorithm to find the shortest path
                        shortest_path = nx.shortest_path(self.graph, source=station1, target=station2, weight='duration')
                        total_duration = sum(self.graph[shortest_path[i]][shortest_path[i+1]]['duration'] for i in range(len(shortest_path)-1))
                        journey_times.append(total_duration)
                    except nx.NetworkXNoPath:
                        # No path found between the specified stations
                        pass

        return journey_times

def load_data_from_excel(file_path, tube_system_route_planner):
    # Load station and connection data from an Excel file
    data = pd.read_excel(file_path)

    # Check the actual column names in your Excel file
    expected_columns = ['Bakerloo', 'Harrow & Wealdstone', 'Unnamed: 2', 'Unnamed: 3']
    if not all(column in data.columns for column in expected_columns):
        raise ValueError("Invalid Excel file structure. Make sure it has the expected columns.")

    for _, row in data.iterrows():
        tube_system_route_planner.add_station(row['Bakerloo'])
        tube_system_route_planner.add_station(row['Harrow & Wealdstone'])
        
        # Check if 'Unnamed: 2' is a numeric value
        if pd.notna(row['Unnamed: 2']) and pd.to_numeric(row['Unnamed: 2'], errors='coerce') == pd.to_numeric(row['Unnamed: 2'], errors='coerce'):
            tube_system_route_planner.add_connection(row['Bakerloo'], row['Harrow & Wealdstone'], float(row['Unnamed: 2']))
            # Add other connections as needed

def take_input():
    # Gather route information from the traveler
    start_station = input("Enter the starting station: ")
    destination_station = input("Enter the destination station: ")
    return start_station, destination_station

def display_route(route, total_duration):
    # Display the detailed list of stations and total duration
    if route:
        print(f"Route: {' -> '.join(route)}")
        print(f"Total duration: {total_duration} minutes")
    else:
        print("No valid route found.")

def plot_histogram(journey_times):
    # Plot a histogram of journey times
    plt.hist(journey_times, bins=20, color='blue', edgecolor='black')
    plt.title('Histogram of Journey Times')
    plt.xlabel('Journey Time (minutes)')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    # Creating an instance of RoutePlanner
    tube_system_route_planner = RoutePlanner()

    # Specify the path to your Excel file (add path to your Excel file)
    excel_file_path = './London Underground data.xlsx'

    # Load data from the Excel file
    load_data_from_excel(excel_file_path, tube_system_route_planner)

    # Gather route information from the traveler
    start_station, destination_station = take_input()

    # Plan the route
try:
    route, total_duration = tube_system_route_planner.find_route(start_station, destination_station)
    print("Route:", route)
    print("Total Duration:", total_duration)
except ValueError as e:
    print(f"Error: {e}")
except nx.NetworkXNoPath:
    print(f"No path found between {start_station} and {destination_station}.")
    # Display the route and total duration
    display_route(route, total_duration)

    # Calculate journey times
    journey_times = tube_system_route_planner.calculate_journey_times()

    # Plot histogram
    plot_histogram(journey_times)
