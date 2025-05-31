package vm

import api.API

object Repl extends App {

  val summary = """{
                  |  "string": "James",
                  |  "age": 10,
                  |  "longitude": [11,12,13,14],
                  |  "latitude": [1,2,3,4],
                  |  "date": [10,3,17],
                  |  "time": [12,14]
                  |}""".stripMargin

  def showHelp() = {
    val help =
      """|tos: show top of stack, "null" if stack is empty
         |ps: print stack (up to TOS)
         |ps2: print all the elements in the stack (can be different from ps)
         |ss: stack size""".stripMargin
    println(help)
  }

  def printStack(showEverything:Boolean = false) = {
    val index = if (showEverything) vm.stack.stack.size else vm.stack.sp

    for (i <- 0 until index) {
      val content = vm.stack.stack(i)
      if (content == null) print("null" + "|")
      else print(content.toString + "|")
    }
    println()
  }

  val fbf = API.create_fbf_summary(summary, Q = 4)
  val vm = new ChitchatVM(fbf)
  var proceed = true

  def commandProcess(command:String) : Boolean = {
    if (command.length == 0) return true
    else {
      command match {
        case "help" => showHelp(); return true
        case "tos" => println(vm.stack.tos); return true
        case "ss" => println(vm.stack.sp); return true
        case "ps" => printStack(); return true
        case "ps2" => printStack(true); return true
        case _ => return false
      }
    }
  }

  while (proceed) {
    print("> ")
    val ln = scala.io.StdIn.readLine().trim()
    if (ln == "q" || ln == "quit") {
      proceed = false
    }
    else
    {
      if (!commandProcess(ln)) {
        try {
          vm.evalCommand(ln, null)
        }
        catch {
          case e : Throwable => println(e)
        }
      }
    }
  }
}
