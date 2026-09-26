from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Indoor map
graph = {
    "Entrance": ["Corridor"],
    "Corridor": ["Entrance", "Room 101", "Room 102"],
    "Room 101": ["Corridor", "Library"],
    "Room 102": ["Corridor"],
    "Library": ["Room 101"]
}
directions = {
    ("Entrance", "Corridor"): "Go straight to the Corridor.",
    ("Corridor", "Room 101"): "Turn left and continue to Room 101.",
    ("Room 101", "Library"): "Go straight. The Library is ahead.",
    ("Corridor", "Room 102"): "Turn right and continue to Room 102.",
    ("Room 101", "Corridor"): "Go back to the Corridor.",
    ("Library", "Room 101"): "Go back toward Room 101.",
    ("Room 102", "Corridor"): "Go back to the Corridor.",
    ("Corridor", "Entrance"): "Continue straight toward the Entrance."
}




# Dijkstra's algorithm
def find_shortest_path(start, destination):

    distances = {location: float("inf") for location in graph}
    previous = {location: None for location in graph}

    distances[start] = 0
    unvisited = list(graph.keys())

    while unvisited:

        current = min(
            unvisited,
            key=lambda location: distances[location]
        )

        unvisited.remove(current)

        if current == destination:
            break

        for neighbour in graph[current]:

            new_distance = distances[current] + 1

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find-route", methods=["POST"])
def find_route():

    data = request.get_json()

    start = data["start"]
    destination = data["destination"]

    route = find_shortest_path(start, destination)

    instructions = []

    for i in range(len(route) - 1):

        current = route[i]
        next_location = route[i + 1]

        instruction = directions.get(
            (current, next_location),
            f"Continue to {next_location}."
        )

        instructions.append(instruction)

    return jsonify({
        "route": route,
        "instructions": instructions
    })

if __name__ == "__main__":
    app.run(debug=True)