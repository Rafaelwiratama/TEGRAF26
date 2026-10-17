from itertools import permutations

# Daftar simpul pada graf
nodes = ["u", "y", "v", "x", "w", "z"]

# Bobot setiap sisi pada graf tak berarah
weights = {
    ("u", "x"): 60,
    ("u", "w"): 56,
    ("u", "v"): 51,
    ("u", "z"): 35,
    ("u", "y"): 2,
    ("x", "w"): 70,
    ("x", "v"): 13,
    ("x", "z"): 68,
    ("x", "y"): 61,
    ("w", "v"): 78,
    ("w", "z"): 21,
    ("w", "y"): 57,
    ("v", "z"): 68,
    ("v", "y"): 51,
    ("z", "y"): 36,
}


# Mengambil bobot sisi tanpa memperhatikan arah
def edge_weight(a, b):
    if (a, b) in weights:
        return weights[(a, b)]

    return weights[(b, a)]


def solve_tsp():
    start = "u"
    other_nodes = [node for node in nodes if node != start]

    best_route = None
    best_cost = float("inf")
    total_routes = 0

    # Mencoba semua permutasi simpul selain titik awal
    for order in permutations(other_nodes):
        route = [start, *order, start]
        total_routes += 1

        # Menghitung total bobot rute
        cost = sum(
            edge_weight(route[i], route[i + 1])
            for i in range(len(route) - 1)
        )

        # Menyimpan rute dengan bobot terkecil
        if cost < best_cost:
            best_cost = cost
            best_route = route

    # Menghitung bobot setiap sisi pada rute optimal
    route_weights = [
        edge_weight(best_route[i], best_route[i + 1])
        for i in range(len(best_route) - 1)
    ]

    print("=== HASIL TSP ===")
    print("Jumlah rute yang diperiksa:", total_routes)
    print("Rute optimal:", " -> ".join(best_route))
    print("Bobot setiap sisi:", route_weights)
    print("Total bobot minimum:", best_cost)


if __name__ == "__main__":
    solve_tsp()