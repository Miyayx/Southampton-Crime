
var pathGraph = function(graphid, tweetid) {
    //var jsonfile = "triple_tnt_list.json";
    var jsonfile = "data/triple_tnt_dict.json";
    var graphid = "#path-graph";
	var links = [];
	$.getJSON(jsonfile, function(json) {
        if(!tweetid){
          for(var k in json){
            d = json[k];
            d.forEach(function(n){
            links.push(n); 
           });
          }
          }
        else{
		function getlink(json, tweetid) {
			newlinks = json[tweetid];
            if(newlinks){
            newlinks.forEach(function(n){
                links.push(n);
            })
			newlinks.forEach(function(l) {
				getlink(json, l["target"]);
			});}
		};
		getlink(json, tweetid);
        }
	var nodes = {};

	// Compute the distinct nodes from the links.
	links.forEach(function(link) {
		link.source = nodes[link.source] || (nodes[link.source] = {
			name: link.source,
            tweet:link.source_tweet
		});
		link.target = nodes[link.target] || (nodes[link.target] = {
			name: link.target,
            tweet:link.target_tweet
		});
	});

	var width = 750,
	height = 800;
    if(!tweetid)
        width = 1200;

	var force = d3.layout.force().nodes(d3.values(nodes)).links(links).size([width, height]).linkDistance(60).charge( - 300).on("tick", tick).start();

	var svg = d3.select(graphid).append("svg").attr("width", width).attr("height", height);

	var link = svg.selectAll(".link").data(force.links()).enter().append("line").attr("class", "link");

	var node = svg.selectAll(".node")
    .data(force.nodes())
    .enter()
    .append("g")
    .attr("class", "node")
    .on("mouseover", function(d,i){
		d3.select(this).select("circle").transition().duration(750).attr("r", 16);
        showTweets2(d.tweet);
    })
    .on("mouseout", mouseout).call(force.drag);

	node.append("circle")
    .attr("r", 8)
    .attr("fill",function(d){ return (d.name == tweetid)? "#428bca":"#ccc"; })
    .on("click",function(d,i){
        showTweets(d.tweet);
    });

	node.append("text").attr("x", 12).attr("dy", ".35em").text(function(d) {
		return d.name;
	});

	function tick() {
		link.attr("x1", function(d) {
			return d.source.x;
		}).attr("y1", function(d) {
			return d.source.y;
		}).attr("x2", function(d) {
			return d.target.x;
		}).attr("y2", function(d) {
			return d.target.y;
		});

		node.attr("transform", function(d) {
			return "translate(" + d.x + "," + d.y + ")";
		});
	}

	function mouseover(d,i) {
		d3.select(this).select("circle").transition().duration(750).attr("r", 16);
	}

	function mouseout() {
		d3.select(this).select("circle").transition().duration(750).attr("r", 8);
	}

	});
}

