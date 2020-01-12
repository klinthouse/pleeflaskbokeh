from flask import Flask, render_template, url_for, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import quandl
import pandas as pd
import numpy as np


quandl.ApiConfig.api_key = "6ofCSn1hDTbSNL8-rs2a"
app = Flask(__name__)
def grab_data(stock, dates):
    company = stock#'FB'
    start_date = dates[0]#'2016-02-01'
    end_date = dates[1]#'2016-03-01'

    data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['date', 'close'] }, ticker = [company], date = { 'gte': start_date, 'lte': end_date })
    return data 

def datetime(x):
    return np.array(x, dtype=np.datetime64)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        company = request.form['ticker'] # input from the typing (import from html)
        time_span = [request.form['start_date'], request.form['end_date']]
        data = grab_data(company,time_span)
        
        try: #add input to the table, stack the tasks
            fig = figure(x_axis_type="datetime", title="Stock Closing Prices", plot_width=600, plot_height=600)
 
            fig.grid.grid_line_alpha=0.3
            fig.xaxis.axis_label = 'Date'
            fig.yaxis.axis_label = 'Price'
        
            fig.line(
                datetime(data['date']), 
                data['close'], 
                line_width=2,
                legend=company,
                color='navy'
            )
            
            # grab the static resources
            js_resources = INLINE.render_js()
            css_resources = INLINE.render_css()

            # render template
            script, div = components(fig)
            html = render_template(
                'bokeh.html',
                plot_script=script,
                plot_div=div,
                js_resources=js_resources,
                css_resources=css_resources,
            )
            return encode_utf8(html)
            # return redirect('/bokeh', data= data)
        except:
            return 'There was an issue searching your ticker'

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)