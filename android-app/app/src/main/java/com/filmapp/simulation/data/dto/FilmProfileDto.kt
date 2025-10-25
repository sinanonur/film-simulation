package com.filmapp.simulation.data.dto

import com.filmapp.simulation.domain.models.*
import kotlinx.serialization.Serializable

/**
 * Data Transfer Object for FilmProfile JSON deserialization
 */
@Serializable
data class FilmProfileDto(
    val color_curves: ColorCurvesDto,
    val contrast: Float,
    val saturation: Float,
    val chromatic_aberration: Float = 0f,
    val blur: Float = 0f,
    val base_color: List<Int>,
    val grain_amount: Float = 0f,
    val grain_size: Int = 1,
    val halation_strength: Float = 0f,
    val halation_threshold: Float = 0.7f,
    val vignette_strength: Float = 0f,
    val shadow_tint: List<Int> = listOf(0, 0, 0),
    val highlight_rolloff: Float = 0f,
    val color_bleed: Float = 0f
) {

    /**
     * Converts DTO to domain model
     *
     * @param name Profile name from JSON key
     * @return FilmProfile domain model
     */
    fun toDomain(name: String): FilmProfile {
        return FilmProfile(
            id = name.replace(" ", "_").lowercase(),
            name = name,
            colorCurves = color_curves.toDomain(),
            contrast = contrast,
            saturation = saturation,
            chromaticAberration = chromatic_aberration,
            blur = blur,
            baseColor = ColorRGB(
                r = base_color[0],
                g = base_color[1],
                b = base_color[2]
            ),
            grainAmount = grain_amount,
            grainSize = grain_size,
            halationStrength = halation_strength,
            halationThreshold = halation_threshold,
            vignetteStrength = vignette_strength,
            shadowTint = ColorRGB(
                r = shadow_tint[0],
                g = shadow_tint[1],
                b = shadow_tint[2]
            ),
            highlightRolloff = highlight_rolloff,
            colorBleed = color_bleed,
            isFavorite = false,
            isCustom = false
        )
    }
}

@Serializable
data class ColorCurvesDto(
    val R: CurveDataDto,
    val G: CurveDataDto,
    val B: CurveDataDto
) {

    fun toDomain(): ColorCurves {
        return ColorCurves(
            red = R.toPoints(),
            green = G.toPoints(),
            blue = B.toPoints()
        )
    }
}

@Serializable
data class CurveDataDto(
    val x: List<Float>,
    val y: List<Float>
) {

    /**
     * Converts curve data to list of CurvePoints
     */
    fun toPoints(): List<CurvePoint> {
        require(x.size == y.size) {
            "Curve x and y arrays must have the same length"
        }

        return x.zip(y) { xVal, yVal ->
            CurvePoint(xVal, yVal)
        }
    }
}
