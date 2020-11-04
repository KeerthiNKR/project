from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    import pandas
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure,output_file,show
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2016,1,1)
    end=datetime.datetime(2016,3,10)
    df=data.DataReader(name="GOOG", data_source="yahoo",start=start,end=end)
    #print(df.index)
    #print(df)
    def inc_dec(c,o):
        if c>o:
            value="increase"
        elif c<o:
            value="decrease"
        else:
            value="equal"
        return value
    df["Status"]=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Open-df.Close)

    p=figure(x_axis_type="datetime",width=1000,height=300,title="candlestic chart")
    p.grid.grid_line_alpha=0.2
    hours_12=12*60*60*1000
    p.segment(df.index,df.High,df.index,df.Low,color="black")
    p.rect(df.index[df.Status=="increase"],df.Middle[df.Status=="increase"],hours_12,
            df.Height[df.Status=="increase"],fill_color="green",line_color="black")
    p.rect(df.index[df.Status=="decrease"],df.Middle[df.Status=="decrease"],hours_12,
            df.Height[df.Status=="decrease"],fill_color="red",line_color="black")

    script1,div1=components(p)
    cdn_js=CDN.js_files[0]

    return render_template("plot.html",script1=script1,div1=div1,cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
