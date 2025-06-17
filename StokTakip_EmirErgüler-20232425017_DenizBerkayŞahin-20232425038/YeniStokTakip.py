import pyodbc
from tkinter import *
from tkinter import messagebox

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'
    'DATABASE=StokTakip;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()#execute()

root = Tk()
root.title("Giriş Ekranı")
root.geometry("500x400")
root.config(bg="white")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 400
window_height = 400
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

urunler = []


def urunListele():
    global urunler
    listbox.delete(0, END)
    cursor.execute("SELECT ID, Isim, Fiyat, Adet FROM Urunler")
    rows = cursor.fetchall()  # liste olarak alir
    urunler = [{"id": row.ID, "isim": row.Isim, "fiyat": row.Fiyat, "adet": row.Adet} for row in rows]

    if not urunler:
        listbox.insert(END, "Henüz ürün eklenmedi.")
    else:
        for urun in urunler:
            listbox.insert(END, f"{urun['id']} - {urun['isim']} - {urun['fiyat']} TL - {urun['adet']} adet")


def urunEkle():
    isim = isim_entry.get()
    fiyat = fiyat_entry.get()
    adet = adet_entry.get()

    if not isim or not fiyat.isdigit() or not adet.isdigit():
        messagebox.showwarning("Hata", "Lütfen geçerli veriler girin.")
        return

    cursor.execute("INSERT INTO Urunler (Isim, Fiyat, Adet) VALUES (?, ?, ?)", isim, int(fiyat),
                   int(adet))  # Yeni ürün eklemek için SQL sorgusu
    conn.commit()  # Değişiklikleri veritabanına kaydet
    urunListele()
    isim_entry.delete(0, END)
    fiyat_entry.delete(0, END)
    adet_entry.delete(0, END)


def urunSil():
    secim = listbox.curselection()
    if secim:
        urun_id = urunler[secim[0]]['id']
        cursor.execute("DELETE FROM Urunler WHERE ID=?", urun_id)  # Ürünü veritabanından silmek için SQL sorgusu
        conn.commit()  # Değişiklikleri veritabanına kaydet
        urunListele()
    else:
        messagebox.showwarning("Hata", "Lütfen bir ürün seçin.")


def urunSec():
    secim = listbox.curselection()
    if secim:
        urun = urunler[secim[0]]
        isim_entry.delete(0, END)
        isim_entry.insert(0, urun["isim"])
        fiyat_entry.delete(0, END)
        fiyat_entry.insert(0, urun["fiyat"])
        adet_entry.delete(0, END)
        adet_entry.insert(0, urun["adet"])
    else:
        messagebox.showwarning("Hata", "Lütfen bir ürün seçin.")


def urunGuncelle():
    secim = listbox.curselection()
    if secim:
        indeks = secim[0]
        isim = isim_entry.get()
        fiyat = fiyat_entry.get()
        adet = adet_entry.get()

        cursor.execute(
            "UPDATE Urunler SET Isim=?, Fiyat=?, Adet=? WHERE ID=?",
            isim, int(fiyat), int(adet), urunler[indeks]["id"]
        )  # Ürünü güncellemek için SQL sorgusu
        conn.commit()  # Değişiklikleri veritabanına kaydet
        urunListele()
        isim_entry.delete(0, END)
        fiyat_entry.delete(0, END)
        adet_entry.delete(0, END)
        messagebox.showinfo("Başarılı", "Ürün başarıyla güncellendi.")
    else:
        messagebox.showwarning("Hata", "Lütfen bir ürün seçin.")


def giris():
    kullaniciAd = entry1.get()
    sifre = entry2.get()

    cursor.execute("SELECT COUNT(*) FROM Kullanicilar WHERE KullaniciAdi=? AND Sifre=?", kullaniciAd,
                   sifre)  # Kullanıcı adı ve şifreyi kontrol eden SQL sorgusu
    result = cursor.fetchone()[0]  # Sonuçtan sayıyı al
    if result > 0:
        root.withdraw()
        anaSayfa = Toplevel()
        anaSayfa.title("Ana Sayfa")

        global isim_entry, fiyat_entry, adet_entry, listbox
        Label(anaSayfa, text="Ürün Adı:", font=("Ariel", 12)).pack(pady=5)
        isim_entry = Entry(anaSayfa)
        isim_entry.pack(pady=5)
        Label(anaSayfa, text="Fiyat:", font=("Ariel", 12)).pack(pady=5)
        fiyat_entry = Entry(anaSayfa)
        fiyat_entry.pack(pady=5)
        Label(anaSayfa, text="Adet:", font=("Ariel", 12)).pack(pady=5)
        adet_entry = Entry(anaSayfa)
        adet_entry.pack(pady=5)
        Button(anaSayfa, text="Ürün Ekle", command=urunEkle, bg="blue", fg="white", relief="flat", width=20).pack(pady=5)
        Button(anaSayfa, text="Ürünü Sil", command=urunSil, bg="red", fg="white", relief="flat", width=20).pack(pady=5)
        Button(anaSayfa, text="Ürünü Seç", command=urunSec, bg="green", fg="white", relief="flat", width=20).pack(pady=5)
        Button(anaSayfa, text="Ürün Güncelle", command=urunGuncelle, bg="orange", fg="white", relief="flat", width=20).pack(pady=5)
        listbox = Listbox(anaSayfa, width=50, height=10)
        listbox.pack(pady=10)
        urunListele()
    else:
        DurumLabel["text"] = "Hatalı giriş yaptınız."


def kullaniciKayit():
    kayit_penceresi = Toplevel()
    kayit_penceresi.title("Kayıt Ol")
    kayit_penceresi.geometry("340x400")

    screen_width = kayit_penceresi.winfo_screenwidth()
    screen_height = kayit_penceresi.winfo_screenheight()
    window_width = 340
    window_height = 400
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    kayit_penceresi.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    Label(kayit_penceresi, text="Yeni Kullanıcı Adı:", font=("Ariel", 12)).pack(pady=10)
    yeni_kullanici = Entry(kayit_penceresi, width=25)
    yeni_kullanici.pack(pady=5)

    Label(kayit_penceresi, text="Şifre:", font=("Ariel", 12)).pack(pady=10)
    yeni_sifre = Entry(kayit_penceresi, width=25, show="*")
    yeni_sifre.pack(pady=5)

    Label(kayit_penceresi, text="Şifreyi Tekrar Girin:", font=("Ariel", 12)).pack(pady=10)
    yeni_sifre_tekrar = Entry(kayit_penceresi, width=25, show="*")
    yeni_sifre_tekrar.pack(pady=5)

    Label(kayit_penceresi, text="Referans Kodu:", font=("Ariel", 12)).pack(pady=10)
    referans_kodu = Entry(kayit_penceresi, width=25)
    referans_kodu.pack(pady=5)

    def kayit_ol():
        kullaniciAd = yeni_kullanici.get()
        sifre = yeni_sifre.get()
        sifre_tekrar = yeni_sifre_tekrar.get()
        referans = referans_kodu.get()

        if referans != "izinliyim":
            messagebox.showerror("Hata", "Geçersiz referans kodu.", parent=kayit_penceresi)
            return

        if not kullaniciAd or not sifre or not sifre_tekrar:
            messagebox.showerror("Hata", "Tüm alanlar doldurulmalıdır.", parent=kayit_penceresi)
            return

        if sifre != sifre_tekrar:
            messagebox.showerror("Hata", "Şifreler uyuşmuyor.", parent=kayit_penceresi)
            return

        cursor.execute("SELECT COUNT(*) FROM Kullanicilar WHERE KullaniciAdi=?", kullaniciAd)  # Kullanıcı adı kontrolü
        result = cursor.fetchone()[0]
        if result > 0:
            messagebox.showerror("Hata", "Kullanıcı adı zaten mevcut.", parent=kayit_penceresi)
        else:
            cursor.execute("INSERT INTO Kullanicilar (KullaniciAdi, Sifre) VALUES (?, ?)", kullaniciAd, sifre)  # Yeni kullanıcı ekleme
            conn.commit()  # Değişiklikleri veritabanına kaydet
            messagebox.showinfo("Başarılı", "Kullanıcı başarıyla kaydedildi.", parent=kayit_penceresi)
            kayit_penceresi.destroy()

    Button(kayit_penceresi, text="Kaydol", command=kayit_ol, bg="blue", fg="white", relief="flat", width=20).pack(pady=20)


BaslıkLabel = Label(root, font=("Ariel", 14), text="Stok Takip Sistemine Hoş Geldiniz", bg="white", fg="blue")
KullanıcıAdiLabel = Label(root, font=("Ariel", 14), text="Kullanıcı Adı :", bg="white", fg="blue")
SifreLabel = Label(root, font=("Ariel", 14), text="Şifre :", bg="white", fg="blue")
DurumLabel = Label(root, font=("Ariel", 14), text="", bg="white", fg="red")
entry1 = Entry(root, width="25")
entry2 = Entry(root, width="25", show="*")
giris_button = Button(root, text="Giriş", font=("Ariel", 12), command=giris, width=10, bg="blue", fg="white", relief="flat")
kayit_button = Button(root, text="Kayıt Ol", font=("Ariel", 12), command=kullaniciKayit, width=10, bg="green", fg="white", relief="flat")

BaslıkLabel.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
KullanıcıAdiLabel.grid(row=2, column=0, pady=5)
SifreLabel.grid(row=3, column=0, pady=5)
DurumLabel.grid(row=6, column=1,pady=20)
entry1.grid(row=2, column=1, pady=5)
entry2.grid(row=3, column=1, pady=5)
giris_button.grid(row=4, column=1)
kayit_button.grid(row=5, column=1)

root.mainloop()