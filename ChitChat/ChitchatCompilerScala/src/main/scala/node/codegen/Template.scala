package node.codegen

trait Template {

  def getTemplateString(template:String, replacement:Map[String, String]) = {
    // replace all the $ with \\$
    // \\\\ => \
    // \\$ => \$
    val r = replacement map {
      case (key, value) => (key, value.replaceAll("\\$", "\\\\\\$"))
    }

    r.foldLeft(template)((s:String, x:(String,String)) => ( "#\\{" + x._1 + "\\}" ).r.replaceAllIn( s, x._2 ))
  }

  def getClassName(name:String) = {
    name.replace("\"","").capitalize.replace(" ", "_")
  }

}
