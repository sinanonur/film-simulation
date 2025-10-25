package com.filmapp.simulation.domain.repositories

import com.filmapp.simulation.domain.models.FilmProfile
import kotlinx.coroutines.flow.Flow

/**
 * Repository interface for film profiles
 */
interface FilmProfileRepository {

    /**
     * Gets all available film profiles
     *
     * @return Flow of profile list
     */
    fun getAllProfiles(): Flow<Result<List<FilmProfile>>>

    /**
     * Gets a single profile by ID
     *
     * @param id Profile ID
     * @return Result containing profile or error
     */
    suspend fun getProfileById(id: String): Result<FilmProfile>

    /**
     * Gets favorite profiles
     *
     * @return Flow of favorite profiles
     */
    fun getFavoriteProfiles(): Flow<Result<List<FilmProfile>>>

    /**
     * Toggles favorite status for a profile
     *
     * @param id Profile ID
     * @return Result containing updated profile
     */
    suspend fun toggleFavorite(id: String): Result<FilmProfile>

    /**
     * Searches profiles by name
     *
     * @param query Search query
     * @return Result containing matching profiles
     */
    suspend fun searchProfiles(query: String): Result<List<FilmProfile>>
}
