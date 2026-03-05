import os
import json
import time
import requests
import datetime
import feedparser
import pandas as pd
import xlwings as xw
from bs4 import BeautifulSoup
from urllib.parse import urljoin

excel_path = r"D:\News_Output.xlsx"

sent_news_file = r"D:\sent_news.json"

news_dict = {
    'Real_Estates': {
        'Keywords': ["Bất động sản", "BĐS", "Nhà ở xã hội", "NOXH", "Khu công nghiệp", "KCN", "FDI",
                    "Dự án", "Đô thị", "KĐT", "Nhà đất", "Đất nền", "Đấu giá", "Sử dụng đất", "Chuyển nhượng dự án", "Quy hoạch", "Mở bán",
                    "Nhà phố", "Chung cư", "Căn hộ", "Địa ốc", "Hạ tầng", "Vành đai", "Cao tốc", "Khởi công", "phép xây dựng", "cao su"
                    "VHM", "NVL", "KDH", "NLG", "DXG", "PDR", "HDG", "AGG", "HDC", "DIG", "NTC", "DPR", "PHR",
                    "Vinhomes", "Novaland", "Khang Điền", "Nam Long", "Đất Xanh", "Phát Đạt", "Hà Đô", "An Gia", "Nam Tân Uyên", "Đồng Phú", "Phước Hòa"],                    
        'RSS_FEEDS': {
            "VnExpress": ["https://vnexpress.net/rss/bat-dong-san.rss"],
            "Vietstock": ["https://vietstock.vn/4220//bat-dong-san/thi-truong-nha-dat.rss",
                            "https://vietstock.vn/42221/bat-dong-san/quy-hoach-ha-tang.rss",
                            "https://vietstock.vn/4222/bat-dong-san/du-an.rss"]
        },
        'WEB_SOURCES': {
            "CafeF_BDS": {"url": "https://cafef.vn/bat-dong-san.chn", "css_selector": "h3 > a"},
            "Batdongsan": {"url": "https://batdongsan.com.vn/tin-tuc", "css_selector": "h3 > a"},
            "Vietnambiz": {"url": "https://vietnambiz.vn/nha-dat.htm", "css_selector": "h3 > a"}
        }
    },
                        
    'Basic_Materials': {
        'Keywords': ["Vật liệu xây dựng", "Đá xây dựng", "Thép", "Quặng sắt", "Than cốc", "HRC", "Tôn mạ", "Tôn kẽm", "Hạt nhựa", "Nhựa xây dựng", "Hạt PVC",
                    "Đường sắt", "Worldsteel", "Khoáng sản và xây dựng Bình Dương", "Vật Liệu Xây Dựng Biên Hòa"
                    "Hòa Phát", "Tập đoàn Hoa Sen", "Nam Kim", "Tôn Đông Á", "Thép Tiến Lên", "Nhựa Bình Mình","Nhựa Thiếu niên Tiền Phong",
                    "HPG", "HSG", "NKG", "GDA", "TLH", "BMP", "NTP", "KSB", "VLB"],
        'RSS_FEEDS': {
            "VnExpress": ["https://vnexpress.net/rss/kinh-doanh.rss"],
            "Vietstock": ["https://vietstock.vn/742/hang-hoa/kim-loai.rss"]

        },
        'WEB_SOURCES': {
            "Vietnambiz": {"url": "https://vietnambiz.vn/hang-hoa/nguyen-lieu.htm", "css_selector": "h3 > a"},
            "CafeF_DoanhNghiep": {"url": "https://cafef.vn/doanh-nghiep.chn", "css_selector": "h3 > a"},
            "CafeF_ThiTruong": {"url": "https://cafef.vn/thi-truong.chn", "css_selector": "h3 > a"},
        }
    }
}

