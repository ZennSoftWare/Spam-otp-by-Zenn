## ** 📦  INSTALASI DI TERMUX YGY **
*_Jalankan perintah ini di termux_*

```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests
git clone https://github.com/username/otp-spammer.git
cd 

# ** MENJALANKAN NYA **
```bash
python otp_spammer.py
# atau langsung dengan nomor
python otp_spammer.py 62xxx

---

## ** ATAU LEBIH DETAIL CARA MENJALANKAN DI TERMUX **

---

## 📱 Yang Harus Dilakukan di Termux

### 1. Instalasi Dasar
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests

---

### 1.Clone Repository Ini
git clone https://github.com/username/otp-spammer.git
cd otp-spammer

-----

### 3.Beri Izin Eksekusi (Opsional)
```bash
chmod +x otp_spammer.py

---

### 4.Jalankan Tools nya
```bash
python otp_spammer.py
# atau langsung dengan nomor
python otp_spammer.py 62xxx

---

## ** ⚠️ Hal Penting yang Perlu Diperhatikan **

** 1. Sumber Proxy Bisa Diblokir: Script mengambil proxy dari proxyscrape.com dan spys.me. Jika koneksi internet di Indonesia memblokir situs tersebut, ambil proxy manual dan isi ke variabel PROXY_LIST. **

** 2. Izin Penyimpanan: Jika ingin edit script dari aplikasi lain: **
   ```bash
   termux-setup-storage
   ```
   
** 3. Koneksi Internet Stabil: Tools ini sangat bergantung pada koneksi internet. Pastikan koneksi stabil, idealnya pakai Wi-Fi. **

** 4. Update Endpoint OTP: Daftar layanan di script hanyalah contoh dan bisa usang. Pantau dan perbarui sendiri secara berkala. **

---

## ** 📋 Checklist Sebelum Push ke GitHub **

· Script berhasil diuji di Termux
· requirements.txt sudah dibuat
· README.md berisi panduan instalasi lengkap
· Tidak ada data sensitif (nomor, token, dll.) di dalam script

---

** CATATAN!! **: Dilarang Mengambil Source Code Tanpa Credit/LICENSE dari pencipta nya!! 

#_Ide Itu Mahal_
