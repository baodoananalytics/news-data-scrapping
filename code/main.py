from hardcode import *

class industry():
    def __init__(self, industry_name=None):
        self.industry_name = industry_name
        self.keywords = news_dict[self.industry_name]['Keywords']
        self.RSS_FEEDS = news_dict[self.industry_name]['RSS_FEEDS']
        self.WEB_SOURCES = news_dict[self.industry_name]['WEB_SOURCES']
    def news(self):

        def read_sent_news(filepath):
            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                return {}
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    return json.load(file) 
            except json.JSONDecodeError:
                return {}

        sent_news = read_sent_news(sent_news_file)
        titles = [sent_news[link]['title'] for link,_ in sent_news.items()]

        def save_sent_news():
            with open(sent_news_file, "w", encoding="utf-8") as f:
                json.dump(sent_news, f, ensure_ascii=False, indent=4) 
        
        def rss_feed_news():
            news_list = []
            for source, urls in self.RSS_FEEDS.items():
                for url in urls:
                    feed = feedparser.parse(url)
                    for entry in feed.entries:
                        title = entry.title
                        link = entry.link
                        summary = BeautifulSoup(entry.summary, "html.parser").get_text() if 'summary' in entry else None
                        if 'published_parsed' in entry:
                            p = entry['published_parsed']
                            published_time = datetime.datetime(p.tm_year, p.tm_mon, p.tm_mday, 
                                                               p.tm_hour, p.tm_min, p.tm_sec)
                        if title not in titles and any(keyword.lower() in title.lower() for keyword in self.keywords):
                            news = {"source": source, 
                                    "title": title,
                                    "summary": summary, 
                                    "link": link, 
                                    "published_time": published_time.isoformat() if published_time else None}

                            sent_news[link] = news 
                            news_list.append(news)
                            save_sent_news()
            return news_list
        
        def web_sources_news():
            news_list = []
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                for source, info in self.WEB_SOURCES.items():
                    response = requests.get(info["url"], headers=headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        articles = soup.select(info["css_selector"])

                        for article in articles:
                            title = article.get_text().strip()
                            link = urljoin(info["url"], article.get('href'))

                            if title not in titles and any(keyword.lower() in title.lower() for keyword in self.keywords):
                                news = {"source": source,
                                        "title": title,
                                        "summary": None,
                                        "link": link,
                                        "published_time": None}
                                
                                sent_news[link] = news
                                news_list.append(news)
                                save_sent_news()
                return news_list
                
            except Exception as e:
                print(f"Error")
            return []

        rss_news = rss_feed_news()
        web_news = web_sources_news()

        all_news_list = rss_news + web_news
        return all_news_list
    def news_storage(self):
        def append_unique(arr, excel_path, sheet_name='Sheet1',
            table_name='Table1', key_col='id'):
            wb  = xw.Book(excel_path)
            ws  = wb.sheets[sheet_name]
            tbl = ws.tables[table_name]
            
            old_df = tbl.range.options(pd.DataFrame,
                                    header=True, index=False,
                                    expand='table').value
            
            col_names = old_df.columns.tolist()
            new_df = pd.DataFrame(arr, columns=col_names)
            
            mask = ~new_df[key_col].isin(old_df[key_col])
            append_df = new_df[mask]
            if append_df.empty:
                print('No news now!')
                return
            
            first_empty_row = tbl.range.last_cell.row + 1
            first_col       = tbl.range.column
            ws.range((first_empty_row, first_col)).options(
                index=False, header=False).value = append_df.values
            
            n_new = len(append_df)
            n_cols = tbl.range.columns.count
            tbl.resize(tbl.range.resize(old_df.shape[0] + n_new + 1, n_cols))
            
            print(f'Appended {n_new} new rows and eliminate {len(arr)-n_new} duplicates.')
        
        arr = []
        sheet_name = self.industry_name
        table_name = f'tbl_{self.industry_name}_News'
        key_col = 'id'
        
        all_news = industry(industry_name=self.industry_name).news()
        for news in all_news:
            date = datetime.datetime.today()
            source = news['source']
            title = news['title']
            link = news['link']
            _id = f'{source}_{title}'
            arr.append([_id, date, source, title, link, ''])
        
        append_unique(arr, excel_path, sheet_name, table_name, key_col)

if __name__ == "__main__":
    while True:
        industry(industry_name='Real_Estates').news_storage()
        industry(industry_name='Basic_Materials').news_storage()

        time.sleep(600)