from flask import Flask, render_template, request

app = Flask(__name__)

# ===============================
# Graph (MUST be global)
# ===============================
graph = {
    "Tambaram": {"Guindy": 25, "Velachery": 30},
    "Guindy": {"Tambaram": 25, "T Nagar": 15, "Velachery": 20},
    "Velachery": {"Tambaram": 30, "Guindy": 20, "Adyar": 15},
    "T Nagar": {"Guindy": 15, "Anna Nagar": 25},
    "Adyar": {"Velachery": 15, "Anna Nagar": 30},
    "Anna Nagar": {"T Nagar": 25, "Adyar": 30}
}

# ===============================
# Coordinates (MUST be global)
# ===============================
coordinates = {
    "Tambaram": [12.9249, 80.1000],
    "Guindy": [13.0067, 80.2206],
    "Velachery": [12.9815, 80.2180],
    "T Nagar": [13.0418, 80.2337],
    "Adyar": [13.0012, 80.2565],
    "Anna Nagar": [13.0850, 80.2101]
}

traffic_multiplier = {
    "normal": 1.0,
    "moderate": 1.3,
    "heavy": 1.6
}

# ===============================
# Dijkstra Algorithm
# ===============================
def dijkstra(graph, start, end, traffic_level):
    unvisited = list(graph.keys())
    distances = {node: float('inf') for node in graph}
    previous = {}

    distances[start] = 0

    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current)

        for neighbor, time in graph[current].items():
            adjusted_time = time * traffic_multiplier[traffic_level]
            new_distance = distances[current] + adjusted_time

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current

    path = []
    current = end

    while current in previous:
        path.insert(0, current)
        current = previous[current]

    path.insert(0, start)

    return path, round(distances[end], 2)

# ===============================
# Route
# ===============================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]
        traffic = request.form["traffic"]

        if source == destination:
            result = {"path": source, "time": 0}
        else:
            path, total_time = dijkstra(graph, source, destination, traffic)
            result = {
                "path": " → ".join(path),
                "time": total_time
            }

    return render_template("index.html", result=result, coordinates=coordinates)

# ===============================
# Production Run
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
