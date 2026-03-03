from flask import Flask, render_template, request

app = Flask(__name__)

# -----------------------------
# Sample Bus Network (Prototype)
# -----------------------------
# Graph: Node -> Connected Node -> Time (in minutes)

graph = {
    "Tambaram": {"Guindy": 25, "Velachery": 30},
    "Guindy": {"Tambaram": 25, "T Nagar": 15, "Velachery": 20},
    "Velachery": {"Tambaram": 30, "Guindy": 20, "Adyar": 15},
    "T Nagar": {"Guindy": 15, "Anna Nagar": 25},
    "Adyar": {"Velachery": 15, "Anna Nagar": 30},
    "Anna Nagar": {"T Nagar": 25, "Adyar": 30}
}

# -----------------------------
# Traffic Multipliers
# -----------------------------
traffic_multiplier = {
    "normal": 1.0,
    "moderate": 1.3,
    "heavy": 1.6
}

# -----------------------------
# Dijkstra Algorithm
# -----------------------------
def dijkstra(graph, start, end, traffic_level):
    unvisited = list(graph.keys())
    distances = {node: float('inf') for node in graph}
    previous = {}
    
    distances[start] = 0

    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current)

        if distances[current] == float('inf'):
            break

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

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]
        traffic = request.form["traffic"]

        path, total_time = dijkstra(graph, source, destination, traffic)

        result = {
            "path": " → ".join(path),
            "time": total_time
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
