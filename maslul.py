import keren_shava as ks
import shpitzer as shp
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Text, Button

## initial params
loan = 0
ribit = 0.001
krn_year = 1
shp_year = 1
krn_months = 12 * krn_year
shp_months = 12 * shp_year

### global params
masluls = []

## total sum data ##
total_monthly_sum_shp = [0]
total_monthly_sum_krn = [0]
source_total_monthly_sum_shp = ColumnDataSource(dict(x=[0], y=[0], text=["Shpitzer total: " + str(total_monthly_sum_shp[0])]))
source_total_monthly_sum_krn = ColumnDataSource(dict(x=[0], y=[0], text=["keren shava total: " + str(total_monthly_sum_krn[0])]))
glyph_shp = Text(x=0, y=50, text="text", angle=0.0, text_color="blue", name='source_total_monthly_sum_shp')
glyph_krn = Text(x=0, y=50, text="text", angle=0.0, text_color="green", name='source_total_monthly_sum_krn')

glyph_shp.text_font_size = '11pt'
glyph_krn.text_font_size = '11pt'

total_fig_shp = figure(background_fill_color='white',
                   background_fill_alpha=0.5,
                   border_fill_color=None,
                   border_fill_alpha=0.25,
                   plot_height=50,
                   plot_width=400,
                   title='total',
                   title_location=None
                   )

total_fig_krn = figure(background_fill_color='white',
                   background_fill_alpha=0.5,
                   border_fill_color=None,
                   border_fill_alpha=0.25,
                   plot_height=50,
                   plot_width=400,
                   title='total',
                   title_location=None
                   )
total_fig_shp.axis.visible = False
total_fig_shp.toolbar.logo = None
total_fig_shp.toolbar_location = None
total_fig_shp.xgrid.grid_line_color = None
total_fig_shp.ygrid.grid_line_color = None
total_fig_shp.add_glyph(source_total_monthly_sum_shp, glyph_shp)

total_fig_krn.axis.visible = False
total_fig_krn.toolbar.logo = None
total_fig_krn.toolbar_location = None
total_fig_krn.xgrid.grid_line_color = None
total_fig_krn.ygrid.grid_line_color = None
total_fig_krn.add_glyph(source_total_monthly_sum_krn, glyph_krn)


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
             tools=["hover", "pan", "box_zoom", "wheel_zoom", "reset"])
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
                   tools=["hover", "pan", "box_zoom", "wheel_zoom", "reset"])
        else:
            raise KeyError("ERROR figure_factory: [get_figture] no such figure_type {}. please choose one of {}".format(figure_type, self.figures_types))


class MaslusSliders:
    def __init__(self):
        # configure Sliders
        self.ribit_slider = Slider(title="ribit", value=ribit, start=0.0, end=5.0, step=0.01)
        self.ks_years_slider = Slider(title="keren shava years", value=00.0, start=1.0, end=30.0, step=1)
        self.shp_years_slider = Slider(title="shpitzer years", value=00.0, start=1.0, end=30.0, step=1)
        self.loan_slider = Slider(title="loan", value=000000.0, start=0.0, end=700000.0, step=1000)
        self.loan_slider.width = 700

    def get_sliders(self):
        return column(self.loan_slider, self.ribit_slider, self.ks_years_slider,
              self.shp_years_slider)

    def update_on_change_callbaks(self, function):
        self.ribit_slider.on_change('value', function)
        self.ks_years_slider.on_change('value', function)
        self.shp_years_slider.on_change('value', function)
        self.loan_slider.on_change('value', function)


class MaslulGraphic:
    def __init__(self):
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

            total_monthly_sum_shp = [0]
            total_monthly_sum_krn = [0]
            for m in masluls:
                total_monthly_sum_shp[0] += m.m_shp.shita.get_monthly_total()[0]
                total_monthly_sum_krn[0] += m.m_krn.shita.get_monthly_total()[0]
            source_total_monthly_sum_shp.data = dict(x=[100], y=[100], text=["Shpitzer total: " + str(round(total_monthly_sum_shp[0], 2))])
            source_total_monthly_sum_krn.data = dict(x=[100], y=[100], text=["keren shava total: " + str(round(total_monthly_sum_krn[0], 2))])

        self.m_sliders.update_on_change_callbaks(_update_data_handler)

def add_maslul_handler():
    if masluls.__len__() > 10:
        print("can not adding more then 20 masluls.")
        return
    masluls.append(MaslulGraphic())
    m = masluls[-1]
    curdoc().add_root(column(m.m_sliders.get_sliders(), row(m.figures[0], m.figures[1], width=800)))

add_maslul_button = Button(label="add maslul +", button_type="success")
add_maslul_button.on_click(add_maslul_handler)

curdoc().add_root(column(row(total_fig_shp, total_fig_krn)))
curdoc().add_root(column(add_maslul_button))
