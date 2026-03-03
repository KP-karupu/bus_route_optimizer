from flask import Flask, render_template, request

app = Flask(__name__)

# -----------------------------
# Sample Bus Network (Prototype)
# -----------------------------
# Graph: Node -> Connected Node -> Time (in minutes)

graph = {
    "A": {"B": 10, "C": 15},
    "B": {"A": 10, "D": 12, "E": 15},
    "C": {"A": 15, "F": 10},
    "D": {"B": 12, "E": 2},
    "E": {"B": 15, "D": 2, "F": 5},
    "F": {"C": 10, "E": 5}
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