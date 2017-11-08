import matplotlib.pyplot as plt
from utils_general import Data2DTraj


class LineplotDynamic:
	def __init__(self, label_x, label_y, title, adjust_right=None):
		self.fig, self.ax = plt.subplots(1, 1)
		if adjust_right:
			self.fig.subplots_adjust(right=adjust_right)
		self.ax.set_xlabel(label_x)
		self.ax.set_ylabel(label_y)
		plt.title(title)
		plt.ion()

		self.hl_dict = dict()
		self.data_dict = dict()
		self.filled_lines_dict = dict()

	def append_data_and_plot(self, hl_name, x_new, y_new, y_stdev_new):
		cur_hl = self.hl_dict[hl_name]
		cur_data = self.data_dict[hl_name]

		cur_data.appendToTraj(x=x_new, y_mean=y_new, y_stdev=y_stdev_new)
		cur_hl.set_xdata(cur_data.x_traj)
		if self.filled_lines_dict[hl_name] is not None:
			self.filled_lines_dict[hl_name].remove()
		self.filled_lines_dict[hl_name] = self.ax.fill_between(cur_data.x_traj, cur_data.y_lower_traj, cur_data.y_upper_traj, facecolor=cur_hl.get_color(), alpha=0.3)
		cur_hl.set_ydata(cur_data.y_mean_traj)

	def update(self, hl_name, x_new, y_new, y_stdev_new=0, label='', init_at_origin=False):
		plt.sca(self.ax)

		# New plot handle
		if not hl_name in self.hl_dict:
			hl_new, = plt.plot(x_new, y_new, label=label)
			self.hl_dict[hl_name] = hl_new
			self.data_dict[hl_name] = Data2DTraj()
			self.filled_lines_dict[hl_name] = None

			if init_at_origin:
				self.append_data_and_plot(hl_name=hl_name, x_new=0, y_new=0, y_stdev_new=0)
			plt.legend(handles=list(self.hl_dict.values()), loc='center left', bbox_to_anchor=(1, 0.5), frameon=True)

		self.append_data_and_plot(hl_name=hl_name, x_new=x_new, y_new=y_new, y_stdev_new=y_stdev_new)

		self.ax.relim()
		self.ax.autoscale_view()
		self.fig.canvas.draw()
		plt.pause(0.00001)