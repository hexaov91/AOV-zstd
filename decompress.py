from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict
import os
import zipfile
import re
from os import walk
from os.path import join
import pathlib
import zstd
import zstandard
import time
success= 0
fail =0
deleatlist=[]
os.chdir(os.getcwd())
print(os.getcwd())

InputPath='input'
OutputPath='output'
dictPath=r'dict'
with open(dictPath, 'rb') as f:
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


def de_compress_file(f, mode=False):
	
	methods = get_methods(f.read(4), mode)
	lens = int.from_bytes(f.read(4), byteorder='little')
	data = f.read(lens)
	for func, argus in methods:
		if func is None:
			raise ('error:')
		instant = func(**argus)
		data = instant.decompress(data)
	return data


def de_compress_folder(inp, out, mode=False):
	global success
	global fail
	inp = modifypath(inp, os.path.sep)
	out = modifypath(out, os.path.sep)
	for path, _, file_names in os.walk(inp):
		output_path = out + path[len(inp):]
		makedir(output_path)
		for file_name in file_names:
			input_path = path + os.path.sep + file_name
			with open(input_path, 'rb') as f:
				with open(output_path + os.path.sep + file_name, 'wb') as of:
					try:
						of.write(de_compress_file(f, mode))
						success +=1
					except TypeError as e:
						deleatlist.append(output_path + os.path.sep + file_name)
						fail +=1

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
				
input=InputPath
output=OutputPath

start = time.time()
unpackpkg(input)
de_compress_folder(input,output)

for delfile in deleatlist:
 os.remove(delfile)
 with open(delfile + 'error' , 'w') as of:
   of.write('error')
 with open(r'error.log', 'a') as f:
    f.writelines(delfile+'\n')
   
end = time.time()   
print("解壓了"+ str(success) + f"個文件 於 {end - start} 秒,真的太星爆了")
   
   
   