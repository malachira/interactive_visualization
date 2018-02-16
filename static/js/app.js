
function buildForm() {
/* Function to build dropdown memo from /names route */
    
    var URL = "/names"

    d3.json(URL, function(error, response) {
        if (error) return console.warn(error);
  
        /*construct dropdown*/
        d3.select("body")
        .append("select")
        .attr("id","selDataset")
        .attr("onchange","getData(this.value)");
    
        for(i=0; i<response.length;i++){
    
            d3.select("select")
            .append("option")
            .attr("value",response[i])
            .text(response[i]);
        }

    })
}

function buildPlot(url) {

    Plotly.d3.json(url, function(error, response) {

        console.log(url);

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

function getData(dataset) {
    console.log(dataset);
    var url = "/samples/" + dataset;
    buildPlot(url);

  }

buildForm();

var init_url = "/samples/BB_940";
buildPlot(init_url);