# 🎓 Öğrenci Bilgi Sistemi

> Python ile geliştirilmiş kullanıcı dostu bir masaüstü öğrenci bilgi yönetim sistemi.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Proje Hakkında

Bu uygulama, öğrencilerin ve yöneticilerin etkileşimli bir arayüz aracılığıyla **öğrenci yönetimi**, **ders yönetimi**, **not takibi** ve **raporlama** işlemlerini gerçekleştirmelerini sağlayan bir masaüstü çözümüdür.  
Kod yapısı **modüler**, veri işlemleri ve arayüz ayrı tutulmuştur.

## 🧰 Kullanılan Teknolojiler

- `Python 3.x`
- `Tkinter` – Grafiksel kullanıcı arayüzü (GUI)
- `SQLite` – Yerel veritabanı yönetimi
- `openpyxl` – Excel dosyalarına veri aktarma
- `OOP & MVC` benzeri yapı

---

## 🚀 Özellikler

### 👨‍💼 Admin Girişi ile:

- Öğrenci ekleme, silme, güncelleme
- Ders ekleme, silme
- Öğrenci ve derse özel not girişi (vize/final)
- Harf notu ve geçme durumu otomatik hesaplama
- Notları `Excel` olarak dışa aktarma (tüm öğrenciler ve genel ortalamalar dahil)

### 👨‍🎓 Öğrenci Girişi ile:

- Sadece kendi notlarını görüntüleme
- Notları Excel'e aktarma

### 🧠 Akıllı Özellikler:

- Ortalama bazlı **harf notu hesaplama**
- `ON CONFLICT` yapısıyla aynı öğrenci/ders için güncelleme yapabilme
- Yetkilendirme: Admin / Öğrenci ayrımı
- TreeView ile tablolu veri görüntüleme

---

## 📸 Video Görüntüleri

> 👉 Video'ya ulaşmak için: [Video Linki](https://www.youtube.com/watch?v=MHCPIqRilds&t=476s)

---

## 📁 Kurulum

### 1. Gerekli Modüller:

```bash
pip install openpyxl
```

Tkinter Python ile birlikte gelir, ayrıca kurmanız gerekmez.

### 2. Çalıştırma:

```bash
python ogrenci_gui.py
```

---

## 🗂 Dosya Yapısı

```
.
├── ogrenci_gui.py         # GUI arayüzü
├── ogrenci_sistemi.py     # Veritabanı ve işlemler
├── ogrenciler.db          # SQLite veritabanı (ilk çalıştırmada otomatik oluşur)
└── README.md
```

---

## 📤 Excel Raporlama

- `Admin` olarak tüm öğrencilerin notları, her ders için ortalama ile birlikte `.xlsx` olarak dışa aktarılabilir.
- `Öğrenci` olarak sadece kendi notlarını dışa aktarabilir.

---

## 📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasını inceleyin.

---

## ✨ Katkı ve Geri Bildirim

Bu projeyi geliştirmeye devam etmek istiyorum. Her türlü PR, issue veya yorumunuz çok kıymetlidir.  
👉 Bana ulaşmak için: [LinkedIn Profilim](https://www.linkedin.com/in/ismailyaltirik/)

---

## 💬 Teşekkürler

Projeyi incelediğiniz için teşekkür ederim. Eğer işinize yararsa, yıldız vermeyi unutmayın ⭐
