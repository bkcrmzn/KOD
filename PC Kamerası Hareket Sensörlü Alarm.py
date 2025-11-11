
import cv2
import time
from playsound import playsound
import threading  # Ses çalma işlemini ayrı bir iş parçacığında yapacağız

ALARM_SOUND = "WhatsApp Ses 2025-11-04 saat 19.22.44_c49e739f.mp3"  # Yüklediğin ses dosyası
SON_CALMA_ZAMANI = 0
BEKLEME_SURESI = 1  # saniye (1 saniye aralıkla alarm çalacak)

# Alarmı arka planda çalan fonksiyon
def alarm_cal():
    threading.Thread(target=playsound, args=(ALARM_SOUND,), daemon=True).start()

# Kamerayı başlat
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("❌ Kamera açılamadı!")
    exit()

print("✅ Kamera açıldı.")
time.sleep(2)

ret, frame1 = camera.read()
ret, frame2 = camera.read()
if not ret:
    print("❌ Kamera görüntüsü alınamadı!")
    camera.release()
    exit()

print("🎥 Hareket algılama sistemi başlatıldı... (Çıkmak için 'q' tuşuna bas)")

while camera.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    hareket_var = False

    for contour in contours:
        if cv2.contourArea(contour) < 1500:
            continue
        hareket_var = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Hareket varsa ve 1 saniye geçtiyse alarm çal
    SON_CALMA_ZAMANI
    if hareket_var and (time.time() - SON_CALMA_ZAMANI > BEKLEME_SURESI):
        print("🚨 Hareket algılandı! Alarm çalıyor...")
        alarm_cal()
        SON_CALMA_ZAMANI = time.time()

    cv2.imshow("Hareket Algılama", frame1)
    frame1 = frame2
    ret, frame2 = camera.read()
    if not ret:
        break

    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("🛑 Sistem kapatılıyor...")
        break

camera.release()
cv2.destroyAllWindows()
