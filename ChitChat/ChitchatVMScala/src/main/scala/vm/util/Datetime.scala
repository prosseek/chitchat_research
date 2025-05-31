package vm.util

import java.text.SimpleDateFormat

object Datetime {
  def getDistance(date1:List[Int], time1:List[Int], date2:List[Int], time2:List[Int]) = {
    def dateString(date:List[Int]) = {
      f"${date(0)}%02d/${date(1)}%02d/${date(2)}%02d"
    }
    def timeString(time:List[Int]) = {
      f"${time(0)}%02d:${time(1)}%02d:${time(2)}%02d"
    }
    // find date difference
    val format = new SimpleDateFormat("yy/MM/dd HH:mm:ss");
    val d1 = format.parse(dateString(date1) + " " + timeString(time1))
    val d2 = format.parse(dateString(date2) + " " + timeString(time2));

    val diff = d1.getTime() - d2.getTime();
    val diffSeconds = diff / 1000;
    diffSeconds / 60;
  }
}
