package smcho

/**
 * Created by smcho on 8/21/15.
 */
class NoContextException(message: String) extends Exception {
  override def toString() = {
    message
  }
}
