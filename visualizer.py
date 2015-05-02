import csv
import itertools
import string
import random
import json

class Visualizer:
	def __init__(self, filename):
		adj_mat = []
		with open(filename, 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				adj_mat += [row]
		self.adj_mat = adj_mat

	def transform_adjmat(self):
		G = {'links': [], 'nodes': []}
		n = len(self.adj_mat[0])
		key_links = ('source', 'target', 'value')
		key_nodes = {'group', 'name'}
		for i, row in enumerate(self.adj_mat):
			G['nodes'].append(dict(zip(key_nodes,
				(1, 'n{0}'.format(i)))))
			for j, item in enumerate(row):
				G['links'].append(dict(zip(key_links, (i, j, item))))
		return G

	def write_json(self, G):
		uniq_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
		with open('user_data/' + str(uniq_id), mode='w') as f:
			json.dump(G, f)
		return uniq_id