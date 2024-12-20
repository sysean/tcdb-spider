from loguru import logger

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "*/*",
}

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

headers_v2 = {
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": (
        "CFID=1966457988; "
        "CFTOKEN=d6598bbd9e7c4a88-38F13C1F-D879-CC43-9DFF65669374BF2E; "
        "JSESSIONID=A5351CC068D5D0244C1C0F31F05C0403.cfusion; "
        "__cf_bm=1h0QpEpuzcwjiWaQUJ73oxkbfD.oMaqofllzJML6Lh0-1732255847-1.0.1.1-sw5xUHpAlZgAGUX4zWyNEdX51SnT7HXE2HVGU5Rdl0byqaw7Sszw8MKJZmK8Gut8RbB_3KH0vp6O4WCuqVMOCA; "
        "_ga=GA1.1.1089424365.1732255848; "
        "cf_clearance=9v4FqZV55ABN5BJQO4wJ0UzJj_Kh.XPQC03EYTHjRKA-1732255848-1.2.1.1-0orh3MnPtqboMNnHLdfGlmXLRS58v6jYMG6eFYSNNuwm47VRS4aRPc7gE4SV9Ut_NyFL0_CP4eqhmLbnfhm7mezA2vf5Iqaa9rV_J2XkB.yuaKqpWGBuTpZjwtDQe4Ftqaeb3MClwpwz61XO0UMH9pL4riihAeRewCnNGdCX3iYgTssO1SIj9xOt0eJ.jAigyH8X73Jm9Cam4Nl1vksMm0nLML3JI_ZyybQc7bx_r73mPTOC6RWXlNgLQGGjUcfhs.zDO3Qbx.tYtB0YwFOpkZ.R3erm2qdgqOqIT5vv.5ecV0N7lPnDX49Svcmlozc3SdH_gQsEBDWExoEZrxJIX.Z.oUrDG0Cwrmlem6b5InwsGfIk6eJFTPEiYyMQCAX5Xvv4.zioMm9VQHMGdNPTnw; "
        "usprivacy=1N--; "
        "__gads=ID=a6e6f28b64f27521:T=1732255853:RT=1732255853:S=ALNI_MaPtk14bCgI-ULt_YJC2D3XExaurg; "
        "__gpi=UID=00000f724894e59e:T=1732255853:RT=1732255853:S=ALNI_MYlwiCzStxL8i2KdHEqfi71-PNDOw; "
        "__eoi=ID=b7db7668f9870c1e:T=1732255853:RT=1732255853:S=AA-AfjZX5VcHgA6WAuVui6ALdscX; "
        "_cc_id=e71f2d72ad275d2c7f37159c2d436b71; "
        "panoramaId_expiry=1732860654451; "
        "panoramaId=53c95dad8714de138a38251c6da216d53938feb769c5ddf586828cea03838c84; "
        "panoramaIdType=panoIndiv; "
        "_sharedID=092224c6-6761-43c6-8341-486b9780a131; "
        "_sharedID_cst=kSylLAssaw%3D%3D; "
        "cto_bidid=kvTlDl84V251ajBybW95cWtjTmFUZ1VuUXB0cURZbiUyQldHWUklMkZLRDBzMklrJTJCeWFVc0hGdTFNQkRBa1ZmU2pxOTZ4WlFHUkRGc2twMmVDOEV5SW5oVkp0Z1VnZyUzRCUzRA; "
        "_ga_VGXS6LWKSL=GS1.1.1732255847.1.1.1732255871.0.0.0; "
        "cto_bundle=FEGvz19DS2NpeXhSWG96eWl0VyUyRm1oYkhjWU1UQkNhTW5YWVZyeklNSyUyRmtmN2FOOWxjcWtqOEp4YklwNEhoUW94QlF4SGRsbUQlMkJYS1glMkZHWFJOY3QxNzlidUZtY2wwVElERkY0b1cwM0VhbFllTzRvVmpsQjlnSU1wdEdwRUFoVHdxViUyRlVNUDlrMUNlUmt0bVlWZG9CMTJLS0hzc05KSm1Tc3ZKWmliTlVMNk00aGdTZDIlMkJiUjBJJTJGM3BUaG1yRXRvaDRPZQ"
    ),
    "Accept": "*/*",
}

headers_v3 = {
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Priority": "u=0, i",
    "Cookie": "__cf_bm=FDCGWm8TYVwKIgEHMle2Sc6MFTMlLCcaupsCEzQYvGM-1733735764-1.0.1.1-hgxcSyw_UA.wunt7iZF9dc2l5yMLX.iT2.b2O0X1vwCxr7H4UA6KrK2rT.Lp79pmX0pH8nSNS7HiE04hrSA6Qw; CFID=1999324526; CFTOKEN=e3a148977df305ae-AB0C443D-92C0-1FD0-B1103C3AB772C9FC; JSESSIONID=9A18B8B7F61011160849E523B038B529.cfusion; _ga=GA1.1.1754710102.1733735795; cf_clearance=pNgqV2MPf.NzPwvZBWagixGfqqq.hOwYsllnkFNQVTQ-1733735775-1.2.1.1-dhKAD.OqoENSPQs_Hr32DYrsYc8Ap68Gg02HyRHtVeAXH.DBk2l0aUXHX7QPNfSaThDxeCO3BPKV_D8C6fHPtmWn01Cbk_gmIS3Yb8tmLAytVqONiq.M_faPl9Pkj0HN320.R0UD.B6ZMkf5tJds1qRnHEGtFvjeJj6GlB_CNbWAsioLk0CgkeTWHD5a6roD55guCwjVh2w3KjlISIzqcVzN0Qs.LeKkdjSEZ.0iE13mqUlaVEkv0jCzfuGvgbothWYZy7GJ6y.G4Q5i1Dh4kwdWv1enzDO07NQMCrR9sHT5GRaTgggRUdpSydqguDnpGF.kp7EyPNTKtzkD3Fc.bJl1zv71cLVeJMp9PB3evRmNm1SpkLaHDnYZJ.fBSrf.qbS4kuorGHrE0RGZIh_h8NQ1LXtLap0cXQLaozxf1k8MAdgw1mHeasRr0hxeO8ZD; _sharedID=34bb057f-111a-4732-8822-b8135cf1c773; usprivacy=1N--; _cc_id=51832671c43e231825e574d58ec81ca0; panoramaId_expiry=1734340577984; panoramaId=f756d27b5ce7907e4ee3f3527558185ca02c67b03fb49db284776fd7dfb365a4; panoramaIdType=panoDevice; __gads=ID=32f4d46688e37275:T=1733735779:RT=1733735779:S=ALNI_MaYLLPFLwFTrR5T-vlp_vi3mkg6jw; __gpi=UID=00000f88179280ec:T=1733735779:RT=1733735779:S=ALNI_Mb4xxPtvuSg0xQne4WBR5r-957dpw; __eoi=ID=7654b60e7592477e:T=1733735779:RT=1733735779:S=AA-AfjZLg8jlZUmMVnczoISVCXvK; _sharedID_cst=kSylLAssaw%3D%3D; _ga_VGXS6LWKSL=GS1.1.1733735795.1.0.1733735803.0.0.0; cto_bundle=GmEATV8xQVglMkIlMkZHN0pVWSUyQk9MYmY2cVpPUGE2cXpKdlpTRU5jZ2xqV0daRmtIbTclMkJGYjBjTFhuMVVjbXJabmtSVHV2dFY4R2JWZThrYXNSMzRIcmx6SCUyRnNUc0NWQVlwUGJYemtmM3Z4cVJqbG42czUlMkY5S2U5cFFCbGFQUkxwJTJGVU5ObG5QeTBiZlFGVlpMQ2pDbnZhNEhLcXVOZyUzRCUz",
    "Accept": "*/*",
}

header_list = [headers, headers_v2, headers_v3]
current_header_index = 0


def get_header(call_time):
    global current_header_index
    if call_time > 50:
        if current_header_index == 0:
            current_header_index = 1
        else:
            current_header_index = 0
        return header_list[current_header_index]
    return header_list[current_header_index]
