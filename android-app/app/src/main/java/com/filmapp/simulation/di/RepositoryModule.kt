package com.filmapp.simulation.di

import com.filmapp.simulation.data.repositories.FilmProfileRepositoryImpl
import com.filmapp.simulation.domain.repositories.FilmProfileRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

/**
 * Hilt module for repository dependencies
 */
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindFilmProfileRepository(
        impl: FilmProfileRepositoryImpl
    ): FilmProfileRepository
}
