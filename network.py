import igraph
import numpy

class Network:
	def __init__(self, filename):
		self.graph = igraph.Graph.Read_Adjacency(filename, mode='UNDIRECTED')

	def median_degree(self):
		degrees = self.graph.degree()
		degrees.sort()
		return degrees[len(degrees) / 2]

	def assortativity(self, degrees=None):
		if degrees is None: degrees = self.graph.degree()
		degrees_sq = [deg**2 for deg in degrees]
 
		m = float(self.graph.ecount())
		num1, num2, den1 = 0, 0, 0
		for source, target in self.graph.get_edgelist():
			num1 += degrees[source] * degrees[target]
			num2 += degrees[source] + degrees[target]
			den1 += degrees_sq[source] + degrees_sq[target]
		num1 /= m
		den1 /= 2*m
		num2 = (num2 / (2*m)) ** 2
		return (num1 - num2) / (den1 - num2)

	def global_efficiency(self):
		shortest_paths = self.graph.shortest_paths_dijkstra()
		total = 0
		count = 0
		for i in shortest_paths:
			for j in i:
				if j != 0:
					total += 1 / float(j)
					count += 1
		return total / float(count)

	def optimal_modularity(self):
		modularity_structure = self.graph.community_fastgreedy()
		modularity_clustering = modularity_structure.as_clustering()
		modularity_score = self.graph.modularity(modularity_clustering)
		return modularity_score

	def closeness(self):
		closeness_all = self.graph.closeness()
		avg_closeness = numpy.mean(closeness_all)
		var_closeness = numpy.var(closeness_all)
		return avg_closeness, var_closeness

	def compute(self):
		med_deg = self.median_degree()
		assort = self.assortativity()
		efficiency = self.global_efficiency()
		transitivity = self.graph.transitivity_undirected()
		optimal_modularity = self.optimal_modularity()
		avg_closeness, var_closeness = self.closeness()

		return [med_deg, assort, efficiency, transitivity, optimal_modularity,
		        avg_closeness, var_closeness]

