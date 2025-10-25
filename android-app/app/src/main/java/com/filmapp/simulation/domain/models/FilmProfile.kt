package com.filmapp.simulation.domain.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize
import kotlinx.serialization.Serializable

/**
 * Represents a film simulation profile with all processing parameters
 *
 * @property id Unique identifier for the profile
 * @property name Display name (e.g., "Kodak Portra 400")
 * @property colorCurves RGB color curves for tone mapping
 * @property contrast Contrast adjustment multiplier (1.0 = no change)
 * @property saturation Saturation multiplier (0.0 = grayscale, 1.0 = original)
 * @property chromaticAberration Chromatic aberration strength
 * @property blur Gaussian blur radius
 * @property baseColor Base color tint (RGB 0-255)
 * @property grainAmount Film grain intensity (0.0-1.0)
 * @property grainSize Grain particle size
 * @property halationStrength Halation (glow) effect strength
 * @property halationThreshold Brightness threshold for halation
 * @property vignetteStrength Vignette darkening strength
 * @property shadowTint Color tint in shadow areas (RGB 0-255)
 * @property highlightRolloff Highlight compression strength
 * @property colorBleed Inter-channel color bleeding strength
 */
@Parcelize
@Serializable
data class FilmProfile(
    val id: String,
    val name: String,
    val colorCurves: ColorCurves,
    val contrast: Float,
    val saturation: Float,
    val chromaticAberration: Float,
    val blur: Float,
    val baseColor: ColorRGB,
    val grainAmount: Float,
    val grainSize: Int,
    val halationStrength: Float = 0.0f,
    val halationThreshold: Float = 0.7f,
    val vignetteStrength: Float = 0.0f,
    val shadowTint: ColorRGB = ColorRGB(0, 0, 0),
    val highlightRolloff: Float = 0.0f,
    val colorBleed: Float = 0.0f,
    val isFavorite: Boolean = false,
    val isCustom: Boolean = false
) : Parcelable {

    /**
     * Returns a copy with the favorite flag toggled
     */
    fun toggleFavorite() = copy(isFavorite = !isFavorite)

    /**
     * Validates that all parameters are within acceptable ranges
     */
    fun isValid(): Boolean {
        return contrast > 0 &&
                saturation >= 0 &&
                chromaticAberration >= 0 &&
                blur >= 0 &&
                grainAmount in 0.0f..1.0f &&
                grainSize > 0 &&
                halationStrength >= 0 &&
                halationThreshold in 0.0f..1.0f &&
                vignetteStrength >= 0 &&
                highlightRolloff >= 0 &&
                colorBleed >= 0
    }
}

/**
 * Color curves for red, green, and blue channels
 */
@Parcelize
@Serializable
data class ColorCurves(
    val red: List<CurvePoint>,
    val green: List<CurvePoint>,
    val blue: List<CurvePoint>
) : Parcelable {

    init {
        require(red.isNotEmpty()) { "Red curve must have at least one point" }
        require(green.isNotEmpty()) { "Green curve must have at least one point" }
        require(blue.isNotEmpty()) { "Blue curve must have at least one point" }
    }

    /**
     * Returns true if all curves are identity curves (no transformation)
     */
    fun isIdentity(): Boolean {
        return red.all { it.x == it.y } &&
                green.all { it.x == it.y } &&
                blue.all { it.x == it.y }
    }
}

/**
 * A point on a color curve
 *
 * @property x Input value (0.0-1.0)
 * @property y Output value (0.0-1.0)
 */
@Parcelize
@Serializable
data class CurvePoint(
    val x: Float,
    val y: Float
) : Parcelable {

    init {
        require(x in 0.0f..1.0f) { "x must be in range [0.0, 1.0]" }
        require(y in 0.0f..1.0f) { "y must be in range [0.0, 1.0]" }
    }
}

/**
 * RGB color representation (0-255 range)
 */
@Parcelize
@Serializable
data class ColorRGB(
    val r: Int,
    val g: Int,
    val b: Int
) : Parcelable {

    init {
        require(r in 0..255) { "Red must be in range [0, 255]" }
        require(g in 0..255) { "Green must be in range [0, 255]" }
        require(b in 0..255) { "Blue must be in range [0, 255]" }
    }

    /**
     * Converts to normalized float values (0.0-1.0)
     */
    fun toFloatArray(): FloatArray {
        return floatArrayOf(r / 255f, g / 255f, b / 255f)
    }

    companion object {
        val WHITE = ColorRGB(255, 255, 255)
        val BLACK = ColorRGB(0, 0, 0)

        /**
         * Creates ColorRGB from normalized float values
         */
        fun fromFloats(r: Float, g: Float, b: Float): ColorRGB {
            return ColorRGB(
                (r * 255).toInt().coerceIn(0, 255),
                (g * 255).toInt().coerceIn(0, 255),
                (b * 255).toInt().coerceIn(0, 255)
            )
        }
    }
}
