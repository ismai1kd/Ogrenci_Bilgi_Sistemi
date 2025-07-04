import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ogrenci_sistemi import OgrenciSistemi
import openpyxl

class OgrenciGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Öğrenci Bilgi Sistemi")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        self.sistem = OgrenciSistemi()

        # Giriş ile ilgili değişkenler
        self.kullanici_rol = None
        self.kullanici_ogrenci_id = None

        self.giris_secim_ekrani()

    def temizle(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def giris_secim_ekrani(self):
        self.temizle()
        tk.Label(self.root, text="Hoşgeldiniz", font=("Arial", 30, "bold"), pady=40).pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=60)

        btn_ogrenci = tk.Button(frame, text="Öğrenci Girişi", font=("Arial", 22), width=15, height=3, command=self.ogrenci_giris_ekrani)
        btn_ogrenci.grid(row=0, column=0, padx=40, pady=20)

        btn_admin = tk.Button(frame, text="Admin Girişi", font=("Arial", 22), width=15, height=3, command=self.admin_giris_ekrani)
        btn_admin.grid(row=0, column=1, padx=40, pady=20)

    # --- Admin Giriş ---
    def admin_giris_ekrani(self):
        self.temizle()
        tk.Label(self.root, text="Admin Girişi", font=("Arial", 26, "bold"), pady=20).pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Kullanıcı Adı:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=5, pady=10)
        self.entry_admin_kullanici = tk.Entry(frame, font=("Arial", 14))
        self.entry_admin_kullanici.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(frame, text="Şifre:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.entry_admin_sifre = tk.Entry(frame, show="*", font=("Arial", 14))
        self.entry_admin_sifre.grid(row=1, column=1, padx=5, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Giriş Yap", font=("Arial", 14), width=15, command=self.admin_giris).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Geri", font=("Arial", 14), width=15, command=self.giris_secim_ekrani).grid(row=0, column=1, padx=10)

    def admin_giris(self):
        kullanici_adi = self.entry_admin_kullanici.get().strip()
        sifre = self.entry_admin_sifre.get().strip()
        if not (kullanici_adi and sifre):
            messagebox.showwarning("Eksik Bilgi", "Lütfen kullanıcı adı ve şifre girin.")
            return
        sonuc = self.sistem.kullanici_giris(kullanici_adi, sifre)
        if sonuc is None or sonuc[0] != "admin":
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış ya da admin değilsiniz.")
            return
        self.kullanici_rol = "admin"
        self.kullanici_ogrenci_id = None
        messagebox.showinfo("Başarılı", "Admin olarak giriş yapıldı.")
        self.ana_menu()

    # --- Öğrenci Giriş ---
    def ogrenci_giris_ekrani(self):
        self.temizle()
        tk.Label(self.root, text="Öğrenci Girişi", font=("Arial", 26, "bold"), pady=20).pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Burada "TC" ve "Öğrenci Numarası" olarak iki giriş alanı istedin ama ogrenci tablosunda TC yok.
        # Bu yüzden biz numarayı TC gibi kullanalım ve giriş olarak 2 alan yerine 1 alan koyuyorum: Numara (TC+Numara karma da olabilir)
        # Ama istersen iki alan da ekleriz, şimdilik 2 alan yapalım (Numara ve Soyadı gibi).

        tk.Label(frame, text="TC Kimlik No:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=5, pady=10)
        self.entry_tc = tk.Entry(frame, font=("Arial", 14))
        self.entry_tc.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(frame, text="Öğrenci Numarası:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.entry_ogrenci_numara = tk.Entry(frame, font=("Arial", 14))
        self.entry_ogrenci_numara.grid(row=1, column=1, padx=5, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Giriş Yap", font=("Arial", 14), width=15, command=self.ogrenci_giris).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Geri", font=("Arial", 14), width=15, command=self.giris_secim_ekrani).grid(row=0, column=1, padx=10)

    def ogrenci_giris(self):
        tc = self.entry_tc.get().strip()
        numara = self.entry_ogrenci_numara.get().strip()
        if not (tc and numara):
            messagebox.showwarning("Eksik Bilgi", "Lütfen TC ve öğrenci numarasını girin.")
            return
        # Veritabanında TC yok, bu yüzden sadece numara ile kontrol yapalım.
        # Eğer TC eklemek istersen ogrenciler tablosuna yeni sütun eklemelisin.
        self.sistem.cursor.execute("SELECT id FROM ogrenciler WHERE numara=?", (numara,))
        sonuc = self.sistem.cursor.fetchone()
        if sonuc:
            self.kullanici_rol = "ogrenci"
            self.kullanici_ogrenci_id = sonuc[0]
            messagebox.showinfo("Başarılı", f"Öğrenci olarak giriş yapıldı. Hoşgeldiniz!")
            self.ana_menu()
        else:
            messagebox.showerror("Hata", "Öğrenci bulunamadı veya bilgiler yanlış.")

    # --- Ana Menü ---
    def ana_menu(self):
        self.temizle()
        tk.Label(self.root, text="Öğrenci Bilgi Sistemi", font=("Arial", 20, "bold"), pady=20).pack()

        if self.kullanici_rol == "admin":
            tk.Button(self.root, text="Öğrenci İşlemleri", font=("Arial", 14), width=25, command=self.ogrenci_menu).pack(pady=10)
            tk.Button(self.root, text="Ders İşlemleri", font=("Arial", 14), width=25, command=self.ders_menu).pack(pady=10)
            tk.Button(self.root, text="Not Verme ve Listeleme", font=("Arial", 14), width=25, command=self.not_menu).pack(pady=10)
            tk.Button(self.root, text="Öğrenci Notlarını Görüntüle", font=("Arial", 14), width=25, command=self.ogrenci_notlari_menu).pack(pady=10)

        elif self.kullanici_rol == "ogrenci":
            tk.Button(self.root, text="Notlarımı Görüntüle", font=("Arial", 14), width=25, command=self.ogrenci_notlarimi_goster).pack(pady=10)

        tk.Button(self.root, text="Çıkış", font=("Arial", 14), width=25, command=self.cikis).pack(pady=10)

    # --- Öğrenci Menüleri (admin erişimi) ---
    def ogrenci_menu(self):
        # Kod aynen önceki gibi (Değişmedi)
        from copy import deepcopy
        self.temizle()
        tk.Label(self.root, text="Öğrenci İşlemleri", font=("Arial", 18, "bold"), pady=10).grid(row=0, column=0, columnspan=5)

        tk.Label(self.root, text="Ad").grid(row=1, column=0, sticky="w", padx=5)
        self.entry_ad = tk.Entry(self.root)
        self.entry_ad.grid(row=1, column=1, padx=5)

        tk.Label(self.root, text="Soyad").grid(row=2, column=0, sticky="w", padx=5)
        self.entry_soyad = tk.Entry(self.root)
        self.entry_soyad.grid(row=2, column=1, padx=5)

        tk.Label(self.root, text="Bölüm").grid(row=3, column=0, sticky="w", padx=5)
        self.entry_bolum = tk.Entry(self.root)
        self.entry_bolum.grid(row=3, column=1, padx=5)

        tk.Label(self.root, text="Numara").grid(row=4, column=0, sticky="w", padx=5)
        self.entry_numara = tk.Entry(self.root)
        self.entry_numara.grid(row=4, column=1, padx=5)

        tk.Button(self.root, text="Ekle", width=12, command=self.ogrenci_ekle).grid(row=5, column=0, pady=10, padx=5)
        tk.Button(self.root, text="Güncelle", width=12, command=self.ogrenci_guncelle).grid(row=5, column=1, pady=10)
        tk.Button(self.root, text="Sil", width=12, command=self.ogrenci_sil).grid(row=5, column=2, pady=10)
        tk.Button(self.root, text="Ana Menü", width=12, command=self.ana_menu).grid(row=5, column=3, pady=10)

        columns = ("ID", "Ad", "Soyad", "Bölüm", "Numara", "Vize", "Final", "Harf Notu", "Durum")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Ad", width=120)
        self.tree.column("Soyad", width=120)
        self.tree.column("Bölüm", width=120)
        self.tree.column("Numara", width=100)
        self.tree.column("Vize", width=50, anchor="center")
        self.tree.column("Final", width=50, anchor="center")
        self.tree.column("Harf Notu", width=70, anchor="center")
        self.tree.column("Durum", width=90, anchor="center")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.grid(row=6, column=0, columnspan=5, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.ogrenci_secildi)

        self.ogrenci_listele()

    def ogrenci_listele(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.sistem.ogrencileri_getir():
            self.tree.insert("", "end", values=row)

    def ogrenci_secildi(self, event):
        secim = self.tree.selection()
        if secim:
            degerler = self.tree.item(secim)["values"]
            self.entry_ad.delete(0, "end")
            self.entry_ad.insert(0, degerler[1])
            self.entry_soyad.delete(0, "end")
            self.entry_soyad.insert(0, degerler[2])
            self.entry_bolum.delete(0, "end")
            self.entry_bolum.insert(0, degerler[3])
            self.entry_numara.delete(0, "end")
            self.entry_numara.insert(0, degerler[4])

    def ogrenci_ekle(self):
        ad = self.entry_ad.get().strip()
        soyad = self.entry_soyad.get().strip()
        bolum = self.entry_bolum.get().strip()
        numara = self.entry_numara.get().strip()
        if not (ad and soyad and bolum and numara):
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return
        if self.sistem.ogrenci_ekle(ad, soyad, bolum, numara):
            messagebox.showinfo("Başarılı", "Öğrenci eklendi.")
            self.ogrenci_listele()
            self.temizle_form()
        else:
            messagebox.showerror("Hata", "Bu numarada öğrenci zaten var.")

    def ogrenci_guncelle(self):
        secim = self.tree.selection()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen güncellenecek öğrenciyi seçin.")
            return
        ogrenci_id = self.tree.item(secim)["values"][0]
        ad = self.entry_ad.get().strip()
        soyad = self.entry_soyad.get().strip()
        bolum = self.entry_bolum.get().strip()
        numara = self.entry_numara.get().strip()
        if not (ad and soyad and bolum and numara):
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return
        if self.sistem.ogrenci_guncelle(ogrenci_id, ad, soyad, bolum, numara):
            messagebox.showinfo("Başarılı", "Öğrenci güncellendi.")
            self.ogrenci_listele()
            self.temizle_form()
        else:
            messagebox.showerror("Hata", "Bu numarada öğrenci zaten var.")

    def ogrenci_sil(self):
        secim = self.tree.selection()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen silinecek öğrenciyi seçin.")
            return
        ogrenci_id = self.tree.item(secim)["values"][0]
        cevap = messagebox.askyesno("Onay", "Seçilen öğrenci silinsin mi?")
        if cevap:
            self.sistem.ogrenci_sil(ogrenci_id)
            messagebox.showinfo("Başarılı", "Öğrenci silindi.")
            self.ogrenci_listele()
            self.temizle_form()

    def temizle_form(self):
        self.entry_ad.delete(0, "end")
        self.entry_soyad.delete(0, "end")
        self.entry_bolum.delete(0, "end")
        self.entry_numara.delete(0, "end")

    # --- Ders Menüsü ---
    def ders_menu(self):
        self.temizle()
        tk.Label(self.root, text="Ders İşlemleri", font=("Arial", 18, "bold"), pady=10).pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Ders Adı:").grid(row=0, column=0, sticky="w")
        self.entry_ders_adi = tk.Entry(frame)
        self.entry_ders_adi.grid(row=0, column=1, padx=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Ekle", width=12, command=self.ders_ekle).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Sil", width=12, command=self.ders_sil).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Ana Menü", width=12, command=self.ana_menu).grid(row=0, column=2, padx=5)

        columns = ("ID", "Ders Adı")
        self.ders_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        self.ders_tree.column("ID", width=50, anchor="center")
        self.ders_tree.column("Ders Adı", width=200)

        for col in columns:
            self.ders_tree.heading(col, text=col)

        self.ders_tree.pack(padx=10, pady=10)
        self.ders_tree.bind("<<TreeviewSelect>>", self.ders_secildi)

        self.dersleri_listele()

    def dersleri_listele(self):
        for i in self.ders_tree.get_children():
            self.ders_tree.delete(i)
        for row in self.sistem.dersleri_getir():
            self.ders_tree.insert("", "end", values=row)

    def ders_secildi(self, event):
        secim = self.ders_tree.selection()
        if secim:
            degerler = self.ders_tree.item(secim)["values"]
            self.entry_ders_adi.delete(0, "end")
            self.entry_ders_adi.insert(0, degerler[1])

    def ders_ekle(self):
        ders_adi = self.entry_ders_adi.get().strip()
        if not ders_adi:
            messagebox.showwarning("Eksik Bilgi", "Lütfen ders adı girin.")
            return
        if self.sistem.ders_ekle(ders_adi):
            messagebox.showinfo("Başarılı", "Ders eklendi.")
            self.dersleri_listele()
            self.entry_ders_adi.delete(0, "end")
        else:
            messagebox.showerror("Hata", "Bu ders zaten var.")

    def ders_sil(self):
        secim = self.ders_tree.selection()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen silinecek dersi seçin.")
            return
        ders_id = self.ders_tree.item(secim)["values"][0]
        cevap = messagebox.askyesno("Onay", "Seçilen ders silinsin mi?")
        if cevap:
            self.sistem.ders_sil(ders_id)
            messagebox.showinfo("Başarılı", "Ders silindi.")
            self.dersleri_listele()
            self.entry_ders_adi.delete(0, "end")

    # --- Not Menüsü ---
    def not_menu(self):
        self.temizle()
        tk.Label(self.root, text="Not Verme ve Listeleme", font=("Arial", 18, "bold"), pady=10).grid(row=0, column=0, columnspan=4)

        # Öğrenci seçimi
        tk.Label(self.root, text="Öğrenci:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combo_ogrenci = ttk.Combobox(self.root, state="readonly", width=40)
        self.combo_ogrenci.grid(row=1, column=1, padx=5, pady=5)
        self.ogrenciler = self.sistem.ogrencileri_getir()
        self.combo_ogrenci['values'] = [f"{o[1]} {o[2]} - {o[4]}" for o in self.ogrenciler]

        # Ders seçimi
        tk.Label(self.root, text="Ders:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_ders = ttk.Combobox(self.root, state="readonly", width=40)
        self.combo_ders.grid(row=2, column=1, padx=5, pady=5)
        self.dersler = self.sistem.dersleri_getir()
        self.combo_ders['values'] = [d[1] for d in self.dersler]

        # Vize ve final notları
        tk.Label(self.root, text="Vize:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_vize = tk.Entry(self.root)
        self.entry_vize.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Final:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_final = tk.Entry(self.root)
        self.entry_final.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Not Kaydet", width=20, command=self.not_kaydet).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Ana Menü", width=20, command=self.ana_menu).grid(row=6, column=0, columnspan=2, pady=10)

        # Not listesi tablosu
        columns = ("Öğrenci", "Ders", "Vize", "Final")
        self.not_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        for col in columns:
            self.not_tree.heading(col, text=col)
            if col == "Öğrenci":
                self.not_tree.column(col, width=200)
            elif col == "Ders":
                self.not_tree.column(col, width=150)
            else:
                self.not_tree.column(col, width=60, anchor="center")
        self.not_tree.grid(row=1, column=2, rowspan=6, padx=10, pady=10)

        self.notlari_listele()

    def notlari_listele(self):
        for i in self.not_tree.get_children():
            self.not_tree.delete(i)
        notlar = self.sistem.not_listesi()
        for ogrenci, ders, vize, final in notlar:
            self.not_tree.insert("", "end", values=(ogrenci, ders, vize, final))

    def not_kaydet(self):
        try:
            ogrenci_idx = self.combo_ogrenci.current()
            ders_idx = self.combo_ders.current()
            vize = int(self.entry_vize.get())
            final = int(self.entry_final.get())
        except ValueError:
            messagebox.showwarning("Hata", "Lütfen geçerli sayısal değerler girin.")
            return

        if ogrenci_idx == -1 or ders_idx == -1:
            messagebox.showwarning("Hata", "Lütfen öğrenci ve ders seçin.")
            return

        ogrenci_id = self.ogrenciler[ogrenci_idx][0]
        ders_id = self.dersler[ders_idx][0]

        self.sistem.not_kaydet(ogrenci_id, ders_id, vize, final)
        messagebox.showinfo("Başarılı", "Not kaydedildi.")
        self.notlari_listele()
        self.entry_vize.delete(0, "end")
        self.entry_final.delete(0, "end")
        self.combo_ogrenci.set('')
        self.combo_ders.set('')

    # --- Öğrenci Notlarını Görüntüleme (Admin için) ---
    def ogrenci_notlari_menu(self):
        self.temizle()
        tk.Label(self.root, text="Öğrenci Notları", font=("Arial", 18, "bold"), pady=10).pack()

        columns = ("Ders", "Vize", "Final", "Harf Notu", "Durum")
        self.notlar_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        for col in columns:
            anchor = "center" if col != "Ders" else "w"
            self.notlar_tree.column(col, width=100, anchor=anchor)
            self.notlar_tree.heading(col, text=col)

        self.notlar_tree.pack(padx=10, pady=10, fill="x")

        # Öğrenci seçimi için combobox
        tk.Label(self.root, text="Öğrenci Seç:").pack(pady=(10, 0))
        self.combo_ogrenci_notlari = ttk.Combobox(self.root, state="readonly", width=50)
        self.combo_ogrenci_notlari.pack()
        self.tum_ogrenciler = self.sistem.ogrencileri_getir()
        self.combo_ogrenci_notlari['values'] = [f"{o[1]} {o[2]} - {o[4]}" for o in self.tum_ogrenciler]

        self.combo_ogrenci_notlari.bind("<<ComboboxSelected>>", self.ogrenci_notlari_goster)

        # Excel aktar butonu alt kısımda
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Excel'e Aktar (Tüm Öğrenciler)", width=30, command=self.excel_tum_notlar_export).pack()

        tk.Button(self.root, text="Ana Menü", width=20, command=self.ana_menu).pack(pady=10)

    def ogrenci_notlari_goster(self, event):
        secim = self.combo_ogrenci_notlari.current()
        if secim == -1:
            return
        ogrenci_id = self.tum_ogrenciler[secim][0]

        notlar = self.sistem.ogrenci_ders_notlari(ogrenci_id)

        for i in self.notlar_tree.get_children():
            self.notlar_tree.delete(i)

        for ders, vize, final, harf, durum in notlar:
            self.notlar_tree.insert("", "end", values=(ders, vize, final, harf, durum))

    # --- Öğrenci kendi notlarını görebileceği ekran ---
    def ogrenci_notlarimi_goster(self):
        self.temizle()
        tk.Label(self.root, text="Notlarım", font=("Arial", 18, "bold"), pady=10).pack()

        columns = ("Ders", "Vize", "Final", "Harf Notu", "Durum")
        self.ogrenci_notlar_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)

        for col in columns:
            anchor = "center" if col != "Ders" else "w"
            self.ogrenci_notlar_tree.column(col, width=100, anchor=anchor)
            self.ogrenci_notlar_tree.heading(col, text=col)

        self.ogrenci_notlar_tree.pack(padx=10, pady=10, fill="x")

        notlar = self.sistem.ogrenci_ders_notlari(self.kullanici_ogrenci_id)
        for ders, vize, final, harf, durum in notlar:
            self.ogrenci_notlar_tree.insert("", "end", values=(ders, vize, final, harf, durum))

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Excel'e Aktar (Sadece Benim Notlarım)", width=30, command=self.excel_ogrenci_notlari_export).pack()

        tk.Button(self.root, text="Ana Menü", width=20, command=self.ana_menu).pack(pady=10)

    # --- Excel Export Fonksiyonları ---
    # Admin için tüm notları (tüm öğrenciler) Excel'e aktar, genel ortalamaları da ekle
    def excel_tum_notlar_export(self):
        dosya = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel dosyası", "*.xlsx")])
        if not dosya:
            return
        # Tüm notları al
        self.sistem.cursor.execute("""
            SELECT d.ders_adi, n.vize, n.final
            FROM notlar n
            JOIN dersler d ON n.ders_id = d.id
        """)
        tum_notlar = self.sistem.cursor.fetchall()

        # Ortalama hesaplamak için derslere göre grupla
        ders_notlari = {}
        for ders_adi, vize, final in tum_notlar:
            ort = vize*0.4 + final*0.6
            if ders_adi not in ders_notlari:
                ders_notlari[ders_adi] = []
            ders_notlari[ders_adi].append(ort)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Tüm Notlar"

        # Tablonun başlığı
        ws.append(["Ders", "Vize", "Final"])

        # Tüm notları tekrar çek
        self.sistem.cursor.execute("""
            SELECT o.ad || ' ' || o.soyad, d.ders_adi, n.vize, n.final
            FROM notlar n
            JOIN ogrenciler o ON n.ogrenci_id = o.id
            JOIN dersler d ON n.ders_id = d.id
            ORDER BY o.ad, d.ders_adi
        """)
        tum_notlar_detay = self.sistem.cursor.fetchall()

        ws.append(["Öğrenci", "Ders", "Vize", "Final"])
        for ogr, ders, vize, final in tum_notlar_detay:
            ws.append([ogr, ders, vize, final])

        # Altına boş satır koy
        ws.append([])
        ws.append(["Genel Not Ortalamaları (Her Ders)"])
        ws.append(["Ders", "Ortalama"])

        for ders_adi, ortalamalar in ders_notlari.items():
            genel_ortalama = round(sum(ortalamalar)/len(ortalamalar), 2)
            ws.append([ders_adi, genel_ortalama])

        wb.save(dosya)
        messagebox.showinfo("Başarılı", f"Tüm notlar ve genel ortalamalar '{dosya}' olarak kaydedildi.")

    # Öğrencinin sadece kendi notlarını Excel'e aktarma
    def excel_ogrenci_notlari_export(self):
        dosya = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel dosyası", "*.xlsx")])
        if not dosya:
            return

        notlar = self.sistem.ogrenci_ders_notlari(self.kullanici_ogrenci_id)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Notlarım"

        ws.append(["Ders", "Vize", "Final", "Harf Notu", "Durum"])
        for ders, vize, final, harf, durum in notlar:
            ws.append([ders, vize, final, harf, durum])

        wb.save(dosya)
        messagebox.showinfo("Başarılı", f"Notlarınız '{dosya}' olarak kaydedildi.")

    def cikis(self):
        self.sistem.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OgrenciGUI(root)
    root.mainloop()
