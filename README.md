# Penyelesaian Traveling Salesman Problem (TSP) Menggunakan Python

## 1. Deskripsi Permasalahan

Traveling Salesman Problem (TSP) merupakan permasalahan optimasi dalam teori graf yang bertujuan mencari rute dengan total bobot minimum. Rute tersebut harus mengunjungi setiap simpul tepat satu kali dan kembali ke simpul awal.

Permasalahan ini dapat diterapkan pada berbagai situasi, seperti perencanaan perjalanan, distribusi barang, pengiriman, dan penentuan urutan kunjungan ke beberapa lokasi.

Pada soal ini, graf yang digunakan merupakan graf tak berarah berbobot dengan enam simpul, yaitu `u`, `x`, `w`, `v`, `z`, dan `y`.

Tujuan penyelesaian adalah menentukan rute yang mengunjungi keenam simpul tepat satu kali, kembali ke simpul awal, dan memiliki total bobot minimum.

## 2. Representasi Graf

Graf direpresentasikan menggunakan daftar pasangan simpul beserta bobot sisi yang menghubungkannya.

| Sisi | Bobot |
|---|---:|
| u-x | 60 |
| u-w | 56 |
| u-v | 51 |
| u-z | 35 |
| u-y | 2 |
| x-w | 70 |
| x-v | 13 |
| x-z | 68 |
| x-y | 61 |
| w-v | 78 |
| w-z | 21 |
| w-y | 57 |
| v-z | 68 |
| v-y | 51 |
| z-y | 36 |
| **Jumlah sisi** | **15** |

Graf mempunyai enam simpul dan 15 sisi. Setiap pasangan simpul terhubung oleh sebuah sisi, sehingga graf tersebut merupakan graf lengkap berbobot.

Dalam TSP, suatu rute harus melewati beberapa sisi untuk menghubungkan seluruh simpul sesuai urutan kunjungan. Bobot rute diperoleh dengan menjumlahkan bobot setiap sisi yang dilewati.

Secara matematis, tujuan TSP dapat dinyatakan sebagai berikut:

\[
\min W(T)=\sum_{i=0}^{n-1}w(v_i,v_{i+1})
\]

dengan \(v_n=v_0\), sehingga rute kembali ke simpul awal.

## 3. Algoritma yang Digunakan

### 3.1. Brute Force

Penyelesaian TSP menggunakan algoritma Brute Force dilakukan dengan mencoba seluruh kemungkinan urutan kunjungan simpul, menghitung total bobot setiap rute, dan memilih rute dengan bobot terkecil.

Pada implementasi ini, simpul `u` ditetapkan sebagai titik awal. Penetapan titik awal tersebut tidak mengurangi kemungkinan solusi optimal karena siklus yang sama dapat dimulai dari simpul mana pun.

Lima simpul lainnya kemudian diatur dalam seluruh kemungkinan permutasi.

Jumlah rute yang perlu diperiksa adalah:

\[
\begin{aligned}
N&=(n-1)!\\
&=(6-1)!\\
&=5!\\
&=\boxed{120}
\end{aligned}
\]

Dengan demikian, program memeriksa 120 urutan rute yang dimulai dari `u` dan berakhir kembali di `u`.

### 3.2. Perhitungan Bobot Rute

Setiap rute direpresentasikan sebagai urutan simpul. Program kemudian mengambil bobot setiap sisi yang menghubungkan dua simpul berturutan dan menjumlahkannya.

Sebagai contoh, rute:

\[
u\rightarrow y\rightarrow v\rightarrow x\rightarrow w\rightarrow z\rightarrow u
\]

memiliki bobot sebagai berikut:

| Perjalanan | Bobot |
|---|---:|
| u-y | 2 |
| y-v | 51 |
| v-x | 13 |
| x-w | 70 |
| w-z | 21 |
| z-u | 35 |
| **Total** | **192** |

Perhitungan total bobot:

\[
\begin{aligned}
W(T)&=2+51+13+70+21+35\\
&=\boxed{192}
\end{aligned}
\]

Program membandingkan total bobot ini dengan bobot rute lainnya, kemudian menyimpan rute dengan bobot terkecil sebagai solusi sementara.

Setelah seluruh kemungkinan diperiksa, rute dengan bobot minimum diperoleh.

## 4. Struktur Implementasi Python

Program menggunakan Python 3 dan pustaka standar `itertools` untuk menghasilkan permutasi simpul.

Berikut penjelasan fungsi-fungsi utama pada program.

### 4.1. Menyimpan Data Graf

Data graf disimpan dalam struktur dictionary bernama `weights`. Setiap pasangan simpul menjadi kunci, sedangkan bobot sisi menjadi nilainya.

Contoh:

```python
weights = {
    ("u", "x"): 60,
    ("u", "y"): 2,
    ("w", "z"): 21,
}
```

Struktur tersebut memudahkan program mencari bobot sisi berdasarkan pasangan simpul.

### 4.2. Fungsi `edge_weight()`

Fungsi ini mengambil bobot sisi di antara dua simpul tanpa memperhatikan arah perjalanan.

Jika pasangan simpul tidak ditemukan dalam urutan yang diberikan, program mencari pasangan dalam urutan terbalik.

Hal ini diperlukan karena graf bersifat tak berarah. Sebagai contoh, bobot sisi `u-x` sama dengan bobot sisi `x-u`.

### 4.3. Fungsi `permutations()`

Program menggunakan `permutations()` dari pustaka `itertools` untuk menghasilkan seluruh urutan kunjungan yang mungkin.

```python
other_nodes = [node for node in nodes if node != start]

for order in permutations(other_nodes):
    route = [start, *order, start]
```

Variabel `start` ditetapkan sebagai simpul `u`. Setiap permutasi lima simpul lainnya ditambahkan di antara titik awal dan titik akhir.

Dengan demikian, setiap kandidat rute selalu dimulai dan berakhir di simpul yang sama.

### 4.4. Menghitung Total Bobot

Untuk setiap rute, program menjumlahkan bobot seluruh sisi yang menghubungkan simpul-simpul berurutan.

```python
cost = sum(
    edge_weight(route[i], route[i + 1])
    for i in range(len(route) - 1)
)
```

Hasil perhitungan tersebut kemudian dibandingkan dengan nilai `best_cost`, yaitu bobot minimum yang ditemukan sejauh ini.

### 4.5. Menyimpan Rute Optimal

Apabila bobot rute yang sedang diperiksa lebih kecil daripada nilai minimum sebelumnya, program memperbarui `best_cost` dan `best_route`.

```python
if cost < best_cost:
    best_cost = cost
    best_route = route
```

Proses ini berlangsung hingga seluruh 120 kemungkinan rute selesai diperiksa.

Pada akhir proses, program menampilkan rute optimal, bobot setiap sisi, dan total bobot minimum.

## 5. Cara Menjalankan Program

Simpan kode program Python pada file bernama `tsp_bruteforce.py`.

Pastikan Python 3 telah terpasang. Program tidak memerlukan instalasi paket tambahan karena menggunakan pustaka standar Python.

Jalankan melalui terminal dengan perintah:

```bash
python tsp_bruteforce.py
```

Jika sistem menggunakan perintah `python3`, gunakan:

```bash
python3 tsp_bruteforce.py
```

Program kemudian memeriksa seluruh kemungkinan rute dan menampilkan solusi dengan bobot minimum.

## 6. Hasil dan Analisis

Hasil penyelesaian TSP pada graf tersebut adalah sebagai berikut.

| Komponen | Hasil |
|---|---:|
| Jumlah simpul | 6 |
| Jumlah sisi | 15 |
| Titik awal dan akhir | u |
| Jumlah rute yang diperiksa | 120 |
| Rute optimal | u-y-v-x-w-z-u |
| Bobot minimum | **192** |

Rute optimal yang diperoleh adalah:

\[
u\rightarrow y\rightarrow v\rightarrow x\rightarrow w\rightarrow z\rightarrow u
\]

Dengan total bobot:

\[
2+51+13+70+21+35=\boxed{192}
\]

Rute kebalikannya, yaitu \(u-z-w-x-v-y-u\), juga menghasilkan bobot 192 karena graf tidak berarah. Kedua urutan tersebut merepresentasikan siklus yang sama apabila perbedaan arah perjalanan diabaikan.

Algoritma Brute Force menjamin hasil optimal untuk graf ini karena seluruh kemungkinan urutan rute telah diperiksa.

### Kompleksitas Algoritma

Dengan \(n\) sebagai jumlah simpul, program memeriksa sebanyak \((n-1)!\) rute. Setiap rute memerlukan waktu \(O(n)\) untuk menghitung total bobotnya.

Dengan demikian, kompleksitas waktu keseluruhan adalah:

\[
\boxed{O(n\cdot(n-1)!)}
\]

Karena jumlah permutasi meningkat secara faktorial, Brute Force kurang efisien untuk graf dengan jumlah simpul yang besar. Untuk permasalahan yang lebih besar, metode seperti Held–Karp Dynamic Programming atau Branch and Bound dapat menjadi alternatif.

## 7. Kesimpulan

Permasalahan kedua diselesaikan menggunakan algoritma Brute Force untuk mencari rute optimal pada Traveling Salesman Problem.

Program menetapkan simpul `u` sebagai titik awal, menghasilkan seluruh permutasi lima simpul lainnya, menghitung bobot setiap rute, dan memilih rute dengan total bobot terkecil.

Dari 120 urutan rute yang diperiksa, diperoleh rute optimal \(u-y-v-x-w-z-u\) dengan total bobot:

\[
2+51+13+70+21+35=\boxed{192}
\]

Dengan demikian, total bobot minimum untuk mengunjungi seluruh simpul tepat satu kali dan kembali ke titik awal pada graf tersebut adalah **192**.
