function createDeployTrendsGraph(divID, timeData, deployData) {
  for (var i = 0; i < timeData.length; i++) {
    timeData[i] = getTimeseriesFormat(timeData[i]);
  }

  timeData.unshift('date');
  deployData.unshift('deploys');

  var chart = c3.generate({
    bindto: divID,
    data: {
      x: 'date',
      x_format : '%Y%m%d', // default '%Y-%m-%d'
      columns: [
        timeData,
        deployData,
        ],
    },
    axis : {
        x : {
            type : 'timeseries'
        }
    }
  });
}

function getTimeseriesFormat(timestamp) {
  var aDate = new Date(timestamp * 1000);
  var year  = aDate.getFullYear();
  var month = aDate.getMonth() + 1;
  var day   = aDate.getDate();

  if(month < 10)
    month = "0" + month;

  if(day < 10)
    day = "0" + day;

  return(year.toString() + month.toString() + day.toString())
}
