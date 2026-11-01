# Sumber internasional dan artikel bahasa Indonesia

## Perubahan

Bot sebelumnya sudah membaca Cointelegraph. Versi ini menambah BBC Business,
The Guardian Business, dan CoinDesk untuk melengkapi sumber Indonesia yang ada.
Ini penemuan berita melalui RSS penerbit, bukan pencarian seluruh internet.

Setiap feed sekarang mempunyai `url`, `name`, dan `language`. Daftar URL string
lama tetap bisa dipakai; bahasa diambil dari RSS bila tersedia, atau `und` jika
belum diketahui. Kandidat diambil bergiliran dari tiap feed agar satu media tidak
memenuhi seluruh batas kandidat. Log mencetak jumlah kandidat dan jumlah yang
berbahasa asing/tidak diketahui; angka ini bukan jumlah sumber yang akhirnya dipilih.

Filter relevansi kini memeriksa makna sumber asing dengan AI karena judul Indonesia
dan Inggris dapat membahas peristiwa sama tanpa kata yang sama. Pemeriksaan ini
juga menolak berita lain yang hanya menyebut lembaga yang sama. Ini menambah panggilan
API teks dan biaya sesuai model/pemakaian, termasuk saat dry-run dan penulisan ulang.

Pemilihan topik diperintahkan menolak topik lama walaupun bahasa sumber berbeda.
Riwayat URL, judul artikel dan preview tetap dipakai. Penilaian makna oleh AI tidak
menjamin semua duplikasi terdeteksi; tetap baca preview sebelum publikasi.

Penulisan menghasilkan judul, excerpt, subjudul, isi dan tag dalam bahasa Indonesia.
Bot menyintesis sumber dengan rujukan, bukan menerjemahkan ulang satu artikel penuh.
Nama, angka, mata uang dan tanggal dipertahankan. Berita negara lain harus menyebut
negara/yurisdiksi; tidak mengarang kurs rupiah atau menganggap aturan asing berlaku
bagi pembaca Indonesia. Istilah teknis dijelaskan saat pertama muncul.

`min_domains` di config dinaikkan dari 1 ke 2 agar artikel baru memakai sekurangnya
dua hostname sumber. Dua media dapat menyalin laporan asal yang sama: jumlah domain
adalah penyaring awal, bukan bukti independensi editorial. Jika bahan kurang atau tidak
ada pasangan peristiwa yang sama, bot boleh melewati topik, bukan memaksakan artikel.

## Memakai

Jalankan dari folder proyek setelah mengambil pembaruan kode dan config:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python bot.py --dry-run --category ekonomi
```

Atau pilih `bisnis`, `investasi`, `trading`, `crypto`, `keuangan-pribadi`, atau
hilangkan `--category` untuk rotasi otomatis. Sumber lokal dan internasional akan
dipertimbangkan bersama. Tidak ada jaminan setiap artikel memakai sumber asing:
pilihan tergantung topik, sumber terbaru dan kecukupan bukti. Untuk mencoba topik
baru, periksa nama preview yang baru dicetak di log.

```bash
xdg-open data/financepress-NAMA-BARU.html
python bot.py --from-preview data/financepress-NAMA-BARU.json
```

Ganti `NAMA-BARU` dengan nama file persis dari log. Perintah pertama hanya membuka
preview; perintah kedua memublikasikan artikel yang sudah ditinjau beserta gambar,
judul, kategori dan tag seperti sebelumnya. Dry-run tetap menggunakan saldo API
untuk teks dan gambar jika membuat konten baru.

Preview lama tidak otomatis diperbarui setelah config berubah. Jangan hapus database
atau riwayat untuk memaksa topik baru karena itu dapat menghilangkan proteksi duplikasi.
Jika memakai konfigurasi sendiri, gabungkan tambahan feed dan keyword Inggris ke
config tersebut; penggantian bot.py saja tidak menambahkan daftar sumber.

## Menambahkan penerbit lain

Tambahkan objek pada `feeds` di `config.json`, misalnya:

```json
{"url":"https://feeds.bbci.co.uk/news/business/rss.xml","name":"BBC Business","language":"en"}
```

URL harus HTTPS. Feed wajib menyediakan tanggal, ringkasan, tautan dan kata kunci
relevan; yang tidak memenuhi syarat akan dilewati. Sebagian penerbit memblokir
server tertentu, mengubah RSS, atau memakai paywall. Bot tidak melewati paywall;
jika isi publik tidak cukup, pilih topik lain. Keyword Inggris dapat ditambah pada
`keywords` tanpa menghapus keyword Indonesia.

## Validasi

53 tes unit lulus, termasuk format feed lama/baru, keseimbangan sumber, relevansi
lintas bahasa, penolakan indeks AI tidak valid, dan alur preview/publikasi lama.
Pengujian tidak memanggil API AI berbayar dan tidak mengunggah post ke WordPress.
Empat RSS internasional dalam config berhasil memberikan respons 200 dan entri RSS
saat pemeriksaan. Ketersediaan penerbit dapat berubah.

```bash
python -m unittest discover -s tests
```
