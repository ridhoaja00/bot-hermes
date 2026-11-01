# FinancePress dengan Hermes + ChatGPT Plus (Codex)

Mode ini menggunakan login **Hermes `openai-codex` milik pengguna Linux `hermes`** untuk *pembuatan teks* melalui CLI. Tidak menggunakan saldo OpenAI API untuk teks, tetapi **tetap memakai kuota penggunaan Codex paket ChatGPT**. Ketentuan penyedia dan dukungan penggunaan otomatis harus dipatuhi; tidak ada jaminan tugas 24/7 tanpa pembatasan. Ini bukan penggunaan API OpenAI gratis.

## Instal di Ubuntu VPS

```bash
# jalankan sebagai user hermes (bukan root)
cd ~/projects/financepress
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
nano .env
command -v hermes
hermes chat --provider openai-codex -Q -q 'Jawab hanya {"ok":true}'
python bot.py --check-site
python bot.py --check-auth
python bot.py --dry-run
```

Isi `WP_USERNAME` dan `WP_APP_PASSWORD` dengan **Application Password baru**, bukan password login WP. Jika login Codex ada di `/home/hermes/.hermes/`, gunakan user tersebut untuk proses bot dan jangan gunakan root/sudo saat menjalankan skrip. Setiap proses penulisan memanggil Hermes melalui `hermes chat ... --query-file -` dan memvalidasi JSON hasilnya. Jika respons tidak valid, bot berhenti tanpa menerbitkan draf tersebut. Hindari menjadwalkan banyak proses karena kuota Plus terbatas.

## Mode dan biaya
- `AI_PROVIDER=hermes`: teks lewat Hermes/Codex; `OPENAI_API_KEY` tidak perlu untuk teks.
- `ENABLE_AI_IMAGE=false`: tidak membuat gambar AI baru; gambar AI memerlukan OpenAI API terpisah jika diaktifkan.
- `AI_PROVIDER=openai`: perilaku API lama; set `OPENAI_API_KEY` dan `OPENAI_MODEL`.
- `POST_STATUS=draft`: aman untuk pengujian. `--from-preview FILE.json` dapat langsung **publish**; jangan jalankan sebelum diperiksa.

## Keamanan
- Jangan memasukkan `.env` atau file auth Hermes ke GitHub, ZIP, atau Telegram.
- **Cabut Application Password WordPress lama**: arsip asal memuat kredensial dan `.env.example` di repo pernah memuat password.
- Hermes diminta tidak menggunakan tool saat menulis JSON; tetap batasi akses Linux, token bot Telegram, dan jangan beri izin perintah kepada orang lain.
- Jangan gunakan `--loop` sebelum `--dry-run`, validasi fakta, integrasi kategori, dan cek duplikasi berhasil.

CLI Hermes resmi: https://hermes-agent.nousresearch.com/docs/user-guide/cli/
