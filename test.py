import networkx as nx
import pandas as pd

class TubeSystemRoutePlanner:
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

    def plan_route(self, start_station, destination_station):
        try:
            # Use Dijkstra's algorithm to find the shortest path
            shortest_path = nx.shortest_path(self.graph, source=start_station, target=destination_station, weight='duration')
            total_duration = sum(self.graph[shortest_path[i]][shortest_path[i+1]]['duration'] for i in range(len(shortest_path)-1))

            return shortest_path, total_duration
        except nx.NetworkXNoPath:
            raise ValueError("No path found between the specified stations.")
        except nx.NodeNotFound as e:
            raise ValueError(f"Invalid station names: {e}")

def load_data_from_excel(file_path, tube_system_route_planner):
    # Load station and connection data from an Excel file
    # Modify this function based on your Excel file structure
    data = pd.read_excel(file_path)

    # Print the column names for reference
    print("Column names in the Excel file:", data.columns)

    # Check the actual column names in your Excel file
    expected_columns = ['Bakerloo', 'Harrow & Wealdstone', 'Unnamed: 2', 'Unnamed: 3']
    if not all(column in data.columns for column in expected_columns):
        raise ValueError("Invalid Excel file structure. Make sure it has the expected columns.")

    for _, row in data.iterrows():
        tube_system_route_planner.add_station(row['Bakerloo'])
        tube_system_route_planner.add_station(row['Harrow & Wealdstone'])
        tube_system_route_planner.add_connection(row['Bakerloo'], row['Harrow & Wealdstone'], row['Unnamed: 2'])
        # Add other connections as needed

def gather_user_input():
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

if __name__ == "__main__":
    # Create an instance of TubeSystemRoutePlanner
    tube_system_route_planner = TubeSystemRoutePlanner()

    # Specify the path to your Excel file
    excel_file_path = './London Underground data.xlsx'

    # Load data from the Excel file
    load_data_from_excel(excel_file_path, tube_system_route_planner)

    try:
        # Gather route information from the traveler
        start_station, destination_station = gather_user_input()

        # Plan the route
        route, total_duration = tube_system_route_planner.plan_route(start_station, destination_station)

        # Display the route and total duration
        display_route(route, total_duration)
    except ValueError as e:
        print(f"Error: {e}")
