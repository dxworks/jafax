package jafax.it.summary

import kotlinx.serialization.json.Json
import org.vladg.jafax.summary.JafaxSummaryData
import org.vladg.jafax.summary.JafaxSummaryService
import java.nio.file.Files
import kotlin.test.Test
import kotlin.test.assertTrue

class SummaryIT {

    private val json = Json { ignoreUnknownKeys = true }

    @Test
    fun `should write summary snapshot data file`() {
        val resultsPath = Files.createTempDirectory("jafax-summary-data-")
        try {
            val summaryData = JafaxSummaryData(
                projectName = "demo",
                onlyLayout = false,
                filesCount = 12,
                topLevelClassesCount = 5,
                layoutObjectsCount = 37,
                internalRelationsCount = 14,
                externalRelationsCount = 6,
                metricsCount = 5,
                importsCount = 21,
                interfacesCount = 2,
                abstractClassesCount = 1,
            )
            val summaryDataPath = resultsPath.resolve("jafax-summary-data.json")
            JafaxSummaryService.writeSummaryData(resultsPath, summaryData)

            assertTrue(Files.exists(summaryDataPath))
            assertTrue(summaryData.metricsCount > 0)

            val persisted = json.decodeFromString(JafaxSummaryData.serializer(), Files.readString(summaryDataPath))
            assertTrue(persisted.topLevelClassesCount > 0)
            assertTrue(persisted.internalRelationsCount > 0)
        } finally {
            resultsPath.toFile().deleteRecursively()
        }
    }

}
