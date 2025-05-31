package smcho

object DatabaseWithStrategy {
  def apply(strategy: String, directory:String, initialSummaryType:String, hostSizes:String) = new DatabaseWithStrategy(strategy, directory, initialSummaryType, hostSizes)
}

class DatabaseWithStrategy(val strategy: String, val directory:String, val initialSummaryType:String, val hostSizes:String) extends Database with LoadClass {
  val storage = Storage(directory, hostSizes)
  val shareLogic: ShareLogic = loadObject(strategy).asInstanceOf[ShareLogic]
  val hostsConfigMap = util.file.readers.readProperty(directory + "/" + "default_buffer_size.txt")

  def getHostLimit(host:Int, hostsLimit:Map[String, Any]): Int = {

    val hostSizesInArray = hostSizes.split(":")
    val groupCount = hostSizesInArray.size // hostsLimit("n").asInstanceOf[Int]
    val accumGroupSizes = new Array[Int](groupCount)
    val defaults = new Array[Int](groupCount)

    // 1. if the hostsLimit (default_buffer_size.txt) has the host id, it just returns it.
    val hostInString = host.toString
    if (hostsLimit.contains(hostInString)) {
      return hostsLimit(hostInString).asInstanceOf[Int]
    }
    else {
      // 1. fill in the groupSizes and default values
      for (g <- 0 until groupCount) {
        accumGroupSizes(g) = hostSizesInArray(g).toInt + (if (g == 0) 0 else accumGroupSizes(g-1))
        defaults(g) = hostsLimit("default" + (g+1)).asInstanceOf[Int]
      }
      // 2. check what group the host is in
      for (g <- 0 until groupCount) {
        if (host < accumGroupSizes(g)) {
          return defaults(g)
        }
      }
      // host
      throw new Exception(s"host id (${host}) is out of range")
    }
  }

  override def get(host: Int) : ContextMessage = {
    val nameTypes = shareLogic.get(host, getHostLimit(host, hostsConfigMap), initialSummaryType)
    ContextMessage(nameTypes)
  }
  // add received ContextMessage to host
  override def add(host: Int, contextMessage: ContextMessage) = {
    storage.add(host, contextMessage)
  }

  override def getSize(nameTypesString: String): Int = {
    NameTypes.size(nameTypesString, storage.summariesMap)
  }

  override def getStorage() : Storage = storage
}