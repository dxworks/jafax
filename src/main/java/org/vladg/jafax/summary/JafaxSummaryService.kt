package org.vladg.jafax.summary

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.nio.file.Files
import java.nio.file.Path
import java.time.Instant

private const val SUCCESS_STATUS = "success"

private const val SUMMARY_DATA_FILE_NAME = "jafax-summary-data.json"

private val format = Json {
    prettyPrint = true
    ignoreUnknownKeys = true
    encodeDefaults = true
}

@Serializable
data class JafaxSummaryData(
    val status: String = SUCCESS_STATUS,
    val projectName: String,
    val onlyLayout: Boolean,
    val sourceLinesCount: Int,
    val filesCount: Int,
    val topLevelClassesCount: Int,
    val layoutObjectsCount: Int,
    val internalRelationsCount: Int,
    val externalRelationsCount: Int,
    val metricsCount: Int,
    val importsCount: Int,
    val interfacesCount: Int,
    val abstractClassesCount: Int,
    val generatedAt: String = Instant.now().toString(),
)

object JafaxSummaryService {

    fun writeSummaryData(resultsPath: Path, data: JafaxSummaryData): Path {
        Files.createDirectories(resultsPath)
        val dataPath = resultsPath.resolve(SUMMARY_DATA_FILE_NAME)
        Files.writeString(dataPath, format.encodeToString(JafaxSummaryData.serializer(), data))
        return dataPath
    }
}
