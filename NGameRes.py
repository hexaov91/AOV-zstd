import os
import zstandard as zstd


class NGameResRW:

    def __init__(self):
        with open(r'DS', 'rb') as f:
            dict_data = f.read()
        dict_data = zstd.ZstdCompressionDict(dict_data)

        self.ZstdAlgorithms = {
            "zstd": (zstd.ZstdCompressor(level=10,dict_data=dict_data), zstd.ZstdDecompressor(dict_data=dict_data)),
        }
        

    def DecodeFile(self,path=""):
        with open(path, 'rb') as f:
            fmode=f.read(4)
            fsize=f.read(4)
            data=f.read()
        if fmode == b'\x22\x4a\x00\xef':
            dedata=self.ZstdAlgorithms['zstd'][1].decompress(data)
        #elif fmode == b'\x22\x4a\x67\x00':
        #    return(decode_AES(fpath,f))
        else:
            print("未知格式，返回原始數據")
            return(fmode+fsize+data)
        return dedata

    def EncodeFile(self,path=""):
        with open(path, 'rb') as f:
            data=f.read()

        data=self.ZstdAlgorithms['zstd'][0].compress(data)

        return data
