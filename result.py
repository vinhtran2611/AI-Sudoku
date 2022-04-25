# importing library
import matplotlib.pyplot as plt

# function to add value labels
def addlabels(x,y):
	for i in range(len(x)):
		plt.text(i, y[i], y[i], ha = 'center')

if __name__ == '__main__':
	
	# creating data on which bar chart will be plot
	x = ["DFS", "BFS", "Greedy", "A*"]
	y = [2.18, 8.17, 1.26, 1.26]
	
	# setting figure size by using figure() function
	plt.figure(figsize = (10, 5))
	
	# making the bar chart on the data
	plt.bar(x, y)
	
	# calling the function to add value labels
	addlabels(x, y)
	
	# giving title to the plot
	plt.title("Average times")
	
	# giving X and Y labels
	plt.xlabel("Alogrithms")
	plt.ylabel("Running time(minutes)")
	
	# visualizing the plot
	plt.show()
