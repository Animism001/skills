import requests
from bs4 import BeautifulSoup
import time

# 搜索兰迪·英格曼森的信息
def search_randy_ingermanson():
    print("🔍 正在搜索兰迪·英格曼森 (Randy Ingermanson) 的信息...")
    print("=" * 80)
    
    # 使用Bing搜索
    search_urls = [
        "https://cn.bing.com/search?q=Randy+Ingermanson+author+biography",
        "https://cn.bing.com/search?q=Randy+Ingermanson+Christian+fiction+books",
        "https://cn.bing.com/search?q=Randy+Ingermanson+Snowflake+Method+writing"
    ]
    
    results = []
    
    for url in search_urls:
        try:
            print(f"\n🌐 搜索: {url}")
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 提取搜索结果
                search_results = soup.find_all('li', class_='b_algo')
                
                for i, result in enumerate(search_results[:3]):  # 每个搜索取前3个结果
                    title = result.find('h2')
                    link = result.find('a')
                    snippet = result.find('p')
                    
                    if title and link and snippet:
                        results.append({
                            'title': title.text.strip(),
                            'url': link.get('href'),
                            'snippet': snippet.text.strip()
                        })
                        print(f"  {i+1}. {title.text.strip()}")
                        print(f"     {snippet.text.strip()[:100]}...")
                        print(f"     {link.get('href')}")
            else:
                print(f"❌ 搜索失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 搜索错误: {e}")
        
        time.sleep(2)  # 避免速率限制
    
    print("\n" + "=" * 80)
    return results

# 主函数
if __name__ == "__main__":
    search_results = search_randy_ingermanson()
    
    if search_results:
        print("\n📊 搜索完成，共找到 {} 条相关结果".format(len(search_results)))
    else:
        print("\n❌ 未找到相关信息")
