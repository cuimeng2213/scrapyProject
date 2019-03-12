import os

def main():
	img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
	print("#####: ", img_path)
	if os.path.exists(img_path):
		print("exists")
	else:
		print("not exists")
		#os.mkdir(img_path)

if __name__ == '__main__':
	main()