app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='r')
X_axis = numpy.linspace(0,100,12800)
#'data' is my required y_axis containing 12800 values
ydata = np.array_split(data,50)
xdata = np.array_split(X_axis,50)
ptr = 0
def update():
    global curve, data, ptr, p6
    curve.setData(xdata[ptr%50],ydata[ptr%50])
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)
