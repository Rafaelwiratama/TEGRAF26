
from collections import defaultdict
from functools import lru_cache
import heapq
import math


# =========================================================
# 1. DATA GRAF
# =========================================================

# Format: (simpul_awal, simpul_tujuan, bobot)
edges = [
    ("u", "x", 1),
    ("u", "y", 4),
    ("u", "w", 5),
    ("x", "y", 2),
    ("x", "z", 3),
    ("x", "v", 6),
    ("y", "z", 2),
    ("y", "w", 1),
    ("z", "w", 2),
    ("z", "v", 3),
    ("w", "v", 2),
]


def chinese_postman(edges):
    if not edges:
        raise ValueError("Graf tidak boleh kosong.")

    if any(weight < 0 for _, _, weight in edges):
        raise ValueError("Bobot sisi harus nonnegatif.")

    # Mengambil semua simpul tanpa duplikasi
    nodes = list(
        dict.fromkeys(
            node
            for u, v, _ in edges
            for node in (u, v)
        )
    )

    # =====================================================
    # 2. MEMBANGUN ADJACENCY LIST
    # =====================================================

    adj = defaultdict(list)

    for eid, (u, v, weight) in enumerate(edges):
        adj[u].append((v, weight, eid))
        adj[v].append((u, weight, eid))

    # =====================================================
    # 3. ALGORITMA DIJKSTRA
    # Mencari lintasan terpendek dari sebuah simpul
    # =====================================================

    def dijkstra(source):
        dist = {node: math.inf for node in nodes}
        parent = {node: None for node in nodes}

        dist[source] = 0
        pq = [(0, source)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current_dist != dist[current]:
                continue

            for neighbor, weight, eid in adj[current]:
                new_dist = current_dist + weight

                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    parent[neighbor] = (current, eid)

                    heapq.heappush(
                        pq, (new_dist, neighbor)
                    )

        return dist, parent

    # Graf harus terhubung
    initial_dist, _ = dijkstra(nodes[0])

    unreachable = [
        node for node in nodes
        if math.isinf(initial_dist[node])
    ]

    if unreachable:
        raise ValueError("Graf harus terhubung.")

    # =====================================================
    # 4. MENCARI SIMPUL BERDERAJAT GANJIL
    # =====================================================

    odd_nodes = [
        node for node in nodes
        if len(adj[node]) % 2 == 1
    ]

    print("Simpul berderajat ganjil:", odd_nodes)

    # =====================================================
    # 5. MENCARI PASANGAN SIMPUL GANJIL DENGAN
    #    TOTAL JARAK MINIMUM
    #
    # Dijkstra menghitung jarak antarsimpul ganjil.
    # Dynamic programming memilih pasangan terbaik.
    # =====================================================

    k = len(odd_nodes)

    shortest_paths = {
        node: dijkstra(node)
        for node in odd_nodes
    }

    distance_matrix = [
        [
            shortest_paths[odd_nodes[i]][0][odd_nodes[j]]
            for j in range(k)
        ]
        for i in range(k)
    ]

    choice = {}

    @lru_cache(maxsize=None)
    def min_matching(mask):
        # Semua simpul sudah dipasangkan
        if mask == 0:
            return 0

        # Ambil simpul ganjil pertama yang belum dipasangkan
        i = (mask & -mask).bit_length() - 1

        remaining = mask ^ (1 << i)
        best_cost = math.inf
        best_partner = None

        # Coba pasangkan dengan setiap simpul yang tersisa
        for j in range(i + 1, k):
            if remaining & (1 << j):
                next_mask = remaining ^ (1 << j)

                cost = (
                    distance_matrix[i][j]
                    + min_matching(next_mask)
                )

                if cost < best_cost:
                    best_cost = cost
                    best_partner = j

        if best_partner is None:
            raise ValueError(
                "Jumlah simpul ganjil tidak valid."
            )

        choice[mask] = best_partner
        return best_cost

    full_mask = (1 << k) - 1
    extra_cost = min_matching(full_mask)

    # =====================================================
    # 6. MENDUPLIKASI LINTASAN TERPENDEK
    #
    # Sisi lintasan terpilih ditambahkan ke graf.
    # Sisi baru tetap memiliki ID yang berbeda meskipun
    # menghubungkan pasangan simpul yang sama.
    # =====================================================

    augmented_edges = list(edges)
    duplicated_paths = []

    mask = full_mask

    while mask:
        i = (mask & -mask).bit_length() - 1
        j = choice[mask]

        source = odd_nodes[i]
        target = odd_nodes[j]

        _, parent = shortest_paths[source]

        current = target
        path_edge_ids = []
        path_nodes = [target]

        # Rekonstruksi lintasan dari target ke source
        while current != source:
            previous, eid = parent[current]

            path_edge_ids.append(eid)
            current = previous
            path_nodes.append(current)

        path_nodes.reverse()

        # Tambahkan salinan setiap sisi pada lintasan
        for eid in reversed(path_edge_ids):
            augmented_edges.append(edges[eid])

        duplicated_paths.append(
            (path_nodes, distance_matrix[i][j])
        )

        # Kedua simpul sudah dipasangkan
        mask ^= (1 << i) | (1 << j)

    # =====================================================
    # 7. MEMBANGUN GRAF HASIL PENAMBAHAN SISI
    # =====================================================

    euler_adj = defaultdict(list)

    for eid, (u, v, weight) in enumerate(augmented_edges):
        euler_adj[u].append(eid)
        euler_adj[v].append(eid)

    # Status setiap sisi:
    # True  = belum dilewati
    # False = sudah dilewati
    active = [True] * len(augmented_edges)

    def other_endpoint(eid, current):
        u, v, _ = augmented_edges[eid]
        return v if current == u else u

    # =====================================================
    # 8. MEMERIKSA JEMBATAN UNTUK ALGORITMA FLEURY
    # =====================================================

    def reachable_count(start, ignored_eid=None):
        visited = {start}
        stack = [start]

        while stack:
            current = stack.pop()

            for eid in euler_adj[current]:
                if not active[eid] or eid == ignored_eid:
                    continue

                neighbor = other_endpoint(eid, current)

                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

        return len(visited)

    def is_bridge(current, eid):
        before = reachable_count(current)
        after = reachable_count(current, eid)

        return after < before

    # =====================================================
    # 9. ALGORITMA FLEURY
    # Membentuk sirkuit Euler pada graf hasil duplikasi
    # =====================================================

    start = nodes[0]
    current = start

    route_nodes = [start]
    route_edges = []
    total_weight = 0

    while any(active):
        candidates = [
            eid for eid in euler_adj[current]
            if active[eid]
        ]

        if not candidates:
            raise RuntimeError(
                "Rute terputus sebelum semua sisi dilewati."
            )

        # Default: gunakan sisi pertama yang tersedia
        chosen = candidates[0]

        # Jika ada pilihan, hindari jembatan
        if len(candidates) > 1:
            for eid in candidates:
                if not is_bridge(current, eid):
                    chosen = eid
                    break

        u, v, weight = augmented_edges[chosen]
        neighbor = v if current == u else u

        # Tandai sisi sebagai sudah dilewati
        active[chosen] = False

        route_edges.append((current, neighbor, weight))
        route_nodes.append(neighbor)

        total_weight += weight
        current = neighbor

    # Pastikan rute kembali ke titik awal
    if current != start:
        raise RuntimeError("Rute bukan sirkuit Euler.")

    # =====================================================
    # 10. MENAMPILKAN HASIL
    # =====================================================

    original_weight = sum(
        weight for _, _, weight in edges
    )

    print("\n=== HASIL CHINESE POSTMAN PROBLEM ===")

    print("\nTotal bobot sisi asli:", original_weight)

    print("\nLintasan yang diduplikasi:")

    if duplicated_paths:
        for path, cost in duplicated_paths:
            print(
                " -> ".join(path),
                f"(bobot {cost})"
            )
    else:
        print("Tidak ada sisi tambahan.")

    print("Total bobot tambahan:", extra_cost)

    print("\nRute optimal:")
    print(" -> ".join(route_nodes))

    print("\nDetail perjalanan:")

    for i, (u, v, weight) in enumerate(route_edges, 1):
        print(
            f"{i:2}. {u} -> {v} "
            f"(bobot {weight})"
        )

    print("\nJumlah perjalanan:", len(route_edges))
    print("Bobot total rute:", total_weight)

    return route_nodes, total_weight


if __name__ == "__main__":
    chinese_postman(edges)
