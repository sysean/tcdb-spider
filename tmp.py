import requests

headers = {
    "Cache-Control": "max-age=0",
    "Sec-CH-UA": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Full-Version": "133.0.6847.2",
    "Sec-CH-UA-Arch": "arm",
    "Sec-CH-UA-Platform": "macOS",
    "Sec-CH-UA-Platform-Version": "14.1.1",
    "Sec-CH-UA-Model": "",
    "Sec-CH-UA-Bitness": "64",
    "Sec-CH-UA-Full-Version-List": '"Chromium";v="130.0.6723.117", "Google Chrome";v="130.0.6723.117", "Not?A_Brand";v="99.0.0.0"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.tcdb.com/ViewSet.cfm/sid/110748/1986-Arizona-Wildcats-Police",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    # "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Cookie": "__qca=I0-807113249-1731549856827; _ga=GA1.1.482979668.1731035921; usprivacy=1N--; _sharedID=eabe51e6-6b8c-4254-abc2-0e6875357040; _cc_id=68f4f779e33d3434cf0c8d459345aec1; _sharedid=706d73c9-1770-4911-a35f-d4aeb60d2c7b; _sharedid_cst=TyylLI8srA%3D%3D; _sharedID_cst=2SzgLJUseQ%3D%3D; panoramaId_expiry=1732297233635; panoramaId=15894eb7979673f9eff0b45d97764945a702d28a549e064b8d0a5b85ffc7e2d5; panoramaIdType=panoIndiv; __gads=ID=9e551d7e6b4c478b:T=1731035925:RT=1732168715:S=ALNI_MbC9obPO1jeazQ_hawbZeeG-XeIUw; __gpi=UID=00000f7d4de3eeda:T=1731035925:RT=1732168715:S=ALNI_MZ9MDhs87mafhYR_-4rHpegXb462Q; __eoi=ID=943cb940abfd2e1b:T=1731035925:RT=1732168715:S=AA-AfjaZeVJWwWyB5d-vYgA9_z9M; CFID=1965167808; CFTOKEN=be0704db5eb9e5cb-05025094-F518-1FEB-EAE52A3CB068B599; JSESSIONID=E9FD6D3367C9015AA6DEC1FB6E4FE3BA.cfusion; __cf_bm=VMwuDVhTUzkLp2.O6zUJdCsEG04I.lE6cemOthxlPUI-1732168717-1.0.1.1-AkOaCmFouXCk7TYmBqiu8qjnhgtRkop4RKTPfqJfOdf3EZwlNNHjPHWxx3yCzlKvelm2PV8bGDWypWtsO1b8uw; cf_clearance=80Xs7a73_LkPM4LLngQPI0MMn2Y9619DGfNKsuSw4W8-1732168719-1.2.1.1-tv88xLBtJ8dw.U66cFZKB32_y6uDVcMYrVnSzg0duBh_QyhLYoil7dtB93GV5bWWt38zs_JrKVUo2Yaq4k_JGGBb2j0qwLAb4ky6tLoJy33pCqFnI7FjjFPmQKNF6PFMXOp4lTYJ74SXqpig6vebAe_I9qZ8.mt5m9F7.d68riaAHE1t7wEMHKLQZDh3s3j64tQe.OFE.mgtQARBBpMEt4HsHoZdh1nQ7NlmBTLdrhGIoVHVw4Et.m1PcExjmAuarH0hl0FTaPUE3JnZa9bzxqw7v4KZzUXSB94X1Xe5JqznNbazj19jbNWyRMLiTjG_6wKu3xIrfafiOGHm.tJkHDREzRacLrFwu06sFL1tHKljYmlpIRDhxCRg_KcueCLSm9J9VUzy24EGRulsqMdDrA; _ga_VGXS6LWKSL=GS1.1.1732168019.38.1.1732168780.0.0.0; cto_bidid=3CBi8l9mVnFnSVNxTlFXSFFTNFgyazVBRGJVNXlnRm53SFBSb3dQY2Z2TkJBU0FjNDVmS29OOFdGRTBVclZvaFVsbzlXamJBUkNaY21vOEdDbjd4VzNKclo2anpPRDQ4ZEs5RXpNR01yZUNLOG9ralM4MHdxRk9scHFPYkZ6ckNiJTJGRUdEMjNhJTJCZjY5bHV1YWNoODRtMDQ2bHN3JTNEJTNE; cto_bundle=1Xp6rV9uV3poMkhTdHlQQUpvTnI2cVZnMlFLNUIlMkI4Y29OaUpqJTJGbE9TMldUMyUyQkxCWURiMEh6VFlIc2F3VHllJTJGR2pQUFN2blolMkIzY2RtZG90Vm54YVBldWhYQjBqJTJGM1M4dUNxSyUyQnpFZnp4Q3RZWHd0MWtrUkpLM01QZ2ZXM21NT0tRT09NUExlRExxU0h2YSUyQnpKT2piMkJRV2p3eWhFdFd6cVFVN1hCSDExSERkRWQlMkYzRHNBRTZNJTJCNXhDTiUyQkFndURPdHRSdHp0VXNDRXBVZDhXNnIxMFdrUmJNZyUzRCUzRA",
    "Priority": "u=0, i",
    "Accept": "*/*",
}

url = 'https://www.tcdb.com/Checklist.cfm/sid/191084'
proxy = 'http://S1zO6DCYBhFoBmAY:WVOEMucxzg54GrI1_country-us@geo.iproyal.com:12321'
proxy_auth = 'S1zO6DCYBhFoBmAY:WVOEMucxzg54GrI1'
proxies = {
    'http': proxy,
    'https': proxy
}

response = requests.get(url, proxies=proxies, headers=headers)
print(response.text)
