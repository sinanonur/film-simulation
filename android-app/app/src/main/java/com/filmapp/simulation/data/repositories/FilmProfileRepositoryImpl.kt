package com.filmapp.simulation.data.repositories

import com.filmapp.simulation.data.parsers.FilmProfileParser
import com.filmapp.simulation.domain.models.FilmProfile
import com.filmapp.simulation.domain.repositories.FilmProfileRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Implementation of FilmProfileRepository
 *
 * Loads profiles from JSON assets and manages favorites in memory
 */
@Singleton
class FilmProfileRepositoryImpl @Inject constructor(
    private val parser: FilmProfileParser
) : FilmProfileRepository {

    private val _profiles = MutableStateFlow<Result<List<FilmProfile>>?>(null)

    /**
     * Loads profiles if not already loaded
     */
    private suspend fun ensureProfilesLoaded() {
        if (_profiles.value == null) {
            val result = parser.loadProfilesFromAssets()
            _profiles.value = result
        }
    }

    override fun getAllProfiles(): Flow<Result<List<FilmProfile>>> {
        return _profiles.map { cached ->
            cached ?: run {
                ensureProfilesLoaded()
                _profiles.value ?: Result.failure(
                    IllegalStateException("Failed to load profiles")
                )
            }
        }
    }

    override suspend fun getProfileById(id: String): Result<FilmProfile> {
        ensureProfilesLoaded()

        return _profiles.value?.mapCatching { profiles ->
            profiles.firstOrNull { it.id == id }
                ?: throw NoSuchElementException("Profile not found: $id")
        } ?: Result.failure(IllegalStateException("Profiles not loaded"))
    }

    override fun getFavoriteProfiles(): Flow<Result<List<FilmProfile>>> {
        return getAllProfiles().map { result ->
            result.map { profiles ->
                profiles.filter { it.isFavorite }
            }
        }
    }

    override suspend fun toggleFavorite(id: String): Result<FilmProfile> {
        ensureProfilesLoaded()

        return _profiles.value?.mapCatching { profiles ->
            val updatedProfiles = profiles.map { profile ->
                if (profile.id == id) {
                    profile.toggleFavorite()
                } else {
                    profile
                }
            }

            _profiles.value = Result.success(updatedProfiles)

            updatedProfiles.first { it.id == id }
        } ?: Result.failure(IllegalStateException("Profiles not loaded"))
    }

    override suspend fun searchProfiles(query: String): Result<List<FilmProfile>> {
        ensureProfilesLoaded()

        return _profiles.value?.mapCatching { profiles ->
            if (query.isBlank()) {
                profiles
            } else {
                profiles.filter { profile ->
                    profile.name.contains(query, ignoreCase = true)
                }
            }
        } ?: Result.failure(IllegalStateException("Profiles not loaded"))
    }
}
