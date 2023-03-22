import { 
    select, csv, scaleLinear, scaleBand, axisBottom, max // axisLeft, format
} from 'd3';

const titleText = 'Adverse Events by Drug and Manufacturer'
const xAxisLabelText = 'Adverse Effect'

const svg = select('svg');

const width = +svg.attr('width');
const height = +svg.attr('height');

const render = data => {
    const xValue = d => d['Adverse Event']
    const yValue = d => d['Count']
    const margin = { top: 50, righ: 40, bottom: 77, left: 180 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const xScale = scaleLinear()
        .domain([0, max(data, xValue)])
        .range([0, innerWidth])

    const yScale = scaleBand()
        .domain(data.map(yValue))
        .range([0, innerHeight])
        .padding(0.1);

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)

    const xAxisG = axisBottom(xScale)
        .tickSize(-innerHeight)

    // g.append('g')
    //     .call(axisLeft(yScale))
    //     .selectAll('.domain, .tick line')
    //           .remove();

    xAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('y', 65)
        .attr('x', innerWidth / 2)
        .attr('fill', 'black')
        .text(xAxisLabelText);

    g.selectAll('rect').data(data)
        .enter().append('rect')
            .attr('y', d => yScale(yValue(d)))
            .attr('width', d => xScale(xValue(d)))
            .attr('height', yScale.bandwidth());

    g.append('text')
        .attr('class', 'title')
        .attr('y', -10)
        .text(titleText);
}


csv('data/BarChart_ACETAMINOPHEN_all.csv').then(data => {
    // data.forEach(d => {
    //     d.population = +d.population * 1000;
    // })
    render(data);
})