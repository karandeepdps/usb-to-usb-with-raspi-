import os,glob,shutil

while True:
	drive_list = os.listdir('/media/pi/.' )
	if(len(drive_list)==2):
		break
	print("Waiting for pendrives to connect")

destination = "/media/pi/"+drive_list[1]+"/"

usba=[]
usbb=[]

for i, drive_name in enumerate( drive_list ):
	
	for j, files_path in enumerate( glob.glob( '/media/pi/'+drive_name+'/*' ) ):
		
		if(i==0):
			usba.append(files_path)
		if(i==1):
			usbb.append(files_path)
		print(i, files_path )

#print(usba)
#print(usbb)

for i, names in enumerate(usba):
	print("Copying"+names)
	os.system('cp -r '+ "'"+names+"' " + destination)
	#if os.path.isdir(names):
	#	shutil.copytree(names,'/home/pi/dump/',symlinks,ignore)
	#else:
	#	shutil.copy2(names,'/home/pi/dump/')

	