package vm.util

object Geolocation {
  /**
    * dd -> degress
    *
    * ==== Example ====
      From [http://www.uwgb.edu/dutchs/usefuldata/utmformulas.htm]
      {{{
        (dd + mm/60 +ss/3600) to Decimal degrees (dd.ff)
         dd = whole degrees, mm = minutes, ss = seconds
         dd.ff = dd + mm/60 + ss/3600
         Example: 30 degrees 15 minutes 22 seconds = 30 + 15/60 + 22/3600 = 30.2561
      }}}
    *
    * @param dd
    */
  def dd2d(dd:List[Int]) = {
    /**
      * ==== Example ====
      * {{{
      *   1 -> 0.1
      *   123 -> 0.123
      * }}}
      *
      * @param value
      */
    def scale(value:Double) = {

    }
    val whole_degree = dd(0).toDouble
    val minute = dd(1).toDouble/60.0
    val second = (dd(2).toString + "." + dd(3).toString).trim.toDouble/3600.0
    whole_degree + minute + second
  }

  def diff(long1:List[Int], long2:List[Int]) = {
    long1.zipWithIndex map {
      case (value, index) => value - long2(index)
    }
  }

  /**
    * http://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    *
    * @param lat1
    * @param long1
    * @param lat2
    * @param long2
    * @return
    */
  def getDistance(lat1:Double, long1:Double, lat2:Double, long2:Double) = {
    def deg2rad(deg:Double) = deg * (Math.PI/180.0)

//    val lat1 = dd2d(la1)
//    val long1 = dd2d(lo1)
//    val lat2 = dd2d(la2)
//    val long2 = dd2d(lo2)

    var R = 6371.0; // Radius of the earth in km
    var dLat = deg2rad(lat2-lat1);  // deg2rad below
    var dLon = deg2rad(long2-long1);
    var a =
      Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
          Math.sin(dLon/2) * Math.sin(dLon/2)

    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c; // Distance in km
    d
  }
}
