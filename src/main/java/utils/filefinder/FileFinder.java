package utils.filefinder;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class FileFinder {

    public static FoundFiles findFiles(Path path) {
        try {
            var fileVisitor = new FileVisitor();
            Files.walkFileTree(path, fileVisitor);
            return FoundFiles.builder()
                            .jarFiles(fileVisitor.getJarFiles())
                            .javaFiles(fileVisitor.getJavaFiles())
                            .build();
        } catch (IOException ex) {
            System.out.println("There is an issue with the path: " + path.toString());
        }
        return new FoundFiles();
    }

}
