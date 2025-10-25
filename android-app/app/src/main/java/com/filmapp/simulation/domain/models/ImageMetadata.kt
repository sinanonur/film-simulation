package com.filmapp.simulation.domain.models

import android.net.Uri
import java.util.Date

/**
 * Metadata for an image
 *
 * @property uri Original image URI
 * @property width Image width in pixels
 * @property height Image height in pixels
 * @property fileSize File size in bytes
 * @property mimeType MIME type (e.g., "image/jpeg")
 * @property dateAdded Date when image was added
 * @property orientation EXIF orientation
 */
data class ImageMetadata(
    val uri: Uri,
    val width: Int,
    val height: Int,
    val fileSize: Long,
    val mimeType: String,
    val dateAdded: Date,
    val orientation: Int = 0
) {

    /**
     * Aspect ratio (width / height)
     */
    val aspectRatio: Float
        get() = width.toFloat() / height.toFloat()

    /**
     * Total pixels
     */
    val megapixels: Float
        get() = (width * height) / 1_000_000f

    /**
     * Human-readable file size
     */
    val fileSizeFormatted: String
        get() = when {
            fileSize < 1024 -> "$fileSize B"
            fileSize < 1024 * 1024 -> "${fileSize / 1024} KB"
            else -> "%.1f MB".format(fileSize / (1024f * 1024f))
        }

    /**
     * Image resolution string
     */
    val resolutionString: String
        get() = "${width}x${height}"
}
