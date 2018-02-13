/* data route */
var url = "/samples/BB_940"

function buildPlot() {
    Plotly.d3.json(url, function(error, response) {

        console.log(response);

        var trace1 = {
            type: "pie",
            name: "OTUs in sample",
            labels: response.otu_id,
            values: response.sample_values
        };

        var data = [trace1];

        var layout = {
            title: "Top-10 OTU for Sample value"
        };

        Plotly.newPlot("plot", data, layout);
    });
}

buildPlot();