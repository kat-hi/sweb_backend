# calculating coordinates of the trees
import math


def calc_row(lat, long, number_of_trees, n):
	if n == number_of_trees:
		return
	lat1 = lat * math.pi / 180
	lng1 = long * math.pi / 180
	brng = 2.3038346
	d = 0.01
	R = 6371

	lat2 = round(math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1) * math.sin(d / R) * math.cos(brng)), 7)
	lng2 = round(lng1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
								   math.cos(d / R) - math.sin(lat1) * math.sin(lat2)), 7)
	print(lat2 * 180 / math.pi, lng2 * 180 / math.pi)

	# write file
	with open('reihe19.txt', 'a+') as f:
		if n == 0:
			f.write(str(long) + ', ' + str(lat) + '\n')
		f.write(str(lng2 * 180 / math.pi) + ', ' + str(lat2 * 180 / math.pi) + '\n')
	n += 1
	calc_row(lng2 * 180 / math.pi, lat2 * 180 / math.pi, number_of_trees, n)


calc_row(13.2637197, 52.8706047, 29, 0)


def calc_new_row_start():
	lat1 = 52.870330 * math.pi / 180  # take param from calc_row as lat1
	lng1 = 13.266005 * math.pi / 180  # take param from calc_row as lat1
	brng = 0.418879
	d = 0.01
	R = 6371
	lat2 = round(math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1) * math.sin(d / R) * math.cos(brng)), 7)
	lng2 = round(lng1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
								   math.cos(d / R) - math.sin(lat1) * math.sin(lat2)), 7)
	print("new row", lat2 * 180 / math.pi, lng2 * 180 / math.pi)


calc_new_row_start()
