import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np

class DataPlot:

    def __init__(self, vmdata, datafile_name):
        """
        Define the data contained in the object and the plot name
        """
        self.data = vmdata
        self.datafile_name = datafile_name
        # self.fpath =

    def plot_fig(self):
        """
        Plot the data
        """

        # define the cropping slider
        crop = widgets.FloatRangeSlider(
            min=0.,
            max=1.,
            value=[0.05,0.6],
            step=0.01,
            continuous_update=True,
            description='crop range'
        )

        # define the binning slider
        b = widgets.IntSlider(
            min=1,
            max=100,
            value=5,
            step=1,
            continuous_update=True,
            description='binning'
        )

        # define the figure and axis
        fig, ax  = plt.subplots()

        # check if the ref data is inversed. if the mean is negative, inverse it.
        if np.mean(self.data.data()['ref']) < 0:
            self.data.data()['ref'] = -1*self.data.data()['ref']

        # input the data into the figure (PL and ref)
        PL_line,  = ax.plot(self.data.data()['t'], self.data.data()['PL'], '.', label='PL')
        ref_line, = ax.plot(self.data.data()['t'], self.data.data()['ref'], '.', label='ref')

        # plot the data in semilog, set a title and insert the legend
        plt.semilogy()
        plt.title(self.datafile_name)
        plt.legend()

        # define the function to update the plot
        def update_plot():

            self.data.crop_start = crop.value[0]
            self.data.crop_end = crop.value[1]
            self.data.binn = b.value

            PL_line.set_xdata(self.data.data()['t'])
            PL_line.set_ydata(self.data.data()['PL'])
            ref_line.set_xdata(self.data.data()['t'])
            ref_line.set_ydata(self.data.data()['ref'])

            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()

        crop.on_trait_change(update_plot, 'value')
        b.on_trait_change(update_plot, 'value')

        display(crop,b)
        update_plot()
