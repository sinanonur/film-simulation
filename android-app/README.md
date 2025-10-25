# Film Simulation - Android App

Transform your photos with authentic film simulation profiles, bringing the classic look of iconic film stocks to your digital images.

## 📱 Project Status

**Current Version:** 0.1.0-alpha (Initial Setup)
**Development Phase:** Phase 1 - Project Setup ✅

### Completed
- ✅ Android project structure
- ✅ Gradle configuration with version catalog
- ✅ Clean Architecture module organization
- ✅ Domain models (FilmProfile, ProcessingParams, ImageMetadata)
- ✅ JSON parser for 12 film profiles
- ✅ Repository pattern implementation
- ✅ Hilt dependency injection setup
- ✅ Material 3 theme with dynamic color
- ✅ Basic MainActivity with Compose

### Next Steps
- ⏳ Film profile list screen
- ⏳ Image picker integration
- ⏳ GPU processing pipeline (OpenGL ES)
- ⏳ First filter implementation (LUT color grading)

## 🎬 Film Profiles Included

The app includes 12 authentic film simulation profiles:

1. **Kodak Portra 400** - Smooth skin tones, warm colors
2. **Fuji Velvia 50** - Ultra-vivid, high saturation
3. **Kodak Ektar 100** - Fine grain, vibrant colors
4. **Fuji Superia 400** - Balanced, slightly cool
5. **Ilford HP5 Plus** - Classic black & white
6. **Kodak Tri-X 400** - High contrast B&W
7. **Fuji Pro 400H** - Muted colors, soft tones
8. **Kodak Gold 200** - Warm, vintage look
9. **Fuji Provia 100F** - Neutral, accurate colors
10. **Kodak Ektachrome E100** - Slide film colors
11. **Lomography Color Negative 400** - Artistic, high contrast
12. **CineStill 800T** - Tungsten balance, halation glow

## 🛠 Tech Stack

### Core
- **Language:** Kotlin 1.9.20
- **Min SDK:** 24 (Android 7.0)
- **Target SDK:** 34 (Android 14)
- **Build System:** Gradle (Kotlin DSL)

### UI
- **Jetpack Compose** - Modern declarative UI
- **Material 3** - Latest design system with dynamic color
- **Navigation Compose** - Type-safe navigation

### Architecture
- **Clean Architecture** - Separation of concerns
- **MVVM** - ViewModel + StateFlow
- **Hilt** - Dependency injection
- **Kotlin Coroutines** - Asynchronous programming
- **Flow** - Reactive streams

### Image Processing (Planned)
- **OpenGL ES 3.0+** - GPU-accelerated processing
- **Coil** - Image loading
- **Custom Filters** - Film-specific effects

### Data
- **Room** - Local database (for favorites, settings)
- **DataStore** - Preferences
- **Kotlinx Serialization** - JSON parsing

### Testing
- **JUnit 4** - Unit testing
- **MockK** - Mocking framework
- **Turbine** - Flow testing
- **Compose UI Test** - UI testing

## 📁 Project Structure

```
app/
├── src/main/java/com/filmapp/simulation/
│   ├── presentation/          # UI Layer
│   │   ├── ui/
│   │   │   ├── screens/      # Compose screens
│   │   │   ├── components/   # Reusable UI components
│   │   │   └── theme/        # Material 3 theme
│   │   └── viewmodels/       # ViewModels
│   │
│   ├── domain/                # Business Logic Layer
│   │   ├── models/           # Data models
│   │   ├── usecases/         # Use cases
│   │   └── repositories/     # Repository interfaces
│   │
│   ├── data/                  # Data Layer
│   │   ├── repositories/     # Repository implementations
│   │   ├── dto/              # Data Transfer Objects
│   │   ├── parsers/          # JSON parsers
│   │   └── local/            # Local storage
│   │
│   ├── processing/            # Image Processing Engine
│   │   ├── engine/           # Core engine
│   │   ├── filters/          # Individual filters
│   │   └── gpu/              # OpenGL/GPU code
│   │
│   ├── di/                    # Dependency Injection
│   └── utils/                 # Utilities
│
└── src/main/assets/
    └── film_profiles/         # JSON film profiles
```

## 🚀 Getting Started

### Prerequisites

- **Android Studio** Hedgehog (2023.1.1) or later
- **JDK** 17 or later
- **Android SDK** with SDK 34
- **Gradle** 8.2 or later (included in wrapper)

### Setup

1. **Clone the repository:**
   ```bash
   cd film-simulation
   cd android-app
   ```

2. **Open in Android Studio:**
   - File → Open → Select `android-app` directory
   - Wait for Gradle sync to complete

3. **Build the project:**
   ```bash
   ./gradlew build
   ```

4. **Run on device/emulator:**
   - Select a device with API 24+
   - Click Run (or Shift+F10)

### Running Tests

```bash
# Unit tests
./gradlew test

# Instrumented tests
./gradlew connectedAndroidTest

# Test coverage
./gradlew testDebugUnitTestCoverage
```

## 📦 Dependencies

See [`gradle/libs.versions.toml`](gradle/libs.versions.toml) for complete dependency list.

Key dependencies:
- Jetpack Compose BOM: 2024.01.00
- Material 3
- Hilt: 2.50
- Coroutines: 1.7.3
- Room: 2.6.1
- Coil: 2.5.0

## 🎯 Development Roadmap

### Phase 1: Foundation (Week 1) ✅
- [x] Project setup
- [x] Dependencies configuration
- [x] Domain models
- [x] JSON parser
- [x] Repository pattern
- [x] Basic UI

### Phase 2: UI Development (Week 2-3)
- [ ] Film profile list screen
- [ ] Image picker integration
- [ ] Basic image display
- [ ] Navigation setup

### Phase 3: GPU Pipeline (Week 3-4)
- [ ] OpenGL ES context
- [ ] Shader infrastructure
- [ ] Texture management
- [ ] First filter (LUT color grading)

### Phase 4: Core Filters (Week 4-6)
- [ ] Contrast & Saturation
- [ ] Vignette
- [ ] Film grain
- [ ] Halation
- [ ] Chromatic aberration

### Phase 5: Polish (Week 7-8)
- [ ] Export functionality
- [ ] Before/after comparison
- [ ] Settings screen
- [ ] Performance optimization

## 📖 Documentation

- [Implementation Tracker](../IMPLEMENTATION_TRACKER.md) - Detailed task breakdown
- [Android Planning](../ANDROID_PLANNING.md) - Technical planning and architecture
- [Original Python Implementation](../README.md) - Reference implementation

## 🧪 Testing Strategy

### Unit Tests
- Domain models validation
- Use cases business logic
- Repository operations
- Parser functionality

### Integration Tests
- Database operations
- File I/O
- Navigation flows

### UI Tests
- Screen layouts
- User interactions
- State changes

### Performance Tests
- Image processing speed
- Memory usage
- GPU utilization

## 🐛 Known Issues

None yet - project just started! 🎉

## 📄 License

[MIT License](https://opensource.org/licenses/MIT)

## 👤 Author

Sinan Onur Altınuç

---

**Note:** This is an active development project. Features and APIs may change.

For detailed planning and progress tracking, see [IMPLEMENTATION_TRACKER.md](../IMPLEMENTATION_TRACKER.md).
