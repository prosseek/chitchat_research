package smcho

/**
 * Database only cares about generating ContextMessage content
 *
 * Created by smcho on 8/26/15.
 */
trait Database {
  // returns Content content (string) to share for host
  def get(host: Int) : ContextMessage
  // add received ContextMessage to host
  def add(host: Int, contextMessage: ContextMessage)
  def getSize(nameTypesString: String) : Int
  def getStorage() : Storage
}
