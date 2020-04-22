import keren_shava as ks
import shpitzer as shp
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show, Row
from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import ColumnDataSource, Slider, CustomJS, TextInput, Paragraph, Text, RadioGroup, Button, CheckboxGroup, Spacer
import time
import datetime
import numpy as np

class Maslul:
    def __init__(self, shita, loan, months, ribit, madad, figures):
        self.fig1 = figures[0]
        self.fig2 = figures[1]
        self.loan = loan
        self.months = months
        self. ribit = ribit
        self.madad = madad
        self.shita_string = shita
        if self.shita_string == "keren" or self.shita_string == "keren_shava":
            self.shita = ks.keren_shava(loan, months, ribit)
        elif self.shita_string == "shpitzer":
            self.shita = shp.shpitzer(loan, months, ribit)
        else:
            raise KeyError("Error shita is no valid {}".format(shita))

        self.shita.build_table(loan, months, ribit)

        self.source_left_loan = ColumnDataSource(data=dict(x=range(0, self.months), y=self.shita.get_left_loan()))
        self.source_monthly_ret = ColumnDataSource(data=dict(x=range(0, self.months), y=self.shita.get_monthly_total()))

        self.fig1.circle(x='x', y='y', source=self.source_left_loan,
                         color=self.shita.color, size=2, alpha=0.3)
        self.fig2.circle(x='x', y='y', source=self.source_monthly_ret,
                         color=self.shita.color, size=2, alpha=0.3)
        text = [self.shita.get_monthly_total()[0]]
        if self.shita.color == 'green':
            x_text = 0
            y_text = 4200
        else:
            x_text = 0
            y_text = 3900
        self.source_text_monthly_ret = ColumnDataSource(dict(x=[x_text], y=[y_text], text=text))
        glyph = Text(x="x", y="y", text="text", angle=0.0, text_color=self.shita.color,
                     name='show_monthly_payment')
        self.fig2.add_glyph(self.source_text_monthly_ret, glyph)

    def __add__(self, other):
        for i in range(0, self.shita.months):
            self.shita.loan_left[i] += other.shita.loan_left[i]
            self.shita.monthly_ret[i] += other.shita.monthly_ret[i]
            self.shita.monthly_fee[i] += self.shita.monthly_fee[i]
            self.shita.monthly_total[i] += self.shita.monthly_total[i]


    def update(self, loan, months, ribit, madad):
        self.loan = loan
        if months == 0:
            print("warning [update] period can't be 0, setting to months to 1 year")
            months = 12
        self.months = months
        self.ribit = ribit
        self.madad = madad
        self.shita.build_table(loan, months, ribit)
        self.source_left_loan.data = dict(x=range(0, int(self.months)), y=self.shita.get_left_loan())
        self.source_monthly_ret.data = dict(x=range(0, int(self.months)), y=self.shita.get_monthly_total())

        text = [self.shita.get_monthly_total()[0]]
        if self.shita.color == 'green':
            x_text = 0
            y_text = 4200
        else:
            x_text = 0
            y_text = 3900

        self.source_text_monthly_ret.data = dict(x=[x_text], y=[y_text], text=text)

        # glyph = Text(x="x", y="y", text="text", angle=0.0, text_color=self.shita.color)
        # self.fig2.add_glyph(self.source_text_monthly_ret, glyph)

loan = 401000

ribit = 4.32

krn_year = 20
shp_year = 20
krn_months = 12 * krn_year
shp_months = 12 * shp_year

# Set up the figure(s)
class figure_factory:
    def __init__(self):
        self.figures_types = ["monthly payment","left loan"]

    def get_figture(self, figure_type):
        if figure_type == self.figures_types[0]:
            return figure(background_fill_color='gray',
             background_fill_alpha=0.5,
             border_fill_color='black',
             border_fill_alpha=0.25,
             plot_height=300,
             plot_width=400,
             x_axis_label='months',
             x_axis_type='linear',
             x_axis_location='below',
             x_range=(0, 360),
             y_axis_label='payment',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(0, 4500),
             title='monthly return Figure',
             title_location='right',
             toolbar_location='below',
             tools=["hover","pan","box_zoom","wheel_zoom","reset"])
        elif figure_type == self.figures_types[1]:
            return figure(background_fill_color='gray',
                   background_fill_alpha=0.5,
                   border_fill_color="black",
                   border_fill_alpha=0.25,
                   plot_height=300,
                   plot_width=400,
                   x_axis_label='months',
                   x_axis_type='linear',
                   x_axis_location='below',
                   x_range=(0, 360),
                   y_axis_label='left loan',
                   y_axis_type='linear',
                   y_axis_location='left',
                   y_range=(0, 450000),
                   title='loan left Figure',
                   title_location='right',
                   toolbar_location='below',
                   tools=["hover","pan","box_zoom","wheel_zoom","reset"])
        else:
            raise KeyError("ERROR figure_factory: [get_figture] no such figure_type {}. please choose one of {}".format(figure_type,self.figures_types))

## KLTZ
fig_kltz1 = figure_factory().get_figture("left loan")
fig_kltz2 = figure_factory().get_figture("monthly payment")
figures_kltz = [fig_kltz1, fig_kltz2]

kalatz_shp = Maslul("shpitzer", loan, months=shp_months, ribit=ribit, madad=106.7, figures=figures_kltz)
kalatz_krn = Maslul("keren_shava", loan, months=shp_months, ribit=ribit, madad=106.7, figures=figures_kltz)

kalatz_shp.update(loan=loan, months=shp_months, ribit=ribit, madad=106.7)
kalatz_krn.update(loan=loan, months=krn_months, ribit=ribit, madad=106.7)

## PRIME
fig_prime1 = figure_factory().get_figture("left loan")
fig_prime2 = figure_factory().get_figture("monthly payment")
figures_prime = [fig_prime1, fig_prime2]

prime_shp = Maslul("shpitzer", loan, months=shp_months, ribit=ribit, madad=106.7, figures=figures_prime)
prime_krn = Maslul("keren_shava", loan, months=shp_months, ribit=ribit, madad=106.7, figures=figures_prime)

prime_shp.update(loan=loan, months=shp_months, ribit=ribit, madad=106.7)
prime_krn.update(loan=loan, months=krn_months, ribit=ribit, madad=106.7)

## Mishtana
fig_mish1 = figure_factory().get_figture("left loan")
fig_mish2 = figure_factory().get_figture("monthly payment")
figures_mish = [fig_mish1, fig_mish2]

mish_shp = Maslul("shpitzer", loan, months=shp_months, ribit=ribit, madad=106.7, figures=figures_mish)
mish_krn = Maslul("keren_shava", loan, months=krn_months, ribit=ribit, madad=106.7, figures=figures_mish)

mish_shp.update(loan=loan, months=shp_months, ribit=ribit, madad=106.7)
mish_krn.update(loan=loan, months=krn_months, ribit=ribit, madad=106.7)


class MaslusSliders:
    def __init__(self):
        # configure Sliders
        self.ribit_slider = Slider(title="ribit", value=ribit, start=0.0, end=5.0, step=0.01)
        self.ks_years_slider = Slider(title="keren shava years", value=20.0, start=1.0, end=30.0, step=1)
        self.shp_years_slider = Slider(title="shpitzer years", value=20.0, start=1.0, end=30.0, step=1)
        self.loan_slider = Slider(title="loan", value=400000.0, start=0.0, end=700000.0, step=1000)
        self.loan_slider.width = 700

    def get_sliders(self):
        return column(self.loan_slider, self.ribit_slider, self.ks_years_slider,
              self.shp_years_slider)

    def update_on_change_callbaks(self, function):
        self.ribit_slider.on_change('value', function)
        self.ks_years_slider.on_change('value', function)
        self.shp_years_slider.on_change('value', function)
        self.loan_slider.on_change('value', function)



total_monthly_sum = [kalatz_shp.shita.get_monthly_total()[0] + prime_shp.shita.get_monthly_total()[0] + mish_shp.shita.get_monthly_total()[0]]
source_total_monthly_sum = ColumnDataSource(dict(x=[0], y=[0], text=["Shpitzer total: " + str(total_monthly_sum[0])]))
glyph = Text(x=100, y=50, text="text", angle=0.0, text_color="red", name='source_total_monthly_sum')
tota_fig = figure(background_fill_color='white',
                   background_fill_alpha=0.5,
                   border_fill_color=None,
                   border_fill_alpha=0.25,
                   plot_height=100,
                   plot_width=400,
                   title='total',
                   title_location=None
                   )
tota_fig.axis.visible = False
tota_fig.toolbar.logo = None
tota_fig.toolbar_location = None
tota_fig.xgrid.grid_line_color = None
tota_fig.ygrid.grid_line_color = None
tota_fig.add_glyph(source_total_monthly_sum, glyph)

def update_data_kltz(attrname, old, new):
    print("ITAY args are attrname, old, new = ",attrname, old, new)
    # Get the current slider values
    r = kltz_sliders.ribit_slider.value
    ks_y = kltz_sliders.ks_years_slider.value
    shp_y = kltz_sliders.shp_years_slider.value
    loan_val = kltz_sliders.loan_slider.value

    # Generate the new curve
    kalatz_shp.update(loan=loan_val, months=(shp_y*12), ribit=r, madad=106.7)
    kalatz_krn.update(loan=loan_val, months=(ks_y*12), ribit=r, madad=106.7)

    total_monthly_sum = [kalatz_shp.shita.get_monthly_total()[0] + prime_shp.shita.get_monthly_total()[0] +
                         mish_shp.shita.get_monthly_total()[0]]
    source_total_monthly_sum.data = dict(x=[0], y=[0], text=["total: " + str(total_monthly_sum[0])])


def update_data_prime(attrname, old, new):
    print("ITAY args are attrname, old, new = ", attrname, old, new)
    # Get the current slider values
    r = prime_sliders.ribit_slider.value
    ks_y = prime_sliders.ks_years_slider.value
    shp_y = prime_sliders.shp_years_slider.value
    loan_val = prime_sliders.loan_slider.value

    # Generate the new curve
    prime_shp.update(loan=loan_val, months=(shp_y*12), ribit=r, madad=106.7)
    prime_krn.update(loan=loan_val, months=(ks_y*12), ribit=r, madad=106.7)

    total_monthly_sum = [kalatz_shp.shita.get_monthly_total()[0] + prime_shp.shita.get_monthly_total()[0] +
                         mish_shp.shita.get_monthly_total()[0]]
    source_total_monthly_sum.data = dict(x=[100], y=[100], text=total_monthly_sum)


def update_data_mish(attrname, old, new):
    print("ITAY args are attrname, old, new = ", attrname, old, new)
    # Get the current slider values
    r = mish_sliders.ribit_slider.value
    ks_y = mish_sliders.ks_years_slider.value
    shp_y = mish_sliders.shp_years_slider.value
    loan_val = mish_sliders.loan_slider.value

    # Generate the new curve
    mish_shp.update(loan=loan_val, months=(shp_y*12), ribit=r, madad=106.7)
    mish_krn.update(loan=loan_val, months=(ks_y*12), ribit=r, madad=106.7)

    total_monthly_sum = [kalatz_shp.shita.get_monthly_total()[0] + prime_shp.shita.get_monthly_total()[0] +
                         mish_shp.shita.get_monthly_total()[0]]
    source_total_monthly_sum.data = dict(x=[100], y=[100], text=total_monthly_sum)


class MaslulGraphic:
    def __init__(self):
        # self.maslul_id = maslul_id
        fig1 = figure_factory().get_figture("left loan")
        fig2 = figure_factory().get_figture("monthly payment")
        self.figures = [fig1, fig2]
        self.m_shp = Maslul("shpitzer", loan, months=shp_months, ribit=ribit, madad=106.7, figures=self.figures)
        self.m_krn = Maslul("keren_shava", loan, months=shp_months, ribit=ribit, madad=106.7, figures=self.figures)


        self.m_shp.update(loan=loan, months=shp_months, ribit=ribit, madad=106.7)
        self.m_krn.update(loan=loan, months=krn_months, ribit=ribit, madad=106.7)

        self.m_sliders = MaslusSliders()

        def _update_data_handler(attrname, old, new):
            # Get the current slider values
            r = self.m_sliders.ribit_slider.value
            ks_y = self.m_sliders.ks_years_slider.value
            shp_y = self.m_sliders.shp_years_slider.value
            loan_val = self.m_sliders.loan_slider.value

            # Generate the new curve
            self.m_shp.update(loan=loan_val, months=(shp_y * 12), ribit=r, madad=106.7)
            self.m_krn.update(loan=loan_val, months=(ks_y * 12), ribit=r, madad=106.7)

            # total_monthly_sum = [kalatz_shp.shita.get_monthly_total()[0] + prime_shp.shita.get_monthly_total()[0] +
            #                      mish_shp.shita.get_monthly_total()[0]]
            # source_total_monthly_sum.data = dict(x=[100], y=[100], text=total_monthly_sum)

        self.m_sliders.update_on_change_callbaks(_update_data_handler)

'''
kltz_sliders = MaslusSliders(update_data_kltz)
prime_sliders = MaslusSliders(update_data_prime)
mish_sliders = MaslusSliders(update_data_mish)

kltz_inputs = kltz_sliders.get_sliders()
prime_inputs = prime_sliders.get_sliders()
mish_inputs = mish_sliders.get_sliders()
'''
masluls = []
maslul_id = 0
def add_maslul_handler():
    masluls.append(MaslulGraphic())
    m = masluls[-1]
    curdoc().add_root(column(m.m_sliders.get_sliders(), row(m.figures[0], m.figures[1], width=800)))

add_maslul_button = Button(label="add maslul", button_type="success")
add_maslul_button.on_click(add_maslul_handler)

curdoc().add_root(column(add_maslul_button))
