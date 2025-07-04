import sqlite3

class OgrenciSistemi:
    def __init__(self):
        self.conn = sqlite3.connect("ogrenciler.db")
        self.cursor = self.conn.cursor()
        self.tablo_olustur()

    def tablo_olustur(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ogrenciler(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            soyad TEXT NOT NULL,
            bolum TEXT NOT NULL,
            numara TEXT NOT NULL UNIQUE,
            vize INTEGER DEFAULT 0,
            final INTEGER DEFAULT 0,
            harf_notu TEXT DEFAULT '',
            durum TEXT DEFAULT ''
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS dersler(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ders_adi TEXT NOT NULL UNIQUE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS notlar(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ogrenci_id INTEGER,
            ders_id INTEGER,
            vize INTEGER,
            final INTEGER,
            FOREIGN KEY(ogrenci_id) REFERENCES ogrenciler(id),
            FOREIGN KEY(ders_id) REFERENCES dersler(id),
            UNIQUE(ogrenci_id, ders_id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT UNIQUE,
            sifre TEXT,
            rol TEXT
        )
        """)

        self.conn.commit()

    # Kullanıcı giriş kontrolü
    def kullanici_giris(self, kullanici_adi, sifre):
        self.cursor.execute("SELECT rol, id FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        return self.cursor.fetchone()

    # Öğrenci işlemleri
    def ogrencileri_getir(self):
        self.cursor.execute("SELECT * FROM ogrenciler")
        return self.cursor.fetchall()

    def ogrenci_ekle(self, ad, soyad, bolum, numara):
        try:
            self.cursor.execute("INSERT INTO ogrenciler (ad, soyad, bolum, numara) VALUES (?, ?, ?, ?)",
                                (ad, soyad, bolum, numara))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def ogrenci_guncelle(self, ogrenci_id, ad, soyad, bolum, numara):
        try:
            self.cursor.execute("""
            UPDATE ogrenciler SET ad=?, soyad=?, bolum=?, numara=? WHERE id=?
            """, (ad, soyad, bolum, numara, ogrenci_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def ogrenci_sil(self, ogrenci_id):
        self.cursor.execute("DELETE FROM ogrenciler WHERE id=?", (ogrenci_id,))
        self.conn.commit()

    # Ders işlemleri
    def dersleri_getir(self):
        self.cursor.execute("SELECT * FROM dersler")
        return self.cursor.fetchall()

    def ders_ekle(self, ders_adi):
        try:
            self.cursor.execute("INSERT INTO dersler (ders_adi) VALUES (?)", (ders_adi,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def ders_sil(self, ders_id):
        self.cursor.execute("DELETE FROM dersler WHERE id=?", (ders_id,))
        self.conn.commit()

    # Not işlemleri
    def not_kaydet(self, ogrenci_id, ders_id, vize, final):
        # Harf notu ve durum hesapla
        ortalama = vize * 0.4 + final * 0.6
        if ortalama >= 85:
            harf_notu = "AA"
            durum = "Geçti"
        elif ortalama >= 70:
            harf_notu = "BA"
            durum = "Geçti"
        elif ortalama >= 60:
            harf_notu = "BB"
            durum = "Geçti"
        elif ortalama >= 50:
            harf_notu = "CB"
            durum = "Geçti"
        elif ortalama >= 40:
            harf_notu = "CC"
            durum = "Geçti"
        elif ortalama >= 30:
            harf_notu = "DC"
            durum = "Koşullu"
        elif ortalama >= 20:
            harf_notu = "DD"
            durum = "Koşullu"
        else:
            harf_notu = "FF"
            durum = "Kaldı"

        self.cursor.execute("""
        INSERT INTO notlar (ogrenci_id, ders_id, vize, final) VALUES (?, ?, ?, ?)
        ON CONFLICT(ogrenci_id, ders_id) DO UPDATE SET vize=?, final=?
        """, (ogrenci_id, ders_id, vize, final, vize, final))
        self.conn.commit()

        # Notların harf ve durum bilgisini ogrenciler tablosuna yansıt (opsiyonel)
        self.cursor.execute("""
        UPDATE ogrenciler SET vize=?, final=?, harf_notu=?, durum=? WHERE id=?
        """, (vize, final, harf_notu, durum, ogrenci_id))
        self.conn.commit()

    def not_listesi(self):
        self.cursor.execute("""
        SELECT o.ad || ' ' || o.soyad, d.ders_adi, n.vize, n.final
        FROM notlar n
        JOIN ogrenciler o ON n.ogrenci_id = o.id
        JOIN dersler d ON n.ders_id = d.id
        ORDER BY o.ad
        """)
        return self.cursor.fetchall()

    def ogrenci_ders_notlari(self, ogrenci_id):
        self.cursor.execute("""
        SELECT d.ders_adi, n.vize, n.final,
        CASE
            WHEN (n.vize*0.4 + n.final*0.6) >= 85 THEN 'AA'
            WHEN (n.vize*0.4 + n.final*0.6) >= 70 THEN 'BA'
            WHEN (n.vize*0.4 + n.final*0.6) >= 60 THEN 'BB'
            WHEN (n.vize*0.4 + n.final*0.6) >= 50 THEN 'CB'
            WHEN (n.vize*0.4 + n.final*0.6) >= 40 THEN 'CC'
            WHEN (n.vize*0.4 + n.final*0.6) >= 30 THEN 'DC'
            WHEN (n.vize*0.4 + n.final*0.6) >= 20 THEN 'DD'
            ELSE 'FF'
        END AS harf_notu,
        CASE
            WHEN (n.vize*0.4 + n.final*0.6) >= 30 THEN 'Geçti'
            ELSE 'Kaldı'
        END AS durum
        FROM notlar n
        JOIN dersler d ON n.ders_id = d.id
        WHERE n.ogrenci_id=?
        """, (ogrenci_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
