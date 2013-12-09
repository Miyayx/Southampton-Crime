var bubbleChart = function(chartid,root){
    $(chartid).empty();

  var diameter = 600,
      format = d3.format(",d"),
      color = d3.scale.category20();
  
  var bubble = d3.layout.pack()
      .sort(null)
      .size([diameter, diameter])
      .padding(1.5);
  
  var svg = d3.select(chartid).append("svg")
      .attr("width", diameter)
      .attr("height", diameter)
      .attr("class", "bubble");
  
  //d3.json(json, function(error, root) {
    var node = svg.selectAll(".node")
        .data(bubble.nodes(
        classes(root))
        .filter(function(d) { return !d.children; }))
      .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .on("click",function(d,i){
           showTweets(d.tweet);
        });
  
    node.append("title")
        .text(function(d) { return d.className + ": " + format(d.value); });
  
    node.append("circle")
        //.attr("r", function(d) { return d.r; })
        .attr("r", 0)
        .style("fill", function(d) { return color(d.className); });

    node.selectAll("circle")
        .transition()
        .attr("r", function(d) { return d.r; })
        .duration(1000)
  
    node.append("text")
        .attr("dy", ".3em")
        .attr("fill", "white")
        .attr("font-size",function(d){ return d.value;})
        .style("text-anchor", "middle")
        .text(function(d) { return d.className; });
//  });
  
  // Returns a flattened hierarchy containing all leaf nodes under the root.
  function classes(root) {
    var classes = [];
  
    function recurse(name, node) {
      if (node.children) node.children.forEach(function(child) { recurse(node.reposts_count, child); });
    //  else classes.push({packageName: reposts_count, className: node.reposts_count, value: (node.fre > 300? 300: node.fre)});
      else classes.push({packageName: name, className: node.repost_count, value: node.fre, tweet:node.tweet });
    }
  
    recurse(null, root);
    return {children: classes};
  }
  
  d3.select(self.frameElement).style("height", diameter + "px");
}
