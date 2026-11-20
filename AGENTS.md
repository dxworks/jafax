# AGENTS Guide for JaFaX

This guide is for coding agents working in this repository. It captures the actual build/test flow and the conventions already present in the code.

## Repository Snapshot
- Primary language: Kotlin (Maven project)
- Entry point: `org.vladg.jafax.MainKt`
- Java version: 11
- Packaging: fat jar via Maven Assembly plugin (`target/jafax.jar`)
- Node wrapper: CommonJS CLI in `lib/*.js` with package entry in `package.json`
- CI validation command: `mvn clean verify`

## Cursor/Copilot Rule Files
- No `.cursorrules` file found
- No `.cursor/rules/` directory found
- No `.github/copilot-instructions.md` found
- Use this `AGENTS.md` and existing repository patterns as the source of truth

## Setup
Run from repository root:
```bash
mvn clean install
```

Node wrapper setup/build:
```bash
npm ci
npm run build
```

Notes:
- `npm run build` copies `lib/*.js` to `dist` and copies `target/jafax.jar` to `dist`
- Build Java first if `target/jafax.jar` does not exist

## Build Commands
Full build:
```bash
mvn clean package
```

Fast build without tests:
```bash
mvn clean package -DskipTests
```

CI-equivalent verification:
```bash
mvn clean verify
```

## Test Commands
Run all unit tests:
```bash
mvn test
```

Run unit + integration tests:
```bash
mvn verify
```

Run one unit test class (Surefire):
```bash
mvn -Dtest=MethodSerializerTest test
```

Run one unit test method:
```bash
mvn -Dtest=MethodSerializerTest#shouldSerializeIgnorablePropertiesWhenValuesAreNotDefault test
```

Run one integration test class (Failsafe):
```bash
mvn -Dit.test=RelationsIT verify
```

Run one integration test method:
```bash
mvn -Dit.test=RelationsIT#shouldProperlyComputeRelationsWhenUsingTheLayoutFile verify
```

Debug fuller stack traces:
```bash
mvn -Dtest=ClassName test -DtrimStackTrace=false
```

Important test config from `pom.xml`:
- Surefire excludes:
  - `FingerprintsXmlParserTest.java`
  - `FileUtilsTest.java`
  - `ImportUtilsTest.java`
  - `JsonToCsvTransformerTest.java`
- Failsafe executes `integration-test` and `verify`

## Lint/Formatting
No dedicated lint/format task is configured (no ktlint, detekt, checkstyle, spotless, eslint, or prettier config detected).

Use this quality baseline:
```bash
mvn clean test
mvn clean verify
```

If you add linting/formatting tooling, do it in a dedicated PR and update this file with exact commands.

## Run Commands
Run built jar:
```bash
java -jar target/jafax.jar <path-to-project>
```

Run through Maven main class:
```bash
mvn -DskipTests exec:java -Dexec.mainClass=org.vladg.jafax.MainKt -Dexec.args="<path-to-project>"
```

Layout-only mode is supported via `-OL`.

## Code Style Guidelines
Follow existing style in touched files over personal preference.

### Imports
- Prefer explicit imports; avoid introducing wildcard imports
- Existing Kotlin grouping pattern:
  1) project imports (`org.vladg...`)
  2) Java/JDK imports (`java...`)
  3) Kotlin imports (`kotlin...`)
- Keep imports stable and reasonably sorted within groups

### Formatting and Structure
- Use 4-space indentation in Kotlin
- Prefer expression-bodied functions for trivial returns
- Wrap chains/long calls across lines when readability improves
- Group members by responsibility (state, computed properties, behavior)
- Avoid comments unless intent is non-obvious

### Types and Nullability
- Prefer explicit types for public API and non-obvious declarations
- Model optional values as nullable (`T?`) and use safe calls/Elvis
- Minimize `!!`; only use when invariants are guaranteed
- Keep mutable types explicit (`MutableList`, `MutableSet`) where mutation is required
- Keep serializer model defaults intact; output size/shape depends on them

### Naming
- Types/objects: `PascalCase`
- Functions/properties/variables: `camelCase`
- Tests: descriptive backtick names are common and preferred
- Use meaningful names (`onlyLayout`, `resultsPath`) over abbreviations

### Error Handling and Logging
- Prefer fail-fast behavior with useful context
- Use SLF4J helper (`logger()`) in Kotlin components
- Keep `println` for user-facing CLI output only
- Do not swallow exceptions silently; log or propagate with context
- Keep side effects localized (scanner init, I/O, repository cleanup)

### Testing Conventions
- Tests live in `src/test/java` (including Kotlin test files)
- Keep test flow clear: arrange/act/assert
- Clear shared repositories in setup when using singleton repos
- Integration-style tests follow `*IT` naming and use fixtures in `src/test/resources`

### Node Wrapper Conventions
- Use CommonJS (`require`, `module.exports`)
- Keep wrapper logic thin; heavy logic belongs in Kotlin code
- Preserve runtime assumptions: Java 11 minimum and `dist/jafax.jar`

## Change Management for Agents
- Make the smallest safe change that solves the task
- Avoid broad refactors unless explicitly requested
- Preserve backward compatibility for output file names and result formats
- Validate with targeted tests first, then broader `mvn verify` when practical
- Update this file whenever build/test workflow changes
