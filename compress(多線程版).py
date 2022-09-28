from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict
import os
import zipfile
import re
from os import walk
from os.path import join
import pathlib
import zstd
import zstandard
import binascii
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
success= 0
fail =0
deleatlist=[]
worlist1=[]
worlist2=[]
worlist3=[]
worlist4=[]
worlist5=[]
os.chdir(os.path.dirname(__file__))
os.chdir(os.getcwd())
print(os.getcwd())

with open(r'DS', 'rb') as f:
	dict_data = f.read()
dict_data = ZstdCompressionDict(dict_data)
del f

ZSTD_DECOMPRESS_INSTANT = ZstdDecompressor
ZSTD_COMPRESS_INSTANT = ZstdCompressor
Zstd_METHOD_MAPPING = {239: ((ZstdDecompressor, {'dict_data': dict_data}), (ZstdCompressor, {'dict_data': dict_data})), 103: ((None, None), (None, None))}


def modifypath(path, split='/'):
	path = path.replace('\\', split)
	if path[-1] != split:
		path = path + split
	return path


def makedir(path):
	if os.path.exists(path) is False:
		os.makedirs(path)


def get_methods(data, mode=False):
	methods = []
	if data[:2] != b'"J':
		return
	for i in data[2:]:
		if i:
			methods.append(Zstd_METHOD_MAPPING[i][mode])
	return methods


def de_compress_file(input_path,ossep,file_name,output_path,dict ):  
	global success

	dict = ZstdCompressionDict(dict_data)	
	cctx = zstandard.ZstdCompressor(level=22,dict_data=dict)
#	print(input_path,ossep,file_name,output_path)


	with open(input_path, 'rb') as f:			
		data=f.read()				
		with open(output_path + ossep + file_name, 'wb') as of:
				compressed = cctx.compress(data)
				size=int(len(data))
				int_bytes = size.to_bytes(4, 'little')  
				lead = b'\x22\x4A\x00\xEF' + int_bytes + compressed
				of.write(lead)
				success +=1
				


	
	return lead
	


def de_compress_folder(inp, out, mode=False):
	inp = modifypath(inp, os.path.sep)
	out = modifypath(out, os.path.sep)
	for path, _, file_names in os.walk(inp):
		output_path = out + path[len(inp):]
		makedir(output_path)
		for file_name in file_names:
			input_path = path + os.path.sep + file_name
			worlist1.append(input_path)
			worlist3.append(os.path.sep)
			worlist4.append(file_name)
			worlist5.append(output_path)	
	


def unpackpkg(input):
 pkgpath=input
 for root, dirs, files in walk(pkgpath):
  for f in files:
    fullpath = join(root, f)
    pkg = pathlib.Path(fullpath)
    if ''.join(pkg.suffixes) == '.pkg.bytes' :
     with zipfile.ZipFile(fullpath, 'r') as zip_ref:
      zip_ref.extractall(os.path.dirname(fullpath))
      zip_ref.close()
      os.remove(fullpath)				

def download_all(worlist1,worlist3,worlist4,worlist5,dict_data):
	
	with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
		
		executor.map(de_compress_file, worlist1,worlist3,worlist4,worlist5,dict_data)
		

input=r'待工作區'
output=r'Output'
start = time.time()

unpackpkg(input)
de_compress_folder(input,output)
with open(r'DS', 'rb') as f:
	dict_data = f.read()
	download_all(worlist1,worlist3,worlist4,worlist5,dict_data)	


for delfile in deleatlist:
 os.remove(delfile)
 with open(delfile + 'error' , 'w') as of:
   of.write('error')
   
os.chdir(os.getcwd()+'/'+'output/Ages/Prefab_Characters/Prefab_Hero')
path = "Prefab_Hero"
pathlist= os.listdir()
for fold in pathlist:
 z = zipfile.ZipFile('Actor_'+fold[0:3]+'_Actions.pkg.bytes', 'w', zipfile.ZIP_STORED)
 startdir =fold
 print(startdir)
 for dirpath, dirnames, filenames in os.walk(startdir):
  for filename in filenames:
   z.write(os.path.join(dirpath, filename))
 z.close()

end = time.time()   
print("壓縮了"+ str(success) + f"個文件 於 {end - start} 秒,真的太星爆了")
