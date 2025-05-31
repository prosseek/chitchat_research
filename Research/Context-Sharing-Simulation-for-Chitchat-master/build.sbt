lazy val root = (project in file(".")).aggregate(contextSummary, contextProcessor)
lazy val contextSummary = project
lazy val contextProcessor = project.dependsOn(contextSummary)
