package org.vladg.jafax.utils.filefinder

import java.nio.file.Files
import java.nio.file.Path

object FileFinder {

    fun findFiles(path: Path): JavaSourceFiles {
        val fileVisitor = FileVisitor()
        Files.walkFileTree(path, fileVisitor)
        // walkFileTree hands back directory entries in filesystem order, which
        // differs per platform: roughly sorted on APFS, arbitrary on ext4. When a
        // project holds two classes with the same fully qualified name, the one
        // parsed first wins and the other is dropped as unresolvable, so that
        // order decides the analysis output. Sorting makes the result the same
        // everywhere.
        return JavaSourceFiles(fileVisitor.javaFiles.sorted(), fileVisitor.jarFiles.sorted())
    }

}