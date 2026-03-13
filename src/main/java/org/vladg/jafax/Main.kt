package org.vladg.jafax

import org.vladg.jafax.experimental.InterfaceComputer
import org.vladg.jafax.imports.ImportsComputer
import org.vladg.jafax.io.scanner.ProjectScanner
import org.vladg.jafax.metrics.MetricsComputer
import org.vladg.jafax.repository.ClassRepository
import org.vladg.jafax.repository.CommonRepository
import org.vladg.jafax.repository.FileRepository
import org.vladg.jafax.relations.ExternalRelationsComputer
import org.vladg.jafax.relations.RelationsComputer
import org.vladg.jafax.summary.JafaxSummaryData
import org.vladg.jafax.summary.JafaxSummaryService
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.io.path.ExperimentalPathApi
import kotlin.io.path.name
import kotlin.system.exitProcess

@ExperimentalPathApi
fun main(args: Array<String>) {
    val exitCode = execute(args)
    if (exitCode != 0)
        exitProcess(exitCode)
}

@ExperimentalPathApi
internal fun execute(args: Array<String>): Int {
    var path = Paths.get(".")
    var onlyLayout = false
    if (args.isNotEmpty()) {
        if (args.size > 1) {
            path = Paths.get(args[0])
            if (args[1] == "-OL") onlyLayout = true
        } else {
            if (args[0] == "-OL") onlyLayout = true
            else path = Paths.get(args[0])
        }
    }

    val resultsPath = Paths.get("results")
    runExtraction(path, onlyLayout, resultsPath)

    println("Results can be found at ${resultsPath.toAbsolutePath()}")
    return 0

}

@ExperimentalPathApi
internal fun runExtraction(path: Path, onlyLayout: Boolean, resultsPath: Path): JafaxSummaryData {
    if (!Files.exists(resultsPath))
        resultsPath.toFile().mkdirs()

    ProjectScanner.beginScan(path, path.name)
    val topLevelClassesCount = ClassRepository.topLevelClasses.size
    val filesCount = FileRepository.findAll().size
    val layoutObjectsCount = CommonRepository.findAll().size
    var internalRelationsCount = 0
    var externalRelationsCount = 0
    var metricsCount = 0
    var importsCount = 0
    var interfacesCount = 0
    var abstractClassesCount = 0

    if (!onlyLayout) {
        internalRelationsCount = RelationsComputer.computeRelations(resultsPath, path.name).size
        externalRelationsCount = ExternalRelationsComputer.computeRelations(resultsPath, "${path.name}-external").size
        metricsCount = MetricsComputer.computeMetrics(resultsPath, path.name).size
        importsCount = ImportsComputer.computeImports(resultsPath, path.name).size
        val interfaceSummary = InterfaceComputer.computeImports(resultsPath, path.name)
        interfacesCount = interfaceSummary.interfacesCount
        abstractClassesCount = interfaceSummary.abstractClassesCount
    }

    val status = if (layoutObjectsCount <= 0) "failed" else "success"

    val summaryData = JafaxSummaryData(
        status = status,
        projectName = path.name,
        onlyLayout = onlyLayout,
        filesCount = filesCount,
        topLevelClassesCount = topLevelClassesCount,
        layoutObjectsCount = layoutObjectsCount,
        internalRelationsCount = internalRelationsCount,
        externalRelationsCount = externalRelationsCount,
        metricsCount = metricsCount,
        importsCount = importsCount,
        interfacesCount = interfacesCount,
        abstractClassesCount = abstractClassesCount,
    )
    JafaxSummaryService.writeSummaryData(resultsPath, summaryData)

    return summaryData

}
