import pandas as pd
# from get_data import get_names
from flask import Flask, jsonify, render_template
app = Flask(__name__)

datafile_names = "DataSets/belly_button_biodiversity_samples.csv"
datafile_otu = "DataSets/belly_button_biodiversity_otu_id.csv"
datafile_metadata = "DataSets/Belly_Button_Biodiversity_Metadata.csv"


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/names')
def names():
    df = pd.read_csv(datafile_names)
    col_names_df = list(df.drop(['otu_id'], axis=1))
    data = list(col_names_df)
    return jsonify(data)

@app.route('/otu')
def otu():
    df = pd.read_csv(datafile_otu)
    otu_names = df["lowest_taxonomic_unit_found"].values
    data = list(otu_names)
    return jsonify(data)

@app.route("/metadata/<sampleid>")
def metadata(sampleid):
    df = pd.read_csv(datafile_metadata)
    sampleid = int(sampleid.split("_")[1])
    sampleid_df =df.loc[df['SAMPLEID'] == int(sampleid)]
    meta_df = sampleid_df.to_dict('records')
    return jsonify(meta_df)

@app.route('/wfreq/<sampleid>')
def wfreq(sampleid):
    df = pd.read_csv(datafile_metadata)
    sampleid = int(sampleid.split("_")[1])
    sampleid_df =df.loc[df['SAMPLEID'] == int(sampleid)]
    sampleid_df_wfreq = sampleid_df.filter(items=['WFREQ'])
    value = sampleid_df_wfreq['WFREQ'].values[0]
    return jsonify(value)

@app.route('/samples/<sampleid>')
def samples(sampleid):
    df = pd.read_csv(datafile_names)
    # sampleid_ = 'BB_' + str(sampleid)
    sampleid_ = str(sampleid)
    data = df[['otu_id',sampleid_]]
    data=data.loc[data[sampleid_]>0]
    data.columns=['otu_id',sampleid_]
    data=data.sort_values(sampleid_,ascending=False)
    otu_ids=[]
    samples=[]
    for i in range(0,len(data)):
        otu_ids.append(str(data['otu_id'].iloc[i]))
        samples.append(str(data[sampleid_].iloc[i]))
        newdict={
        "otu_id":otu_ids,
        "samples":samples
        }
    return jsonify(newdict)
    
    


if __name__ == "__main__":
    app.run(debug=True)