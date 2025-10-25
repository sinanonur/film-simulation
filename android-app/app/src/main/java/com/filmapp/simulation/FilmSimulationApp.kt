package com.filmapp.simulation

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

/**
 * Main Application class for Film Simulation
 * Configured with Hilt for dependency injection
 */
@HiltAndroidApp
class FilmSimulationApp : Application() {

    override fun onCreate() {
        super.onCreate()
        // Initialize any app-wide components here
    }
}
