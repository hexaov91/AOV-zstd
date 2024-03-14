import os
import zipfile
from os import walk
from os.path import join
import pathlib
import zstandard as zstd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures

from NGameRes import NGameResRW

success= 0
fail =0
deleatlist=[]

os.chdir(os.getcwd())
print(os.getcwd())

Decoder=NGameResRW().DecodeFile
Encoder=NGameResRW().EncodeFile

d1=[]
d2=[]


def modifypath(path, split='/'):
	path = path.replace('\\', split)
	if path[-1] != split:
		path = path + split
	return path

def makedir(path):
	if os.path.exists(path) is False:
		os.makedirs(path)


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
        executor.map(unpackpkgWork,u2)
    print("unpack End")

def unpackpkgWork(fullpath):
     with zipfile.ZipFile(fullpath, 'r') as zip_ref:
      zip_ref.extractall(os.path.dirname(fullpath))
      zip_ref.close()
      os.remove(fullpath)    
      
def WorkFolder(inp, out):
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
      executor.map(tmpWorker, d1,d2)


def tmpWorker(input_path, output_path):
    global success
    global fail

    with open(output_path, 'wb') as of:
        deData=Decoder(input_path)
        of.write(deData)
        success +=1

input='待工作區'
output='Output'

start = time.time()
unpackpkg(input)
WorkFolder(input,output)
#os.remove('error.log')
#tmpWorker("待工作區/Prefab_Characters/Prefab_Hero/105_LianPo/105_lianpo_actorinfo.bytes","temp")
end = time.time()   
print(f"解壓了 {success} 個文件 於 {end - start} 秒,真的太星爆了")
#print("解壓失敗數量："+ str(fail))

   

   