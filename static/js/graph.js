// Use the margin convention practice
var margin = {top: 50, right: 50, bottom: 50, left: 50},
  width, // width gets defined below
  height = 250 - margin.top - margin.bottom;

// Add the SVG to the page
var svg = d3.select(".graph")
    .append('svg')
    .attr("height", height + margin.top + margin.bottom);

var artboard = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%Y-%m-%d-%HT");
dataset.forEach(function(d) {
  d.date = parseTime(d.date);
});

// Append the path, bind the data, but don't call the line generator just yet
var path = artboard.append("path").data([dataset]) // 10. Binds data to the line
    .attr("class", "line"); // Assign a class for styling

var xScale = d3.scaleTime();
var yScale = d3.scaleLinear()
    .range([height, 0]);

var x_axis = d3.axisBottom(xScale);
var y_axis = d3.axisLeft(yScale)
  .ticks(4);

// d3's line generator
var line = d3.line();

xScale.domain(d3.extent(dataset, function(d) { return d.date; }));
yScale.domain([0, d3.max(dataset, function(d) { return d.high; })]);

// 3. Call the x axis in a group tag
var x_axis_element = artboard.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")");
    // dont call the x_axis here as we want our graph to response to
    // changes of the width of the container

var focus = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0)
  .style("display", "none");

// Call the y axis in a group tag
var y_axis_element = artboard.append("g")
    .attr("class", "axis")

// Drawing

function draw_chart() {

  // reset the width
  width = parseInt(d3.select('.graph').style('width'), 10) - margin.left - margin.right;

  // set the svg dimensions
  svg.attr("width", width + margin.left + margin.right);

  // set the new xScale range
  xScale.range([0, width]);

  // give the x_axis the new scale
  x_axis.scale(xScale);
  // draw the new x axis
  x_axis_element.call(x_axis);
  // give the y_axis the new tick_size
  y_axis.tickSize(-width);
  // draw the new y axis
  y_axis_element.call(y_axis)
    .selectAll(".tick:not(:first-of-type) line").attr("stroke", "#777").attr("stroke-dasharray", "2,2");

  // specify new properties for the line
  line.x(function(d) { return xScale(d.date); }) // set the x values for the line generator
    .y(function(d) { return yScale(d.high); }); // set the y values for the line generator
    //.curve(d3.curveMonotoneX); // apply smoothing to the line

  // draw the path based on the line created above
  path.attr("d", line); // Calls the line generator

  // Appends a circle for each datapoint
  // First remove any existing circles
  artboard.selectAll(".dot").remove()

  var dot = artboard.selectAll(".dot")
    .data(dataset);

  dot.enter().append("circle") // Uses the enter().append() method
    .attr("class", "dot") // Assign a class for styling
    .attr("cx", function(d){ return xScale(d.date)} )
    .attr("cy", function(d) { return yScale(d.high) })
    .attr("r", 5)
    .on("mouseover", function(d) {
    focus.transition()
      .duration(200)
      .style("opacity", 1)
      .style("display", 'inline');
    focus.html(d.high)
      .style("left", (d3.event.pageX) + "px")
      .style("top", (d3.event.pageY - 28) + "px");
    })
  .on("mouseout", function(d) {
    focus.transition()
      .duration(500)
      .style("opacity", 0);
    });

  d3.select("#graph").append("p")
    .attr("class", "tooltip")
    .style("opacity", 0)
    .style("display", "none");
}
// call this once to draw the chart initially
draw_chart();
