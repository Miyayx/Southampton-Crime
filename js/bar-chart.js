var barChart = function(chartid, data){
    $(chartid).empty();

  var margin = {top: 20, right: 20, bottom: 30, left: 40},
      width = 700 - margin.left - margin.right,
      height = 550 - margin.top - margin.bottom;
  
  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);
  
  var y = d3.scale.linear()
      .range([height, 0]);
  
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");
  
  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");
  
  var color = d3.scale.category20();
  
  var svg = d3.select(chartid).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  //d3.json(json,function(error, data) {
    data = data.children;
    x.domain(data.map(function(d){ return d.repost_count; }));
    //y.domain([0, d3.max(data, function(d) { return d.fre; })]);
    y.domain([0, 300]);
  
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
  
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
  
    svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.repost_count); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.fre); })
        .attr("height",0)
        .style("fill", function(d) { return color(d.repost_count); });

    svg.selectAll("rect")
        .transition()
        .attr("height", function(d) { return height - y(d.fre); })


    var yTextPadding = 10;
    svg.selectAll(".bartext")
    .data(data)
    .enter()
    .append("text")
    .attr("class", "bartext")
    .attr("text-anchor", "middle")
    .attr("fill", "black")
    .attr("x", function(d,i) {
            return x(i)+x.rangeBand()/2;
       })
    .attr("y", function(d,i) {
            return y(d.fre > 300 ? 300: d.fre)
       })
    .attr("height", function(d){ return height-y(d.fre)+yTextPadding})
    .text(function(d){
            return d.fre;
      });
  
//  });
  
  function type(d) {
    d.frequency = +d.frequency;
    return d;
  }
}
