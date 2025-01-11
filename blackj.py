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
        # Eğer toplam 11'e eşitse, As 11 olarak sayılır. Aksi takdirde 1.
        if eldeki_toplam + 11 <= 21:
            return 11, as_sayisi
        else:
            return 1, as_sayisi
    else:
        return kart, as_sayisi

def kartlari_goster(kartlar, as_sayisi):
    """
    Kartları ve As'ları gösterir, As'ın 11 veya 1 olarak sayılmasını parantez içinde gösterir.
    """
    kartlar_str = []
    for kart in kartlar:
        if kart == 'A':
            kartlar_str.append(f'{kart}(1/11)')
        else:
            kartlar_str.append(str(kart))
    return ", ".join(kartlar_str)

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

        # Oyuncunun ve kurpiyenin kartları çekilir (Gecikmeli gösterim)
        print("\nOyuncu kartlarını çekiyor...")
        for i in range(2):  # Oyuncuya 2 kart
            kart, as_sayisi_oyuncu = kart_degeri(deste.pop(), oyuncu_toplam, as_sayisi_oyuncu)
            oyuncunun_kartlari.append(kart)
            oyuncu_toplam += kart

            time.sleep(1) 
            kart, as_sayisi_kurpiye = kart_degeri(deste.pop(), kurpiye_toplam, as_sayisi_kurpiye)
            kurpiye_kartlari.append(kart)
            kurpiye_toplam += kart  # Her kart çekişinde 1 saniye bekleyin
            time.sleep(1) 

        # Kartlar gösterilir
        print(f"Kurpiyenin skoru: {kurpiye_kartlari[0]} (diğer kart gizli)")
        print(f"Oyuncunun skoru: {oyuncu_toplam}")
        print(f"Oyuncunun kartları: {kartlari_goster(oyuncunun_kartlari, as_sayisi_oyuncu)}")

        # Oyuncunun kart çekme kısmı
        while oyuncu_toplam < 21:
            print("\nOyuncu kart çekmek istiyor mu? (e/h) veya double seçeneği (d)?")
            cevap = input()
            if cevap == "e":
                kart, as_sayisi_oyuncu = kart_degeri(deste.pop(), oyuncu_toplam, as_sayisi_oyuncu)
                oyuncunun_kartlari.append(kart)
                oyuncu_toplam += kart
                print(f"Oyuncunun kartı: {kart}, Skoru: {oyuncu_toplam}")
                time.sleep(1)  # Kart çekişi gecikmeli göster
                if oyuncu_toplam > 21:
                    print("Cok Fazla Skor! Oyuncu kaybetti.")
                    break
            elif cevap == "d":
                # Double seçildiğinde oyuncu sadece 1 kart çeker ve katılım ücretini iki katına çıkarır
                if oyuncu_bakiye < katilim_ucreti:
                    print("Double yapmak için yeterli bakiyeniz yok! Lütfen başka bir seçenek seçin.")
                    continue  # Double yapılacaksa seçenek yeniden gösterilecek
                oyuncu_bakiye -= katilim_ucreti  # Katılım ücretini iki katına çıkarıyoruz
                print("Double seçildi! Sadece bir kart çekebilirsiniz.")
                time.sleep(1)

                kart, as_sayisi_oyuncu = kart_degeri(deste.pop(), oyuncu_toplam, as_sayisi_oyuncu)
                oyuncunun_kartlari.append(kart)
                oyuncu_toplam += kart
                print(f"Oyuncunun kartı: {kart}, Skoru: {oyuncu_toplam}")
                time.sleep(1)  # Kart çekişi gecikmeli göster
                break  # Double'da bir kart çektikten sonra oyuncu daha fazla kart çekemez
            else:
                break

        # Kurpiyenin kart çekme kısmı (Burada delay ekleniyor)
        print(f"Kurpiyenin skoru: {kurpiye_toplam}")
        while kurpiye_toplam < 17:
            print("\nKurpiyer kart çekiyor...")
            time.sleep(2)  # 2 saniye gecikme ekleniyor
            kart, as_sayisi_kurpiye = kart_degeri(deste.pop(), kurpiye_toplam, as_sayisi_kurpiye)
            kurpiye_kartlari.append(kart)
            kurpiye_toplam += kart
            print(f"Kurpiyerin kartı: {kart}, Skoru: {kurpiye_toplam}")
            time.sleep(1)  # Kart çekişi gecikmeli göster

        # Kazananı belirleme
        if oyuncu_toplam > 21:
            print("Kurpiyer kazandı!")
            kazanan = "Kurpiyer"
        elif kurpiye_toplam == oyuncu_toplam:
            print("Berabere!")
            kazanan = "Berabere"
        elif oyuncu_toplam == 21:
            print("Oyuncu BlackJack yaptı, kazandı!")
            oyuncu_bakiye += katilim_ucreti * 1.5  # Kazanan oyuncuya ödül eklenir
            kazanan = "Oyuncu"
        elif kurpiye_toplam == 21:
            print("Kurpiyer BlackJack yaptı, kazandı!")
            kazanan = "Kurpiyer"
        elif oyuncu_toplam <= 21 and kurpiye_toplam > 21:
            print("Oyuncu kazandı!")
            oyuncu_bakiye += katilim_ucreti * 2  # Kazanan oyuncuya ödül eklenir
            kazanan = "Oyuncu"
        elif kurpiye_toplam > oyuncu_toplam:
            print("Kurpiyer kazandı!")
            kazanan = "Kurpiyer"
        elif kurpiye_toplam < oyuncu_toplam:
            print("Oyuncu kazandı!")
            oyuncu_bakiye += katilim_ucreti * 2  # Kazanan oyuncuya ödül eklenir
            kazanan = "Oyuncu"

        # Oyun sonuçları
        print("Oyuna devam etmek istiyor musunuz? (e/h)")
        cevap = input()
        if cevap == "e":
            print("\n\n\n")
            print("Oyun sonuçları:")
            print(f"Oyuncunun kartları: {kartlari_goster(oyuncunun_kartlari, as_sayisi_oyuncu)}")
            print(f"Kurpiyenin kartları: {kartlari_goster(kurpiye_kartlari, as_sayisi_kurpiye)}")
            print(f"Oyuncunun skoru: {oyuncu_toplam}")
            print(f"Kurpiyenin skoru: {kurpiye_toplam}")
            print(f"Kazanan: {kazanan}")
            print(f"Yeni bakiyeniz: {oyuncu_bakiye} TL")
            print("\n\n\n")
            oyuncunun_kartlari = []
            kurpiye_kartlari = []
            deste_karistir(deste)
            continue
        else:
            break

# Oyunu başlat
oyun()
