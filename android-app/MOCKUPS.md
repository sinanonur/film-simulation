# Beklenen Ekran Görüntüleri (Mockups)

Bu dosya, uygulamanın farklı aşamalarında nasıl görüneceğini gösterir.

## 📱 Current Version (v0.1.0-alpha)

### Welcome Screen (Şu Anki Durum)

```
╔════════════════════════════════════════╗
║  Status Bar                     🔋 📶  ║
╠════════════════════════════════════════╣
║                                        ║
║                                        ║
║                                        ║
║         📸 Film Simulation             ║
║                                        ║
║     Transform your photos with         ║
║     authentic film looks               ║
║                                        ║
║                                        ║
║          ┌──────────────────┐          ║
║          │   Get Started    │          ║
║          └──────────────────┘          ║
║                                        ║
║                                        ║
║                                        ║
╚════════════════════════════════════════╝

Material 3 Theme:
- Primary Color: #6650a4 (Purple)
- Dynamic Color: ✓ (Android 12+)
- Dark Mode: ✓ Supported
- Typography: Default Roboto
```

**Özellikler:**
- ✅ Material 3 Design
- ✅ Dynamic Color (Android 12+)
- ✅ Dark Mode desteği
- ✅ Responsive layout
- ✅ Welcome message
- ⏳ Get Started butonu (henüz işlevsel değil)

---

## 🎨 Planned Screens (Yakında)

### 1. Gallery Screen (v0.2.0)

```
╔════════════════════════════════════════╗
║  ← Gallery               🔍 ⋮          ║
╠════════════════════════════════════════╣
║                                        ║
║  ┌──────┬──────┬──────┐               ║
║  │ 📷   │ 📷   │ 📷   │               ║
║  │ IMG  │ IMG  │ IMG  │               ║
║  └──────┴──────┴──────┘               ║
║  ┌──────┬──────┬──────┐               ║
║  │ 📷   │ 📷   │ 📷   │               ║
║  │ IMG  │ IMG  │ IMG  │               ║
║  └──────┴──────┴──────┘               ║
║  ┌──────┬──────┬──────┐               ║
║  │ 📷   │ 📷   │ 📷   │               ║
║  │ IMG  │ IMG  │ IMG  │               ║
║  └──────┴──────┴──────┘               ║
║                                        ║
╠════════════════════════════════════════╣
║    [+] Select from Gallery             ║
╚════════════════════════════════════════╝
```

**Özellikler:**
- 3 sütunlu grid layout
- Lazy loading
- Image thumbnails
- Pull-to-refresh
- Select image action

---

### 2. Film Profile Selector (v0.2.0)

```
╔════════════════════════════════════════╗
║  ← Select Film Profile          ⋮      ║
╠════════════════════════════════════════╣
║                                        ║
║  ⭐ FAVORITES                          ║
║  ┌────────────────────────────┐       ║
║  │ 📸 Kodak Portra 400    ⭐  │       ║
║  │ Smooth, warm tones          │       ║
║  └────────────────────────────┘       ║
║                                        ║
║  🎬 ALL PROFILES                       ║
║  ┌────────────────────────────┐       ║
║  │ 📸 Fuji Velvia 50       ⭐  │       ║
║  │ Ultra-vivid colors          │       ║
║  └────────────────────────────┘       ║
║  ┌────────────────────────────┐       ║
║  │ 📸 Kodak Ektar 100      ☆  │       ║
║  │ Fine grain, vibrant         │       ║
║  └────────────────────────────┘       ║
║  ┌────────────────────────────┐       ║
║  │ 📸 Ilford HP5 Plus      ☆  │       ║
║  │ Classic B&W             │       ║
║  └────────────────────────────┘       ║
║                                        ║
╚════════════════════════════════════════╝
```

**Özellikler:**
- 12 film profili listesi
- Favorite marking (⭐)
- Profile açıklamaları
- Sectioned list (Favorites / All)
- Search bar (top)

---

### 3. Editor Screen (v0.3.0)

```
╔════════════════════════════════════════╗
║  ← Editor       Compare  Export   ⋮    ║
╠════════════════════════════════════════╣
║                                        ║
║   ┌──────────────────────────────┐    ║
║   │                              │    ║
║   │                              │    ║
║   │       [PHOTO PREVIEW]        │    ║
║   │                              │    ║
║   │                              │    ║
║   │                              │    ║
║   └──────────────────────────────┘    ║
║                                        ║
║   Currently: Kodak Portra 400          ║
║   ⚙️ Processing...                     ║
║                                        ║
╠════════════════════════════════════════╣
║  Film Profiles (swipe) →               ║
║  ┌────┐ ┌────┐ ┌────┐ ┌────┐         ║
║  │📸  │ │📸  │ │📸  │ │📸  │         ║
║  │P400│ │V50 │ │E100│ │S400│         ║
║  └────┘ └────┘ └────┘ └────┘         ║
╚════════════════════════════════════════╝
```

**Özellikler:**
- Fullscreen image preview
- Real-time filter preview (low res)
- Profile carousel at bottom
- Compare mode (before/after slider)
- Export button
- Processing indicator

---

### 4. Compare View (v0.3.0)

```
╔════════════════════════════════════════╗
║  ← Compare                        ✓    ║
╠════════════════════════════════════════╣
║                                        ║
║   ┌──────────────────────────────┐    ║
║   │  BEFORE     ║     AFTER       │    ║
║   │             ║                 │    ║
║   │  Original   ║  Kodak Portra   │    ║
║   │             ║                 │    ║
║   │             ║                 │    ║
║   └──────────────────────────────┘    ║
║          ←──────●──────→                ║
║         Drag to compare                ║
║                                        ║
║  ┌────────────┐  ┌────────────┐       ║
║  │  Original  │  │  Filtered  │       ║
║  │    Only    │  │    Only    │       ║
║  └────────────┘  └────────────┘       ║
║                                        ║
╚════════════════════════════════════════╝
```

**Özellikler:**
- Split screen comparison
- Draggable divider
- Original/Filtered toggle buttons
- Zoom in/out support

---

### 5. Settings Screen (v0.4.0)

```
╔════════════════════════════════════════╗
║  ← Settings                            ║
╠════════════════════════════════════════╣
║                                        ║
║  🎨 APPEARANCE                         ║
║  ┌────────────────────────────┐       ║
║  │ Theme                       │       ║
║  │ System Default          ▼   │       ║
║  └────────────────────────────┘       ║
║  ┌────────────────────────────┐       ║
║  │ Dynamic Color           ☑   │       ║
║  └────────────────────────────┘       ║
║                                        ║
║  ⚙️ PROCESSING                         ║
║  ┌────────────────────────────┐       ║
║  │ Quality                     │       ║
║  │ High                    ▼   │       ║
║  └────────────────────────────┘       ║
║  ┌────────────────────────────┐       ║
║  │ Use GPU Acceleration    ☑   │       ║
║  └────────────────────────────┘       ║
║                                        ║
║  ℹ️ ABOUT                              ║
║  Version 0.4.0                         ║
║  Made with ❤️ by Sinan Onur           ║
║                                        ║
╚════════════════════════════════════════╝
```

**Özellikler:**
- Theme selection (Light/Dark/System)
- Dynamic color toggle
- Processing quality settings
- GPU acceleration toggle
- About information

---

## 🎨 Visual Design System

### Color Palette

**Light Theme:**
```
Primary:   #6650a4 (Purple 40)
Secondary: #625b71 (Purple Grey 40)
Tertiary:  #7D5260 (Pink 40)
Background: #FFFBFE (White)
Surface:   #FFFBFE (White)
```

**Dark Theme:**
```
Primary:   #D0BCFF (Purple 80)
Secondary: #CCC2DC (Purple Grey 80)
Tertiary:  #EFB8C8 (Pink 80)
Background: #1C1B1F (Dark)
Surface:   #1C1B1F (Dark)
```

### Typography

```
Display Large:  Roboto 57sp
Display Medium: Roboto 45sp
Display Small:  Roboto 36sp

Headline Large:  Roboto 32sp
Headline Medium: Roboto 28sp
Headline Small:  Roboto 24sp

Title Large:  Roboto 22sp
Title Medium: Roboto 16sp
Title Small:  Roboto 14sp

Body Large:  Roboto 16sp
Body Medium: Roboto 14sp
Body Small:  Roboto 12sp

Label Large:  Roboto 14sp Bold
Label Medium: Roboto 12sp Bold
Label Small:  Roboto 11sp Bold
```

### Spacing

```
XXS: 4dp
XS:  8dp
S:   12dp
M:   16dp
L:   24dp
XL:  32dp
XXL: 48dp
```

### Components

**Button:**
```
Height: 40dp
Padding: 24dp horizontal, 10dp vertical
Corner Radius: 20dp (Pill shape)
Elevation: 0dp (Filled), 1dp (Outlined)
```

**Card:**
```
Corner Radius: 12dp
Elevation: 1dp
Padding: 16dp
```

**Image Preview:**
```
Aspect Ratio: Original (maintained)
Max Height: 60% screen
Corner Radius: 8dp
```

---

## 📐 Layout Specifications

### Grid System

```
Columns: 12 columns
Gutter: 16dp
Margin: 16dp (phone), 24dp (tablet)
```

### Responsive Breakpoints

```
Compact:  width < 600dp (Phone Portrait)
Medium:   600dp ≤ width < 840dp (Phone Landscape, Tablet Portrait)
Expanded: width ≥ 840dp (Tablet Landscape, Desktop)
```

---

## 🖼️ Asset Requirements

### App Icon
```
Launcher Icon: 512x512 (adaptive)
Notification Icon: 24x24 (monochrome)
Splash Screen: Dynamic (Material You)
```

### Film Profile Thumbnails
```
Size: 300x200 (3:2 aspect ratio)
Format: WebP or JPEG
Quality: 80%
```

### Sample Images
```
Test Images: 1920x1080 minimum
Formats: JPEG, PNG
Max Size: 10MB
```

---

## 🎬 Animation Specs

### Screen Transitions
```
Duration: 300ms
Easing: FastOutSlowIn
Type: Shared Element Transition
```

### Button Press
```
Duration: 100ms (press), 200ms (release)
Scale: 0.95x
```

### Image Loading
```
Placeholder: Shimmer effect
Fade In: 200ms
Error State: Red tint overlay
```

---

**Not:** Bu mockup'lar tasarım hedeflerini gösterir. Gerçek implementasyon sırasında ufak farklılıklar olabilir.

**Güncelleme Tarihi:** 2025-10-25
