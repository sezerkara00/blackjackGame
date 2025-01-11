import random
import time

# Kartlar ve destesi
cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
deste = cards * 3

def deste_karistir(deste):
    random.shuffle(deste)
    return deste

def kart_degeri(kart, eldeki_toplam, as_sayisi):
    """
    Kart değeri belirler. As'ı 11 veya 1 olarak değerlendirir.
    """
    if kart in ['J', 'Q', 'K']:
        return 10, as_sayisi
    elif kart == 'A':
        as_sayisi += 1
        return 11, as_sayisi  # As başlangıçta 11 olarak değerlendirilir
    else:
        return kart, as_sayisi

def as_dinamik_kontrol(toplam, as_sayisi):
    """
    Eğer toplam 21'i aşıyorsa, As değerini 11'den 1'e düşürerek toplamı günceller.
    """
    while toplam > 21 and as_sayisi > 0:
        toplam -= 10  # Bir As'ın değeri 11'den 1'e düşürülür
        as_sayisi -= 1
    return toplam, as_sayisi

def kartlari_goster(kartlar):
    """
    Kartları gösterir, As'ları (A) belirgin şekilde vurgular.
    """
    return ", ".join([f'{kart}(1/11)' if kart == 'A' else str(kart) for kart in kartlar])

def oyun():
    oyuncu_bakiye = 100  # Başlangıç bakiyesi
    while True:
        print(f"Mevcut bakiyeniz: {oyuncu_bakiye} TL")
        katilim_ucreti = int(input("Oyuna katılmak için ücret girin: "))

        if katilim_ucreti > oyuncu_bakiye:
            print("Yeterli bakiyeniz yok!")
            continue

        oyuncu_bakiye -= katilim_ucreti  # Katılım ücreti bakiyeden düşülür
        print(f"\nOyuna {katilim_ucreti} TL ile katıldınız.")

        deste_karistir(deste)
        oyuncunun_kartlari = []
        kurpiye_kartlari = []
        oyuncu_toplam = 0
        kurpiye_toplam = 0
        as_sayisi_oyuncu = 0
        as_sayisi_kurpiye = 0

        # Oyuncunun ve kurpiyenin kartları çekilir
        print("\nOyuncu kartlarını çekiyor...")
        for i in range(2):  # Oyuncuya 2 kart
            kart, as_sayisi_oyuncu = kart_degeri(deste.pop(), oyuncu_toplam, as_sayisi_oyuncu)
            oyuncunun_kartlari.append(kart)
            oyuncu_toplam += kart

            kart, as_sayisi_kurpiye = kart_degeri(deste.pop(), kurpiye_toplam, as_sayisi_kurpiye)
            kurpiye_kartlari.append(kart)
            kurpiye_toplam += kart

        # As dinamik kontrolü uygulanıyor
        oyuncu_toplam, as_sayisi_oyuncu = as_dinamik_kontrol(oyuncu_toplam, as_sayisi_oyuncu)
        kurpiye_toplam, as_sayisi_kurpiye = as_dinamik_kontrol(kurpiye_toplam, as_sayisi_kurpiye)

        # Kartlar gösterilir
        print(f"Kurpiyenin skoru: {kurpiye_kartlari[0]} (diğer kart gizli)")
        print(f"Oyuncunun skoru: {oyuncu_toplam}")
        print(f"Oyuncunun kartları: {kartlari_goster(oyuncunun_kartlari)}")

        # Oyuncunun kart çekme kısmı
        while oyuncu_toplam < 21:
            print("\nOyuncu kart çekmek istiyor mu? (e/h) veya double seçeneği (d)?")
            cevap = input()
            if cevap == "e":
                time.sleep(2)
                kart, as_sayisi_oyuncu = kart_degeri(deste.pop(), oyuncu_toplam, as_sayisi_oyuncu)
                oyuncunun_kartlari.append(kart)
                oyuncu_toplam += kart
                oyuncu_toplam, as_sayisi_oyuncu = as_dinamik_kontrol(oyuncu_toplam, as_sayisi_oyuncu)
                print(f"Oyuncunun kartı: {kart}, Skoru: {oyuncu_toplam}")
                if oyuncu_toplam > 21:
                    print("Çok fazla skor! Oyuncu kaybetti.")
                    break
            elif cevap == "d":
                if oyuncu_bakiye < katilim_ucreti:
                    print("Double yapmak için yeterli bakiyeniz yok!")
                    continue
                oyuncu_bakiye -= katilim_ucreti
                katilim_ucreti *= 2
                print("Double seçildi! Sadece bir kart çekebilirsiniz.")
                time.sleep(2)
                kart, as_sayisi_oyuncu = kart_degeri(deste.pop(), oyuncu_toplam, as_sayisi_oyuncu)
                oyuncunun_kartlari.append(kart)
                oyuncu_toplam += kart
                oyuncu_toplam, as_sayisi_oyuncu = as_dinamik_kontrol(oyuncu_toplam, as_sayisi_oyuncu)
                print(f"Oyuncunun kartı: {kart}, Skoru: {oyuncu_toplam}")
                break
            else:
                break

        # Kurpiyenin kart çekme kısmı
        print(f"Kurpiyenin skoru: {kurpiye_toplam}")
        while kurpiye_toplam < 17:
            print("\nKurpiyer kart çekiyor...")
            time.sleep(2)
            kart, as_sayisi_kurpiye = kart_degeri(deste.pop(), kurpiye_toplam, as_sayisi_kurpiye)
            kurpiye_kartlari.append(kart)
            kurpiye_toplam += kart
            kurpiye_toplam, as_sayisi_kurpiye = as_dinamik_kontrol(kurpiye_toplam, as_sayisi_kurpiye)
            print(f"Kurpiyerin kartı: {kart}, Skoru: {kurpiye_toplam}")

        # Kazananı belirleme
        if oyuncu_toplam > 21:
            print("Kurpiyer kazandı!")
            kazanan = "Kurpiyer"
        elif kurpiye_toplam > 21 or oyuncu_toplam > kurpiye_toplam:
            print("Oyuncu kazandı!")
            oyuncu_bakiye += katilim_ucreti * 2
            kazanan = "Oyuncu"
        elif oyuncu_toplam == kurpiye_toplam:
            print("Berabere!")
            oyuncu_bakiye += katilim_ucreti
            kazanan = "Berabere"
        else:
            print("Kurpiyer kazandı!")
            kazanan = "Kurpiyer"

        # Oyun sonuçları
        print("\nOyun sonuçları:")
        print(f"Oyuncunun kartları: {kartlari_goster(oyuncunun_kartlari)}")
        print(f"Kurpiyenin kartları: {kartlari_goster(kurpiye_kartlari)}")
        print(f"Oyuncunun skoru: {oyuncu_toplam}")
        print(f"Kurpiyenin skoru: {kurpiye_toplam}")
        print(f"Kazanan: {kazanan}")
        print(f"Yeni bakiyeniz: {oyuncu_bakiye} TL")

        print("Oyuna devam etmek istiyor musunuz? (e/h)")
        cevap = input()
        if cevap == "e":
            print("\n\n\n")
            continue
        else:
            break

# Oyunu başlat
oyun()
