#coding:utf-8
import bokeh
from bokeh.charts import HeatMap, output_file, show
from bokeh.sampledata.unemployment1948 import data
import pandas
import Draw
from bokeh.palettes import YlOrRd9 as palette
def das():
    output_file("cat_heatmap.html")
    palette = bokeh.palettes.YlOrRd9[::-1]
    date = Draw.draw_heatmap_data_pre('李开复')
    hm10 = HeatMap(date, x='word', y='year', values='freq', stat=None,
                   sort_dim={'x': False}, width=1000)
    show(hm10)

Draw.draw_heatmap('李开复')
