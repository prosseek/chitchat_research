package vm

import sys.process._
import java.nio.file.{Files, Paths}
import java.text.SimpleDateFormat
import java.util.Calendar

object System {
  def here() = {
    def extractInfo(str: String) = str.split(":")(1).trim.toDouble

    val command = "/Users/smcho/Dropbox/smcho/bin/whereami"
    if (Files.exists(Paths.get(command))) {
      // Latitude: 30.287162
      // Longitude: -97.736658
      // Accuracy (m): 65.000000
      val locationInformation = command.!!.split("\n")
      val latitude = extractInfo(locationInformation(0))
      val longitude = extractInfo(locationInformation(1))
      (latitude, longitude)
    }
  }
  def now() = {
    val now = Calendar.getInstance().getTime()
    val hourFormat = new SimpleDateFormat("y:M:d:H:K:m")
    val result = hourFormat.format(now)
    result.split(":").map(_.trim).map(_.toInt).toList
  }
}
