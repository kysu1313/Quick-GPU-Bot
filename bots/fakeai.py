
'''
Portions of this code were used from: 
https://github.com/guilhermebferreira/selenium-notebooks/blob/master/Mouse%20move%20by%20b-spline%20interpolation.ipynb

Thanks to guilhermebferreira
'''

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import scipy.interpolate as si
from time import sleep
import numpy as np
import time
import os


class FakeAI():
    def __init__(self, driver):
        self.driver = driver
        self.x_i = 0
        self.y_i = 0
        self.__get_lin_curves()

    def __get_lin_curves(self):
        points = [[-6, 2], [-3, -2],[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 5], [8, 8], [6, 8], [5, 9], [7, 2]];
        points = np.array(points)
        x = points[:,0]
        y = points[:,1]
        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)
        x_tup = si.splrep(t, x, k=3)
        y_tup = si.splrep(t, y, k=3)
        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]
        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]
        self.x_i = si.splev(ipl_t, x_list)
        self.y_i = si.splev(ipl_t, y_list)

    def move_cursor(self, element):
        action =  ActionChains(self.driver);
        #First, go to your start point or Element
        time.sleep(1) 
        action.move_to_element(element);
        time.sleep(1) 
        action.perform();

        for mouse_x, mouse_y in zip(self.x_i, self.y_i):
            action.move_by_offset(mouse_x,mouse_y);
            action.perform();
            sleep(0.1)
            print(mouse_x, mouse_y)


#if __name__ == '__main__':
#    tmp = Human()
#    tmp.pretend_to_be_human()