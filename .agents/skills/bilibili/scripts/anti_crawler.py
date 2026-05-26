#!/usr/bin/env python3
"""
B站反爬机制模块
提供多种反爬措施：随机User-Agent、完整请求头、会话保持、重试机制等
"""
import random
import time
import urllib.request
import urllib.error
import http.cookiejar


class AntiCrawler:
    """
    反爬管理器类
    提供多种反爬措施
    """
    
    def __init__(self):
        # 初始化CookieJar
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        
        # 扩展的User-Agent列表
        self.user_agents = [
            # Chrome Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            
            # Chrome Mac
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            
            # Firefox
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
            
            # Safari
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
            
            # Edge
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            
            # Mobile - iPhone
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1",
            
            # Mobile - Android
            "Mozilla/5.0 (Linux; Android 14; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
            
            # iPad
            "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1"
        ]
    
    def get_random_user_agent(self):
        """获取随机的User-Agent"""
        return random.choice(self.user_agents)
    
    def get_complete_headers(self, referer="https://www.bilibili.com", is_json=False, is_video=False):
        """
        获取完整的请求头
        
        Args:
            referer: Referer URL
            is_json: 是否请求JSON数据
            is_video: 是否请求视频页面
            
        Returns:
            headers字典
        """
        user_agent = self.get_random_user_agent()
        
        if is_json:
            headers = {
                "User-Agent": user_agent,
                "Referer": referer,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "X-Requested-With": "XMLHttpRequest"
            }
        elif is_video:
            headers = {
                "User-Agent": user_agent,
                "Referer": referer,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
            }
        else:
            headers = {
                "User-Agent": user_agent,
                "Referer": referer,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1"
            }
        
        return headers
    
    def random_delay(self, min_sec=2, max_sec=5):
        """随机延迟"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        return delay
    
    def long_delay(self, min_sec=10, max_sec=20):
        """较长的随机延迟，用于每处理几个请求后"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        return delay
    
    def make_request(self, url, headers=None, max_retries=3, timeout=30):
        """
        发送请求，带重试机制
        
        Args:
            url: 请求的URL
            headers: 请求头，如果为空则使用默认的
            max_retries: 最大重试次数
            timeout: 超时时间（秒）
            
        Returns:
            响应对象
        """
        if headers is None:
            headers = self.get_complete_headers()
        
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with self.opener.open(req, timeout=timeout) as resp:
                    return resp
            except urllib.error.HTTPError as e:
                last_exception = e
                print(f"HTTP错误 {e.code}: {e.reason} (尝试 {attempt + 1}/{max_retries})")
                if e.code == 412:
                    # Precondition Failed，需要更长的延迟
                    print("遇到412错误，延长延迟时间...")
                    self.long_delay(15, 30)
                elif e.code == 429:
                    # Too Many Requests
                    print("遇到429错误，长时间延迟...")
                    self.long_delay(30, 60)
                else:
                    self.random_delay(5, 10)
            except urllib.error.URLError as e:
                last_exception = e
                print(f"URL错误: {e.reason} (尝试 {attempt + 1}/{max_retries})")
                self.random_delay(5, 10)
            except Exception as e:
                last_exception = e
                print(f"请求错误: {str(e)} (尝试 {attempt + 1}/{max_retries})")
                self.random_delay(5, 10)
        
        # 所有重试都失败了
        raise last_exception if last_exception else Exception("请求失败，所有重试都已耗尽")


# 全局实例
_anti_crawler_instance = None


def get_anti_crawler():
    """获取反爬管理器单例"""
    global _anti_crawler_instance
    if _anti_crawler_instance is None:
        _anti_crawler_instance = AntiCrawler()
    return _anti_crawler_instance
