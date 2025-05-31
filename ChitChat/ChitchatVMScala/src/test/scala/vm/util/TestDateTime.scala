package vm.util

import org.scalatest.FunSuite

class TestDateTime extends FunSuite
{
  test("test date time") {
    val date1 = List(11, 3, 14)
    val time1 = List (9, 29, 58)

    //val dateStop = "11/03/14 09:33:43";
    val date2 = List(11, 3, 14)
    val time2 = List (9, 33, 43)

    val res = Datetime.getDistance(date1, time1, date2, time2)
    assert(res == -3)
  }
}
