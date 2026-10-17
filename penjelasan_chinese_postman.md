# Penyelesaian Chinese Postman Problem Menggunakan Python

## 1. Deskripsi Permasalahan

Chinese Postman Problem (CPP), yang juga dikenal sebagai *Route Inspection Problem*, merupakan permasalahan optimasi graf untuk mencari rute dengan total bobot minimum yang melewati setiap sisi pada graf setidaknya satu kali dan kembali ke titik awal.

Permasalahan ini dapat diterapkan pada berbagai situasi, seperti pengiriman surat, pengangkutan sampah, pemeriksaan jalan, dan distribusi layanan yang mengharuskan seluruh jalan dilalui.

Pada soal ini, graf yang digunakan merupakan graf tak berarah berbobot dengan enam simpul, yaitu `u`, `x`, `y`, `z`, `w`, dan `v`.

Tujuan penyelesaian adalah menentukan rute tertutup yang melewati seluruh sisi dengan total bobot minimum.

## 2. Representasi Graf

Graf direpresentasikan menggunakan daftar sisi (*edge list*). Setiap sisi disimpan dalam bentuk tiga elemen, yaitu simpul awal, simpul tujuan, dan bobot sisi.

| Sisi | Bobot |
|---|---:|
| u-x | 1 |
| u-y | 4 |
| u-w | 5 |
| x-y | 2 |
| x-z | 3 |
| x-v | 6 |
| y-z | 2 |
| y-w | 1 |
| z-w | 2 |
| z-v | 3 |
| w-v | 2 |
| **Total** | **31** |

Total bobot seluruh sisi asli diperoleh dengan menjumlahkan bobot setiap sisi.

\[
W_{\text{asli}}=\sum_{e\in E}w(e)=31
\]

Apabila graf memiliki sirkuit Euler, setiap sisi dapat dilewati tepat satu kali dan tukang pos dapat kembali ke titik awal. Namun, graf pada soal mempunyai simpul berderajat ganjil sehingga beberapa sisi perlu diulangi.

## 3. Konsep Penyelesaian

Penyelesaian Chinese Postman Problem pada graf tak berarah dilakukan melalui beberapa tahap.

### 3.1. Menghitung Derajat Simpul

Derajat simpul merupakan jumlah sisi yang terhubung dengan simpul tersebut.

| Simpul | Derajat | Keterangan |
|---|---:|---|
| u | 3 | Ganjil |
| x | 4 | Genap |
| y | 4 | Genap |
| z | 4 | Genap |
| w | 4 | Genap |
| v | 3 | Ganjil |

Dari hasil tersebut, terdapat dua simpul berderajat ganjil, yaitu `u` dan `v`.

Agar terbentuk sirkuit Euler, semua simpul harus mempunyai derajat genap. Oleh karena itu, diperlukan penambahan lintasan yang menghubungkan simpul-simpul berderajat ganjil dengan biaya minimum.

### 3.2. Mencari Lintasan Terpendek

Algoritma Dijkstra digunakan untuk mencari lintasan terpendek di antara simpul-simpul berderajat ganjil.

Pada graf ini, lintasan terpendek dari `u` ke `v` adalah:

\[
u\rightarrow x\rightarrow y\rightarrow w\rightarrow v
\]

Bobot lintasan tersebut adalah:

\[
W_{\text{tambahan}}=1+2+1+2=6
\]

Dengan demikian, sisi `u-x`, `x-y`, `y-w`, dan `w-v` perlu diulangi.

### 3.3. Mendapatkan Bobot Minimum

Setelah lintasan terpendek ditambahkan kembali ke graf, semua simpul mempunyai derajat genap. Graf tersebut kemudian dapat digunakan untuk mencari sirkuit Euler.

Bobot minimum rute dihitung sebagai berikut:

\[
\begin{aligned}
W_{\min}
&=W_{\text{asli}}+W_{\text{tambahan}}\\
&=31+6\\
&=\boxed{37}
\end{aligned}
\]

## 4. Algoritma yang Digunakan

Implementasi menggunakan Python 3 dengan kombinasi beberapa algoritma.

### 4.1. Dijkstra

Dijkstra digunakan untuk mencari jarak minimum dari satu simpul ke simpul lainnya. Algoritma ini memanfaatkan *priority queue* agar simpul dengan jarak sementara terkecil diproses terlebih dahulu.

Pada program, Dijkstra juga menyimpan informasi simpul sebelumnya dan identitas sisi yang dilewati agar lintasan terpendek dapat direkonstruksi.

### 4.2. Dynamic Programming dengan Bitmask

Program menggunakan *dynamic programming* dengan bitmask untuk menentukan pasangan simpul berderajat ganjil yang menghasilkan total biaya tambahan minimum.

Untuk setiap pasangan simpul ganjil, jarak yang digunakan berasal dari hasil Dijkstra. Program kemudian membandingkan kemungkinan pasangan-pasangan tersebut sehingga diperoleh pencocokan dengan biaya minimum.

Metode ini membuat program dapat menangani graf yang memiliki lebih dari dua simpul berderajat ganjil, selama jumlahnya masih sesuai untuk pendekatan bitmask.

### 4.3. Duplikasi Sisi

Setelah lintasan tambahan minimum ditemukan, setiap sisi dalam lintasan tersebut ditambahkan kembali ke graf.

Sisi hasil duplikasi diperlakukan sebagai sisi berbeda, walaupun menghubungkan pasangan simpul yang sama dengan sisi asli.

Langkah ini membuat semua simpul berderajat genap sehingga sirkuit Euler dapat dibentuk.

### 4.4. Algoritma Fleury

Algoritma Fleury digunakan untuk menyusun sirkuit Euler pada graf hasil duplikasi.

Algoritma ini memilih sisi yang belum dilewati. Apabila tersedia alternatif, sisi yang merupakan jembatan (*bridge*) dihindari agar graf yang tersisa tetap memungkinkan perjalanan dilanjutkan.

Pemeriksaan jembatan dilakukan dengan membandingkan jumlah simpul yang dapat dijangkau sebelum dan sesudah suatu sisi diabaikan sementara.

Setiap sisi yang telah dilewati ditandai sebagai selesai. Proses berlanjut sampai semua sisi pada graf hasil duplikasi telah dilewati dan rute kembali ke titik awal.

## 5. Struktur Implementasi Python

Program dibagi menjadi beberapa bagian utama.

| Bagian | Fungsi |
|---|---|
| Representasi graf | Menyimpan simpul, sisi, dan bobot menggunakan daftar sisi serta adjacency list. |
| `dijkstra()` | Menghitung jarak terpendek dan menyimpan informasi untuk merekonstruksi lintasan. |
| Pencarian simpul ganjil | Mengidentifikasi simpul yang mempunyai derajat ganjil. |
| `min_matching()` | Menggunakan dynamic programming dan bitmask untuk mencari biaya pencocokan minimum. |
| Duplikasi lintasan | Menambahkan kembali sisi-sisi yang diperlukan ke dalam graf. |
| `reachable_count()` | Menghitung jumlah simpul yang masih dapat dijangkau. |
| `is_bridge()` | Memeriksa apakah suatu sisi merupakan jembatan pada graf yang tersisa. |
| Fleury | Menyusun sirkuit Euler dengan melewati setiap sisi hasil duplikasi tepat satu kali. |
| Bagian keluaran | Menampilkan lintasan tambahan, rute, jumlah perjalanan, dan bobot total. |

## 6. Cara Menjalankan Program

Simpan kode program Python pada file bernama `chinese_postman.py`.

Pastikan Python 3 telah terpasang. Program hanya menggunakan pustaka standar Python sehingga tidak memerlukan instalasi paket tambahan.

Jalankan melalui terminal dengan perintah:

```bash
python chinese_postman.py
```

Apabila sistem menggunakan perintah `python3`, jalankan dengan:

```bash
python3 chinese_postman.py
```

Program kemudian menghitung simpul berderajat ganjil, mencari lintasan tambahan minimum, menduplikasi sisi, dan menyusun sirkuit Euler.

## 7. Hasil dan Analisis

Hasil matematis untuk graf pada soal adalah sebagai berikut.

| Komponen | Hasil |
|---|---:|
| Jumlah sisi asli | 11 |
| Total bobot sisi asli | 31 |
| Simpul berderajat ganjil | u dan v |
| Lintasan tambahan minimum | u-x-y-w-v |
| Bobot lintasan tambahan | 6 |
| Jumlah sisi setelah duplikasi | 15 |
| **Total bobot rute optimal** | **37** |

Jumlah sisi setelah duplikasi adalah 15 karena terdapat 11 sisi asli dan 4 sisi tambahan.

Urutan rute yang ditampilkan program dapat bergantung pada urutan pemrosesan sisi. Namun, selama semua sisi hasil duplikasi dilewati tepat satu kali dan rute kembali ke titik awal, total bobot minimumnya tetap 37.

## 8. Kesimpulan

Chinese Postman Problem pada graf ini diselesaikan dengan menghitung total bobot sisi asli, mencari simpul berderajat ganjil, dan menentukan lintasan tambahan minimum menggunakan Dijkstra serta dynamic programming dengan bitmask.

Lintasan `u-x-y-w-v` mempunyai bobot 6 dan perlu diulangi agar semua simpul mempunyai derajat genap. Selanjutnya, algoritma Fleury digunakan untuk membentuk sirkuit Euler pada graf hasil duplikasi.

Berdasarkan perhitungan tersebut, total bobot minimum yang diperlukan untuk melewati seluruh jalan dan kembali ke titik awal adalah **37**.

Implementasi ini mengasumsikan graf tak berarah, terhubung, dan memiliki bobot sisi nonnegatif. Pendekatan pencocokan dengan bitmask cocok untuk jumlah simpul berderajat ganjil yang relatif kecil karena kebutuhan komputasinya meningkat secara eksponensial terhadap jumlah simpul tersebut.