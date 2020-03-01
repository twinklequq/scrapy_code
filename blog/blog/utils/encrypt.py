# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-

import base64
import random
import string
import binascii
import math
import requests
import time
from Crypto.Cipher import AES


def random_16():
    sep = string.digits + string.ascii_letters
    key = bytes("".join(random.sample(sep, 16)), 'utf-8')
    return key


def rsa_encrypt(ran_16, pub_key, mod):
    text = ran_16[::-1]#明文处理，反序并hex编码
    rsa = int(binascii.hexlify(text), 16) ** int(pub_key, 16) % int(mod, 16)
    return format(rsa, 'x').zfill(256)


def aes_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    try:
        text = text.decode()
    except:
        pass
    text = text + pad * chr(pad)
    try:
        text = text.encode()
    except:
        pass
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypted_text = encryptor.encrypt(text)
    encrypted_text = base64.b64encode(encrypted_text)
    return encrypted_text


def get_params(id):
    pub_key = "010001"
    mod = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    iv = '0102030405060708'
    first_key = "0CoJUm6Qyw8W8jud"
    text = '{csrf_token: "", id: %s, lv: -1, tv: -1}' % (id)
    i = random_16()
    encText = aes_encrypt(text, first_key, iv)
    encText = aes_encrypt(encText, i, iv)
    encSecKey = rsa_encrypt(i, pub_key, mod)
    return encText, encSecKey


def get_lyric(id):
    url = "https://music.163.com/weapi/song/lyric?csrf_token="
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "origin": "https://music.163.com",
    }
    params, encSecKey = get_params(id)
    payload = {
        'params': params,
        'encSecKey': encSecKey
    }
    response = requests.post(url=url, headers=headers, data=payload)
    return response.json()['tlyric']['lyric']


if __name__ == '__main__':
    start_time = time.time()
    # get_comments()
    a, b = get_params(1)
    re_a = a.decode()
    print("a type is {}， b type is {}".format(type(re_a), type(b)))
    print("耗时:", time.time()-start_time)