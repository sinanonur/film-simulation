package com.filmapp.simulation.data.parsers

import android.content.Context
import com.filmapp.simulation.data.dto.FilmProfileDto
import com.filmapp.simulation.domain.models.FilmProfile
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.serialization.json.Json
import java.io.IOException
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Parser for film profile JSON files
 */
@Singleton
class FilmProfileParser @Inject constructor(
    @ApplicationContext private val context: Context
) {

    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
    }

    /**
     * Loads all film profiles from assets
     *
     * @return Result containing list of profiles or error
     */
    suspend fun loadProfilesFromAssets(): Result<List<FilmProfile>> {
        return try {
            val jsonString = context.assets
                .open("film_profiles/12-film-profiles.json")
                .bufferedReader()
                .use { it.readText() }

            val profileMap = json.decodeFromString<Map<String, FilmProfileDto>>(jsonString)

            val profiles = profileMap.map { (name, dto) ->
                dto.toDomain(name)
            }

            // Validate all profiles
            val invalidProfiles = profiles.filterNot { it.isValid() }
            if (invalidProfiles.isNotEmpty()) {
                return Result.failure(
                    IllegalStateException(
                        "Invalid profiles: ${invalidProfiles.joinToString { it.name }}"
                    )
                )
            }

            Result.success(profiles)
        } catch (e: IOException) {
            Result.failure(e)
        } catch (e: Exception) {
            Result.failure(
                IllegalStateException("Failed to parse film profiles", e)
            )
        }
    }

    /**
     * Loads a single profile by name
     *
     * @param profileName Name of the profile to load
     * @return Result containing the profile or error
     */
    suspend fun loadProfile(profileName: String): Result<FilmProfile> {
        return loadProfilesFromAssets().mapCatching { profiles ->
            profiles.firstOrNull { it.name == profileName }
                ?: throw NoSuchElementException("Profile not found: $profileName")
        }
    }

    /**
     * Validates a profile's parameter ranges
     *
     * @param profile Profile to validate
     * @return List of validation errors (empty if valid)
     */
    fun validateProfile(profile: FilmProfile): List<String> {
        val errors = mutableListOf<String>()

        if (profile.contrast <= 0) {
            errors.add("Contrast must be > 0")
        }

        if (profile.saturation < 0) {
            errors.add("Saturation must be >= 0")
        }

        if (profile.grainAmount !in 0.0f..1.0f) {
            errors.add("Grain amount must be in [0.0, 1.0]")
        }

        if (profile.halationThreshold !in 0.0f..1.0f) {
            errors.add("Halation threshold must be in [0.0, 1.0]")
        }

        // Validate color curves
        listOf(
            "Red" to profile.colorCurves.red,
            "Green" to profile.colorCurves.green,
            "Blue" to profile.colorCurves.blue
        ).forEach { (channel, points) ->
            if (points.isEmpty()) {
                errors.add("$channel curve must have at least one point")
            }

            if (points.any { it.x !in 0.0f..1.0f || it.y !in 0.0f..1.0f }) {
                errors.add("$channel curve points must be in range [0.0, 1.0]")
            }

            // Check if points are sorted by x
            if (points.zipWithNext().any { (a, b) -> a.x >= b.x }) {
                errors.add("$channel curve points must be sorted by x value")
            }
        }

        return errors
    }
}
