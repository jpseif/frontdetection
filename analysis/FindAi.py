import numpy as np
import math as m
import re
# Find the Ai values for the different measurements
# limit = 0.000001
# limit_iter = 100
# AiPercentage = 0.0001

# Find the Ai value
def Find_data(sel_data_list, index):

    # x data
    xdata = sel_data_list[index].nxc_from_PL()
    xdata[np.isnan(xdata)] = 0
    max_xdata = max(xdata)
    iu, = np.where(xdata == max_xdata)

    # y data
    ydata = sel_data_list[index].tau_eff(nxc=sel_data_list[index].nxc_from_PL())

    ydata_max_x = ydata[iu[0]]

    xdata_before = xdata[:iu[0]-1]
    xdata_before = xdata_before[::-1] # reversed
    # normalize xdata
    xdata_before[:] = [x / max_xdata for x in xdata_before]
    ydata_before = ydata[:iu[0]-1]
    ydata_before = ydata_before[::-1] # reversed
    # normalize ydata to the lifetime at the maximum point
    ydata_before[:] = [x / ydata_max_x for x in ydata_before]

    xdata_before = xdata_before[:10]
    ydata_before = ydata_before[:10]

    xdata_after = xdata[iu[0]+1:]
    # normalize xdata
    xdata_after[:] = [x / max_xdata for x in xdata_after]
    ydata_after = ydata[iu[0]+1:]
    # normalize ydata to the lifetime at the maximum point
    ydata_after[:] = [x / ydata_max_x for x in ydata_after]

    xdata_after = xdata_after[:10]
    ydata_after = ydata_after[:10]

    return xdata_before, ydata_before, xdata_after, ydata_after

def FitData(xb, yb, xa, ya):

    # do a linear fit for the data before and after the maximum PL
    fit_b = np.polyfit(xb, yb, 1)
    fit_a = np.polyfit(xa, ya, 1)
    fit_fb = np.poly1d(fit_b)
    fit_fa = np.poly1d(fit_a)
    # absolute difference of the slopes (FIGURE TO BE MINIMIZED)
    dm = abs(abs(fit_b[0]) - abs(fit_a[0]))
    # print("Abs difference m (from FitData): " + str(dm))

    return dm

def Newton_dm(sel_data_list, sel_dataname_list, lim, lim_iter):

    Ai_values = []
    value_found = False
    dm_final = 0
    Ai_final = 0

    # guess the starting value
    # Sample_Gain = [1, 2, 3, 4, 5, 6, 7, 8, 9] each of them corresponds to one
    # initial Ai_guess.
    Ai_guess = [24, 23, 22, 21, 20, 19, 18, 17, 16]

    for t in np.arange(len(sel_data_list)):

        for j in np.arange(1, lim_iter):

            if j == 1:
                # use the file name to find the sample gain
                regex = re.search('[S]([0-9])', sel_dataname_list[t])
                gain = regex.group(0)
                gain = int(gain[-1:])
                Ai_start = Ai_guess[gain - 1]
                # generate range of log10(Ai) values around the current value
                Ai_range = np.arange(Ai_start-0.02, Ai_start+0.03, 0.01)
            else:
                # generate range of log10(Ai) values around the current value
                Ai_range = np.arange(Ai_new-0.02, Ai_new+0.03, 0.01)

            # initialize an array to store the dm data
            dm_val = []
            # start a loop to calculate the dm values
            for n, val in enumerate(Ai_range, 1):

                # set the next Ai value from Ai_range
                sel_data_list[t].Ai = np.power(10, val)
                # get the current lifetime data
                xb, yb, xa, ya = Find_data(sel_data_list, t)
                xb[np.isnan(xb)] = 0
                yb[np.isnan(yb)] = 0
                xa[np.isnan(xa)] = 0
                ya[np.isnan(ya)] = 0

                # print(sel_dataname_list[t])
                # print("Ai: ", np.power(10, val))
                # print("log10(Ai): ", val)
                # print("xb: ", xb)
                # print("xa: ", xa)
                # print("yb: ", yb)
                # print("ya: ", ya)
                # fit the data to get dm
                dm = FitData(xb, yb, xa, ya)
                # print("dm: ", dm)
                # at the middle of the Ai_range check if dm < lim
                # if it is break the loop
                if dm < lim:
                    value_found = True
                    dm_final = dm
                    Ai_final = val
                    Ai_values.append(round(val,2))
                    break
                dm_val.append(dm)

            if not value_found:
                # if the value is not found continue here
                fit_dm = np.polyfit(Ai_range, dm_val, 1)
                Ai_new = -fit_dm[1]/fit_dm[0]

            if value_found:
                # print("Value found after " + str(j) + " iterations.")
                # print("The final dm value is: " + str(dm_final))
                # print("The Ai for " + sel_dataname_list[t] + " is " + str(Ai_final))
                break

            if j == lim_iter:
                # if no Ai value is found set log10(Ai) to 16
                Ai_values.append(16)
                break

        print(sel_dataname_list[t], ":", round(Ai_final,2))
        # print("")
        value_found = False

    return Ai_values
