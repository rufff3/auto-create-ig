TOOLS INSTAGRAM - README
=======================

📌 DESKRIPSI
------------
Script ini adalah *Instagram automation bot* berbasis Python + Selenium yang memiliki 3 fitur utama:
1. **Pembuatan akun Instagram otomatis** menggunakan email dari tempmail.ac.id.
2. **Pengecekan login akun** untuk akun yang tersimpan di `akun.txt`.
3. **Auto-follow target followers/following** dari akun tertentu.

Script berjalan secara headless dan mendukung banyak akun sekaligus.

📂 STRUKTUR FOLDER
------------------
Script secara otomatis membuat dua folder:
- `cookies/` : folder ini disiapkan (belum dipakai aktif di script ini).
- `data/` : folder tambahan untuk ekspansi ke depan.

📁 FILE YANG DIGUNAKAN
----------------------
- `akun.txt` : Tempat menyimpan akun yang dibuat. Format:
    email: example@mail.com
    username: username123
    sandi: password123
    =========================

📋 FITUR UTAMA
--------------
1. **Buat Akun Instagram (Menu 1)**
   - Mengambil email dari tempmail.ac.id (dengan tab switch, bukan iframe).
   - Validasi domain agar bukan domain blacklist.
   - Input nama, username, password, tanggal lahir.
   - Ambil OTP dari email dan verifikasi akun.
   - Simpan akun ke `akun.txt`.

2. **Cek Login Akun (Menu 2)**
   - Melakukan login ke semua akun dalam `akun.txt`.
   - Menampilkan status berhasil/gagal.

3. **Auto Follow dari Target (Menu 3)**
   - Meminta URL target profil Instagram.
   - Memilih mau follow dari followers atau following.
   - Melakukan proses follow sejumlah akun sesuai input.

🚨 CATATAN PENTING
------------------
❗ Script ini TIDAK memiliki deteksi CAPTCHA.
Jika saat menjalankan menu manapun (terutama saat membuat akun) terjadi error **setelah login berhasil** atau bahkan sebelumnya,
maka kemungkinan besar **akun terkena CAPTCHA** dan script gagal melanjutkan.

🛠 KOMPONEN YANG HARUS DIINSTALL
--------------------------------
Jalankan perintah ini untuk menginstall semua dependensi:

```bash
pip install selenium webdriver-manager colorama pyfiglet
```

💡 Catatan Tambahan:
- Versi ChromeDriver akan otomatis disesuaikan.
- Untuk versi Solana CLI (tidak digunakan di script ini), tidak ada ketergantungan.
- Script menggunakan `--headless=new` agar bisa berjalan tanpa GUI.

✅ TESTED ON:
------------
- Python 3.10+
- Google Chrome versi terbaru
- Sistem operasi Windows/Linux

-----------------------
Gunakan script ini hanya untuk edukasi.
Penulis script tidak bertanggung jawab atas penyalahgunaan.
