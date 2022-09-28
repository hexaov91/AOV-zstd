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



import codecs
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures

success= 0
fail =0

deleatlist=[]
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



def de_compress_file(data, len):

	dctx = zstandard.ZstdDecompressor(dict_data=dict_data)
	decompressed = dctx.decompress(data)
	return decompressed


d1=[]
d2=[]
def de_compress_folder(inp, out, mode=False):

	inp = modifypath(inp, os.path.sep)
	out = modifypath(out, os.path.sep)
	for path, _, file_names in os.walk(inp):
		output_path = out + path[len(inp):]
		makedir(output_path)
		for file_name in file_names:
			input_path = path + os.path.sep + file_name
			output_path=out + path[len(inp):] + os.path.sep + file_name
			d1.append(input_path)
			d2.append(output_path)

	with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
	  executor.map(third, d1,d2)

def third(input_path, output_path):
	global success
	global fail
	with open(input_path, 'rb') as f:
		tmp=f.read()
		header=tmp[0:4]
		lens=tmp[4:8]
		data=tmp[8:]
		with open(output_path, 'wb') as of:
			if header == b'\x22\x4a\x00\xef':
				try:
					of.write(de_compress_file(data, lens))
					success +=1
				except TypeError as e:
					deleatlist.append(output_path)
					fail +=1

			elif header == b'\x22\x4a\x67\x00':
				#try:
					#of.write(decrypt_file(input_path,data))
					#success +=1
				#except TypeError as e:
					deleatlist.append(output_path)
					fail +=1

			else:
				print("未知類型",input_path,header)




def unpackpkg(input):
	u1=[]
	u2=[]
	pkgpath=input
	for root, dirs, files in walk(pkgpath):
		for f in files:
			fullpath = join(root, f)
			pkg = pathlib.Path(fullpath)
			if ''.join(pkg.suffixes) == '.pkg.bytes' :
				u2.append(fullpath)
			else:
				pass
	with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
		executor.map(unpackpkgThird,u2)
	print("unpack End")

def unpackpkgThird(fullpath):
     with zipfile.ZipFile(fullpath, 'r') as zip_ref:
      zip_ref.extractall(os.path.dirname(fullpath))
      zip_ref.close()
      os.remove(fullpath)	
      



input='待工作區'
output='Output'

start = time.time()
unpackpkg(input)
de_compress_folder(input,output)
#os.remove('error.log')
   
end = time.time()   
print("解壓了"+ str(success) + f"個文件 於 {end - start} 秒,真的太星爆了")


   

   
