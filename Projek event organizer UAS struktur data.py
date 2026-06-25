import csv
import os

FILE_CSV = "event.csv"

database_event = {}

stack_undo = []

def muat_data_dari_csv():
    global database_event
    database_event = {} 
    
    if os.path.exists(FILE_CSV):
        with open(FILE_CSV, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None) 
            
            for baris in reader:
                if len(baris) == 5:
                    id_ev, nama, tgl, lok, kap = baris
                    
                    database_event[id_ev] = {
                        "id": id_ev,
                        "nama": nama,
                        "tanggal": tgl,
                        "lokasi": lok,
                        "kapasitas": kap
                    }

# Fungsi buat nyimpen semua data di Dictionary balik ke file CSV
def simpan_data_ke_csv():
    with open(FILE_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        writer.writerow(["ID", "Nama Event", "Tanggal", "Lokasi", "Kapasitas"])
        
        
        for data in database_event.values():
            writer.writerow([data["id"], data["nama"], data["tanggal"], data["lokasi"], data["kapasitas"]])


def tambah_event():
    muat_data_dari_csv()
    print("\n--- TAMBAH EVENT ---")
    id_ev = input("Masukkan ID Event: ")
    
    # Cek apakah ID sudah ada di Hash Map
    if id_ev in database_event:
        print("ID sudah dipake! Gagal nambahin.")
        return
        
    nama = input("Nama Event: ")
    tgl  = input("Tanggal   : ")
    lok  = input("Lokasi    : ")
    kap  = input("Kapasitas : ")
    
    # Simpan ke Hash Map
    database_event[id_ev] = {"id": id_ev, "nama": nama, "tanggal": tanggal, "lokasi": lok, "kapasitas": kap}
    simpan_data_ke_csv()
    print("Event berhasil disimpan!")

# [READ] Tampilkan Semua Event
def lihat_event():
    muat_data_dari_csv()
    print("\n--- DAFTAR EVENT ---")
    if not database_event:
        print("Tidak ada data event.")
        return
        
    for data in database_event.values():
        print(f"ID: {data['id']} | Nama: {data['nama']} | Tgl: {data['tanggal']} | Lokasi: {data['lokasi']} | Kuota: {data['kapasitas']}")

# [Update] Ubah Data Event
def ubah_event():
    muat_data_dari_csv()
    print("\n--- UBAH EVENT ---")
    id_ev = input("Masukkan ID Event yang mau diubah: ")
    
    if id_ev not in database_event:
        print("ID Event tidak ditemukan!")
        return
        
    print("Masukkan data baru:")
    database_event[id_ev]["nama"] = input("Nama Baru: ")
    database_event[id_ev]["tanggal"] = input("Tgl Baru : ")
    database_event[id_ev]["lokasi"] = input("Lokasi Baru: ")
    database_event[id_ev]["kapasitas"] = input("Kapasitas Baru: ")
    
    simpan_data_ke_csv()
    print("Data sukses diubah!")

# [Delete] Hapus Event & Masuk ke Stack Undo
def hapus_event():
    muat_data_dari_csv()
    print("\n--- HAPUS EVENT ---")
    id_ev = input("Masukkan ID Event yang mau dihapus: ")
    
    if id_ev not in database_event:
        print("ID Event tidak ketemu!")
        return
        
    # Push ke Stack: Ambil datanya, masukin ke list stack_undo sebelum diapus
    data_dihapus = database_event[id_ev]
    stack_undo.append(data_dihapus)
    
    # Hapus dari Hash Map
    del database_event[id_ev]
    
    simpan_data_ke_csv()
    print("Event berhasil dihapus! ")

# [STACK OPERATION] Batalkan Hapus (Undo)
def undo_hapus():
    muat_data_dari_csv()
    print("\n--- UNDO HAPUS (STACK) ---")
    
    # Cek apakah stack kosong atau tidak
    if len(stack_undo) == 0:
        print("Tidak ada data yang bisa di-undo.")
        return
        
    # POP dari Stack Ambil data paling terakhir yang dihapus
    data_kembali = stack_undo.pop()
    
    # Masukin lagi ke Hash Map utama
    id_ev = data_kembali["id"]
    database_event[id_ev] = data_kembali
    
    simpan_data_ke_csv()
    print(f"Sukses! Event '{data_kembali['nama']}' dibalikin lagi.")

# [SEARCHING] Linear Search Nyari Nama Event
def cari_event():
    muat_data_dari_csv()
    print("\n--- CARI EVENT ---")
    cari = input("Masukkan nama event yang dicari: ").lower()
    ketemu = False
    
    # Ngecek satu-satu dari awal sampe abis (Linear Search)
    for data in database_event.values():
        if cari in data["nama"].lower():
            print(f"Ketemu -> ID: {data['id']} | Nama: {data['nama']} | Lokasi: {data['lokasi']}")
            ketemu = True
            
    if not ketemu:
        print("Event Tidak ketemu.")

# [SORTING] Bubble Sort Mengurutkan Nama Event (A-Z)
def urutkan_event():
    muat_data_dari_csv()
    print("\n--- URUTKAN EVENT (A-Z) ---")
    
    # Ubah dulu dict values jadi list biasa biar bisa disorting
    list_event = list(database_event.values())
    jumlah_data = len(list_event)
    
    if jumlah_data == 0:
        print("Tidak ada data buat diurutkan.")
        return
        
    
    for i in range(jumlah_data):
        for j in range(0, jumlah_data - i - 1):
            if list_event[j]["nama"].lower() > list_event[j+1]["nama"].lower():
                
                list_event[j], list_event[j+1] = list_event[j+1], list_event[j]
                
 
    for data in list_event:
        print(f"Nama: {data['nama']} | ID: {data['id']} | Lokasi: {data['lokasi']}")

while True:
    print("\n=============================")
    print("    MENU EVENT ORGANIZER     ")
    print("=============================")
    print("1. Tambah Event (Create)")
    print("2. Lihat Semua Event (Read)")
    print("3. Ubah Event (Update)")
    print("4. Hapus Event (Delete)")
    print("5. Cari Event (Searching)")
    print("6. Urutkan Event A-Z (Sorting)")
    print("7. Batalin Hapus (Undo - Stack)")
    print("0. Keluar")
    
    pilih = input("Pilih Menu: ")
    
    if pilih == "1":
        tambah_event()
    elif pilih == "2":
        lihat_event()
    elif pilih == "3":
        ubah_event()
    elif pilih == "4":
        hapus_event()
    elif pilih == "5":
        cari_event()
    elif pilih == "6":
        urutkan_event()
    elif pilih == "7":
        undo_hapus()
    elif pilih == "0":
        print("Program Selesai!")
        break
    else:
        print("Menu Tidak ada, pilih yang bener!")