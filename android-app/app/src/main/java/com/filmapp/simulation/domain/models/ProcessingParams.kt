package com.filmapp.simulation.domain.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

/**
 * Parameters for image processing
 *
 * @property colorTemp Color temperature in Kelvin (2000-10000, neutral=6500)
 * @property crossProcess Apply cross-processing effect
 * @property quality Processing quality level
 */
@Parcelize
data class ProcessingParams(
    val colorTemp: Int = 6500,
    val crossProcess: Boolean = false,
    val quality: ProcessingQuality = ProcessingQuality.HIGH
) : Parcelable {

    init {
        require(colorTemp in 2000..10000) {
            "Color temperature must be in range [2000, 10000]"
        }
    }

    companion object {
        /**
         * Default processing parameters
         */
        val DEFAULT = ProcessingParams()

        /**
         * Parameters optimized for preview
         */
        val PREVIEW = ProcessingParams(quality = ProcessingQuality.PREVIEW)

        /**
         * Parameters optimized for export
         */
        val EXPORT = ProcessingParams(quality = ProcessingQuality.ULTRA)
    }
}

/**
 * Processing quality levels
 */
@Parcelize
enum class ProcessingQuality : Parcelable {
    /**
     * Fast preview - lower resolution, simplified effects
     * Target: <30ms
     */
    PREVIEW,

    /**
     * Balanced quality - good for interactive preview
     * Target: <50ms
     */
    MEDIUM,

    /**
     * High quality - for final preview before export
     * Target: <100ms
     */
    HIGH,

    /**
     * Ultra quality - maximum quality for export
     * No time constraint
     */
    ULTRA;

    /**
     * Resolution scale factor for this quality level
     */
    val scaleFactor: Float
        get() = when (this) {
            PREVIEW -> 0.25f // 1/4 resolution
            MEDIUM -> 0.5f   // 1/2 resolution
            HIGH -> 0.75f    // 3/4 resolution
            ULTRA -> 1.0f    // Full resolution
        }

    /**
     * LUT size for color grading
     */
    val lutSize: Int
        get() = when (this) {
            PREVIEW -> 32  // 32x32x32
            MEDIUM -> 48   // 48x48x48
            HIGH -> 64     // 64x64x64
            ULTRA -> 64    // 64x64x64
        }
}
