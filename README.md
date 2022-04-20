# IF2250-2021-K01-16-Usada Carbon Tracker

Tugas Besar IF2250 Rekayasa Perangkat Lunak 2021 - Usada Carbon Tracker

## K01 - Kelompok 16
| NIM      | Nama                      |
| ---      | ----                      |
| 13520003 | Dzaky Fattan Rizqullah    |
| 13520091 | Andreas Indra Kurniawan   |
| 13520127 | Adzka Ahmadetya Zaidan    |
| 13520157 | Thirafi Najwan Kurniatama |


## 1. Penjelasan Singkat Aplikasi
Usada Carbon Tracker merupakan sebuah aplikasi pencatat jejak karbon yang dihasilkan dari alat elektronik serta emisi bahan bakar. 
## 2. Requirements
Program dijalankan dengan ```Python 3.97```
Modul yang mungkin perlu diinstall menggunakan pip install:
- Lorem
- PyQt5
- Datetime
## 3. Cara Menjalankan Aplikasi
1. Current working directory harus berada pada folder src
2. Lalu jalankan command ```python main.py```
3. Aplikasi akan muncul pada windows
4. Untuk mengakses fitur harus dilakukan login
5. Jika tidak memiliki akun maka lakukan register terlebih dahulu dengan menekan hyperlink ```sign up now```
## 4. Daftar Modul yang Diimplementasi
1. Login/Register
2. Catatan jejak aktivitas
3. Tips and Tricks
4. Membership
## 5. Daftar Tabel Basis Data

<table>
<tr><th>account</th><th>activity_history</th></tr>
<tr>
<td>
<ins>username</ins><br>
email<br>
password<br> 
credit_card<br>
no_telp<br>
account_status
</td>
<td>
<ins>activityid</ins><br>
username<br>
nama_aktivitas
kategori<br>
jumlah_bensin<br>
total_watt<br>
timestamp_key
</td>
</tr>
</table>

<table>
<tr><th>daftar_berita</th><th>tips_and_trick</th></tr>
<tr>
<td>
<ins>beritaid</ins><br>
judul<br>
subtitle<br>
konten<br>
timestamp_key
</td>
<td>
<ins>tntid</ins><br>
judul<br>
subtitle<br>
konten<br>
timestamp_key
</td>
</tr>
</table>

<table>
<tr><th>pending_membership</th><th>logged_user</th></tr>
<tr>
<td>
<ins>requestid</ins><br>
username<br>
timestamp_key
</td>
<td>
<ins>username</ins>
</td>
</tr>
</table>