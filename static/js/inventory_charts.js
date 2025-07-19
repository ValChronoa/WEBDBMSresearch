/* global d3 */
function drawAging(selector, url) {
  d3.json(url).then(data => {
    const width = 250, height = 250, radius = Math.min(width, height) / 2;
    const color = d3.scaleOrdinal(d3.schemeCategory10);
    const svg = d3.select(selector).append("svg")
                  .attr("viewBox", `0 0 ${width} ${height}`)
                  .append("g").attr("transform", `translate(${width/2},${height/2})`);
    const pie = d3.pie().value(d => d.count);
    const arc = d3.arc().innerRadius(50).outerRadius(radius);
    svg.selectAll("path").data(pie(data)).join("path")
       .attr("d", arc).attr("fill", d => color(d.data.bucket))
       .append("title").text(d => `${d.data.bucket}: ${d.data.count}`);
  });
}

function drawForecast(selector, url) {
  d3.json(url).then(data => {
    const height = 150, margin = {top: 10, right: 30, bottom: 20, left: 40};
    const width = 600 - margin.left - margin.right;
    const svg = d3.select(selector).append("svg")
                  .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
                  .append("g").attr("transform", `translate(${margin.left},${margin.top})`);
    const x = d3.scaleBand().domain(data.map(d => d.due)).range([0, width]).padding(0.1);
    const y = d3.scaleLinear().domain([0, 1]).range([height, 0]);
    svg.append("g").attr("transform", `translate(0,${height})`).call(d3.axisBottom(x).tickFormat(d3.timeFormat("%m-%d")));
    svg.selectAll("rect").data(data).join("rect")
       .attr("x", d => x(d.due)).attr("y", d => y(1))
       .attr("width", x.bandwidth()).attr("height", d => height - y(1))
       .attr("fill", "#2c5f97");
  });
}