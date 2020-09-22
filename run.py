from nav import Map

def run():
	n_points = int(input("No of points : ")) # 400
	length = int(input("Enter length : ")) # 10
	width = int(input("Enter width : ")) # 8

	m_map = Map()

	t_start = m_map.defineStart()

	t_dest = m_map.defineDestination()

	m_map.bakePath(n_points, length, width)
	# m_map.showAllConnections(m_map)
	# m_map.showStart()

	start = m_map.findStart() # Index of starting point
	dest = m_map.findDestination() # Index of destination point
	# dest = 0 # Index of destination point

	path = m_map.getPathNew(start, dest)
	m_map.showPath(path)


run()
