
var timeChart = function(chartid, json){
    $(chartid).empty();
    
    var jsonfile = "data/triple_tnt_dict.json";
    var graphid = "#time-graph";
    var data = []

	//$.getJSON(jsonfile, function(json) {
    //    if(!tweetid){
    //      for(var k in json){
    //        d = json[k];
    //        d.forEach(function(n){
    //        data.push(n); 
    //       });
    //      }
    //      }
    //    else{
	//	function getdata(json, tweetid) {
	//		newdata = json[tweetid];
    //        if(newdata){
    //        newdata.forEach(function(n){
    //            data.push(n);
    //        })
	//		newdata.forEach(function(l) {
	//			getdata(json, l["target"]);
	//		});}
	//	};
	//	getdata(json, tweetid);
    //    }

  var margin = {top: 20, right: 20, bottom:100, left: 50},
      width = 750 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom;
  
  //var parseDate = d3.time.format("%y.%m.%d").parse;

  
    data = json;
    data.forEach(function(d){
      d.date = d.time;
      d.close = d.tweetNum;
      });

    var formatTime = d3.time.format("%M:%S");
    var formatMinutes = function(d,i){
      return formatTime(d);
    };
  
  //var x = d3.scale.linear()
      //.domain([0,data[data.length-1].time])
  //    .domain([0,12])
  //    .range([0,width]);
  var x = d3.time.scale()
          .domain([0,d3.max(data,function(d){return new Date(Number(d.time)*1000)})])
          .range([0,width])
  
  var y_max = d3.max(data,function(d){return d.tweetNum})
  var y = d3.scale.linear()
      .domain([0,y_max])
      .range([height, 0]);
  
  var xAxis = d3.svg.axis()
      .scale(x)
      .ticks(data.length)
      .orient("bottom")
      //.tickFormat(formatMinutes);
  
  var yAxis = d3.svg.axis()
      .scale(y)
      .ticks(y_max)
      .orient("left");
  
  var line = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.close); });
  
  var svg = d3.select(chartid).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
    x.domain(d3.extent(data, function(d) { return d.date; }));
    //y.domain(d3.extent(data, function(d) { return d.close; }));
  
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(90)")
        .style("text-anchor", "start");
  
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("");
  
    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);
  
}
