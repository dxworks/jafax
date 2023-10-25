package org.vladg.jafax.ast

import com.google.inject.Inject
import org.eclipse.jdt.core.JavaCore
import org.eclipse.jdt.core.dom.AST
import org.eclipse.jdt.core.dom.ASTParser
import org.vladg.jafax.utils.extensions.logger

class ASTCreator {

    @Inject
    private lateinit var astRequester: ASTRequester

    private val logger = logger()

    fun createAst(javaFiles: Array<String>, jarFiles: Array<String>) {
        logger.info("Creating the AST Request...")
        val parser = ASTParser.newParser(AST.JLS17)
        parser.setResolveBindings(true)
        parser.setKind(ASTParser.K_COMPILATION_UNIT)
        setParserOptions(parser)
        parser.setEnvironment(jarFiles, emptyArray(), emptyArray(), true)
        val encodings = javaFiles
            .map { "UTF-8" }
            .toList()
            .toTypedArray()
        parser.createASTs(javaFiles, encodings, emptyArray(), astRequester, null)
    }

    private fun setParserOptions(parser: ASTParser) {
        val options = JavaCore.getOptions()
        options[JavaCore.COMPILER_COMPLIANCE] = JavaCore.VERSION_17
        options[JavaCore.COMPILER_CODEGEN_TARGET_PLATFORM] = JavaCore.VERSION_17
        options[JavaCore.COMPILER_SOURCE] = JavaCore.VERSION_17
        parser.setCompilerOptions(options)
    }

}