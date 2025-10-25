# Android Studio İçin Çalıştırma Talimatları

Bu belge Android uygulamasını nasıl çalıştıracağınızı adım adım açıklar.

## 📋 Ön Gereksinimler

1. **Android Studio Hedgehog (2023.1.1) veya daha yeni**
   - Download: https://developer.android.com/studio

2. **JDK 17 veya daha yeni**
   - Android Studio ile birlikte gelir

3. **Android SDK**
   - Android Studio SDK Manager'dan yükleyin
   - Gerekli: SDK 34 (Android 14)

## 🚀 Adım Adım Çalıştırma

### 1. Projeyi Android Studio'da Açma

```bash
# Terminal'de proje dizinine gidin
cd film-simulation/android-app

# Android Studio'yu açın
# File → Open → "android-app" klasörünü seçin
```

**Alternatif:** Android Studio'yu başlatın ve "Open" butonuna tıklayın, ardından `android-app` klasörünü seçin.

### 2. Gradle Sync

Projeyi açtıktan sonra Android Studio otomatik olarak Gradle sync başlatacaktır.

Eğer başlatmazsa:
- **Tools → Android → Sync Project with Gradle Files**

İlk sync 5-10 dakika sürebilir (tüm dependencies indirilecek).

### 3. Emülatör Kurulumu

#### Mevcut Emülatör Varsa:
- Toolbar'da device selector'dan emülatörü seçin

#### Yeni Emülatör Oluşturma:
1. **Tools → Device Manager**
2. **Create Device**
3. Önerilen: **Pixel 5** veya **Pixel 7**
4. System Image: **Android 14.0 (API 34)** - UpsideDownCake
5. **Finish**

### 4. Uygulamayı Çalıştırma

**Yöntem 1: Run Button**
- Yeşil ▶️ butonuna tıklayın
- Veya `Shift + F10` kısayolu

**Yöntem 2: Terminal**
```bash
# Debug build
./gradlew installDebug

# Release build
./gradlew assembleRelease
```

### 5. İlk Çalıştırma Sonucu

Uygulama açıldığında şunları göreceksiniz:

```
┌──────────────────────────────┐
│     Film Simulation          │
│                              │
│  Transform your photos with  │
│  authentic film looks        │
│                              │
│      [Get Started]           │
│                              │
└──────────────────────────────┘
```

## 🔍 Sorun Giderme

### Gradle Sync Hatası

**Hata:** "Failed to sync Gradle"

**Çözüm:**
```bash
# Gradle cache'i temizle
./gradlew clean

# Yeniden sync
./gradlew build
```

### SDK Bulunamadı Hatası

**Hata:** "SDK location not found"

**Çözüm:**
1. **File → Project Structure → SDK Location**
2. Android SDK path'i belirleyin
3. Genellikle:
   - Windows: `C:\Users\[USERNAME]\AppData\Local\Android\Sdk`
   - macOS: `/Users/[USERNAME]/Library/Android/sdk`
   - Linux: `/home/[USERNAME]/Android/Sdk`

### Build Hatası: "Kotlin version mismatch"

**Çözüm:**
```kotlin
// build.gradle.kts dosyasında kotlin versiyonunu kontrol edin
// libs.versions.toml'da:
kotlin = "1.9.20"
```

### Emülatör Başlamıyor

**Çözüm:**
1. **Tools → AVD Manager**
2. Emülatörün yanındaki ▼ → **Cold Boot Now**
3. HAXM/Intel virtualization etkin mi kontrol edin

## 📱 Gerçek Cihazda Test

### Android Cihazı Hazırlama

1. **Developer Options'ı Aktifleştirin:**
   - Ayarlar → Telefon Hakkında
   - "Build Number"a 7 kez tıklayın

2. **USB Debugging'i Açın:**
   - Ayarlar → Developer Options
   - USB Debugging ✓

3. **Cihazı Bilgisayara Bağlayın:**
   - USB kablosu ile bağlayın
   - Cihazda "USB Debugging'e izin ver" onaylayın

4. **Android Studio'da Cihazı Seçin:**
   - Device selector'da gerçek cihazınız görünecektir
   - Run butonuna basın

## 🎨 Ekran Görüntüsü Alma

### Android Studio'dan:
1. Uygulamayı çalıştırın
2. **View → Tool Windows → Logcat**
3. Logcat toolbar'ında 📷 Camera icon
4. Ekran görüntüsü kaydedilir

### ADB ile:
```bash
# Ekran görüntüsü al
adb shell screencap /sdcard/screen.png

# Bilgisayara kopyala
adb pull /sdcard/screen.png

# Temizle
adb shell rm /sdcard/screen.png
```

### Emülatör ile:
- Emülatör yan panel → 📷 Camera butonu
- Veya emülatörü sağ tık → **Save Screenshot**

## 📊 Beklenen Çıktı

### İlk Çalıştırma (Current)
```
Screen: Welcome Screen
Components:
  - App Title: "Film Simulation"
  - Subtitle: "Transform your photos..."
  - Button: "Get Started"

Status: ✅ Çalışıyor
Features: Temel UI, Material 3 theme
```

### Sonraki Sürümler (Planned)
```
Screen 1: Gallery
  - Image grid from device
  - Select image

Screen 2: Film Profile List
  - 12 film profiles
  - Preview thumbnails

Screen 3: Editor
  - Image preview
  - Apply filters
  - Export
```

## 🐛 Debugging

### Logcat ile Log İzleme

Android Studio'da **Logcat** penceresini açın:
```
View → Tool Windows → Logcat
```

**Filter tags:**
- `FilmSimulation` - Uygulama logları
- `MainActivity` - Activity logları
- `FilmProfileParser` - Parser logları

### Breakpoint Koyma

1. Kod satırının sol tarafına tıklayın (kırmızı nokta)
2. **Debug** mode'da çalıştırın (🐛 icon)
3. Breakpoint'te durduğunda Variables penceresinde değerleri inceleyin

## 📝 Örnek Komutlar

```bash
# Build debug APK
./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk

# Run unit tests
./gradlew test

# Run instrumented tests
./gradlew connectedAndroidTest

# Check for updates
./gradlew dependencies

# Clean build
./gradlew clean build

# Install on device
./gradlew installDebug

# Uninstall
adb uninstall com.filmapp.simulation
```

## 🎯 Next Steps

Bu temel setup çalıştıktan sonra:

1. **UI Development** - Film profile list ekranı
2. **Image Picker** - Galeriden fotoğraf seçme
3. **Navigation** - Ekranlar arası geçiş
4. **GPU Pipeline** - OpenGL ES ile filtreleme

---

**Not:** Herhangi bir sorunla karşılaşırsanız [GitHub Issues](https://github.com/sinanonur/film-simulation/issues) üzerinden bildirebilirsiniz.
