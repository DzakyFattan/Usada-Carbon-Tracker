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
## 2. Cara Menjalankan Aplikasi
1. Current working directory harus berada pada folder src
2. Lalu jalankan command ```python main.py```
3. Aplikasi akan muncul pada windows
4. Untuk mengakses fitur harus dilakukan login
5. Jika tidak memiliki akun maka lakukan register terlebih dahulu dengan menekan hyperlink ```sign up now```
## 3. Daftar Modul yang Diimplementasi
1. Login/Register
2. Catatan jejak aktivitas
3. Tips and Tricks
4. Membership
## 4. Daftar Tabel Basis Data

<table>
<tr><th>**account**</th><th>**activity_history**</th></tr>
<tr>
<td>
|    username    |
|      email     |
|    password    |
|   credit_card  |
|     no_telp    |
| account_status |
</td>
<td>
|      activityid      |
|       username       |
|    nama_aktivitas    |
|       kategori       |
|     jumlah_bensin    |
|      total_watt      |
|     timestamp_key    |
</td>
</tr>
</table>

<table>
<tr><th>**daftar_berita**</th><th>**tips_and_trick**</th></tr>
<tr>
<td>
|      beritaid     |
|       judul       |
|      subtitle     |
|       konten      |
|   timestamp_key   |
</td>
<td>
|        tntid       |
|        judul       |
|      subtitle      |
|       konten       |
|    timestamp_key   |
</td>
</tr>
</table>

<table>
<tr><th>**pending_membership**</th><th>**logged_user**</th></tr>
<tr>
<td>
|        requestid       |
|        username        |
|      timestamp_key     |
</td>
<td>
|     username    |
</td>
</tr>
</table>
