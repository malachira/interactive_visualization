# import necessary libraries
import pandas as pd

from flask import (
    Flask,
    json,
    render_template,
    jsonify)

#Read all the csv files into data-frames
sample = pd.read_csv("DataSets/belly_button_biodiversity_samples.csv")
otu_id = pd.read_csv("DataSets/belly_button_biodiversity_otu_id.csv")
metadata = pd.read_csv("DataSets/Belly_Button_Biodiversity_Metadata.csv")
otu_in_samples = pd.read_csv("DataSets/belly_button_biodiversity_samples.csv")

#Create data for @app.route('/names')
#Get the column-names into a list
sample_names = list(sample.columns[1:])

#Create data for @app.route('/otu')
#Make a list of OTU descriptions
otu_descr = list(otu_id["lowest_taxonomic_unit_found"])

#Create data for @app.route('/metadata/<sample>')
#Choose only the relevant columns
new_metadata = metadata[["AGE", "BBTYPE", "ETHNICITY", "GENDER", "LOCATION", "SAMPLEID", "WFREQ"]]

#convert df columns to list of dictionaries
meta_dict = list(new_metadata.T.to_dict().values())

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#  send the jsonified sample-name results from the "sample" df created above
@app.route("/names")
def names():
    return jsonify(sample_names)

#Send the jsonified list of OTU descriptions.
@app.route('/otu')
def otu():
    return jsonify(otu_descr)

#Send jsonified MetaData for a given sample.
# Args: Sample in the format: `BB_940`
@app.route('/metadata/<sample>')
def metadata(sample):
    #remove the pre-fix BB_ form sample & convert to int type
    sample = int(sample[3:])

    #search through all dictionary for sample & return jsonified samples
    for samples in meta_dict:
        search_term = int(samples["SAMPLEID"])

        if(search_term == sample):
            return jsonify(samples)

    return jsonify({"error": f"Sample with ID {sample} not found."}),404


# Send jsonified OTU IDs and Sample Values for a given sample.
@app.route('/samples/<sample>')
def samples(sample):
    #remove the pre-fix BB_ form sample & convert to int type
    sample = int(sample[3:])

    #parse through all the sample_ids & extract the otu_ids & quantity present for each sample_id
    for col in otu_in_samples.columns[1:]:

        col_name = int(col[3:])

        if(col_name == sample):

            sample_pd = pd.DataFrame(columns=["otu_id","num_samples"])
            otu_id_lst = []
            sample_val_lst = []
        
            #extract list of non-zero otu_ids
            non_zero_index = [x for x in otu_in_samples[col].index if otu_in_samples[col][x] > 0]

            #create a list of otu_ids & values for each sample
            for indx in non_zero_index:
                otu_id_lst.append(otu_in_samples["otu_id"][indx])
                sample_val_lst.append(otu_in_samples[col][indx])

            #create datframes for sorting by sample values    
            sample_pd["otu_id"] = otu_id_lst
            sample_pd["num_samples"] = sample_val_lst

            #sort df by sample values
            sample_pd = sample_pd.sort_values('num_samples',ascending=False)

            #convert columns to string to prevent "int64 is not JSON serializable" error
            sample_pd["otu_id"] = sample_pd["otu_id"].astype(str)
            sample_pd["num_samples"] = sample_pd["num_samples"].astype(str)

            #After sorting, put the columns in list format(easier to slice)
            otu_id_lst = list(sample_pd["otu_id"])
            sample_val_lst = list(sample_pd["num_samples"])

            sample_dict = {
                "otu_id": otu_id_lst[:10],
                "sample_values": sample_val_lst[:10],
                "type": "pie"
            }
            
            return jsonify(sample_dict)

    return jsonify({"error": f"Sample with ID {sample} not found."}),404

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
