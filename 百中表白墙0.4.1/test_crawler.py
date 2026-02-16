import requests
import time
import threading

# 测试目标URL
base_url = 'http://localhost:5000'

# 测试1: 请求频率限制
def test_rate_limit():
    print("=== 测试请求频率限制 ===")
    count = 0
    success_count = 0
    error_count = 0
    
    start_time = time.time()
    for i in range(100):
        try:
            response = requests.get(f"{base_url}/")
            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                error_count += 1
                print(f"请求被限制: {i+1}")
            count += 1
            time.sleep(0.1)  # 稍微延迟，避免太快
        except Exception as e:
            print(f"请求失败: {e}")
            error_count += 1
    
    end_time = time.time()
    print(f"总请求数: {count}")
    print(f"成功请求数: {success_count}")
    print(f"错误请求数: {error_count}")
    print(f"测试耗时: {end_time - start_time:.2f}秒")
    print()

# 测试2: 访问敏感路径
def test_sensitive_paths():
    print("=== 测试访问敏感路径 ===")
    paths = [
        "/admin",
        "/admin/login",
        "/admin/dashboard"
    ]
    
    for path in paths:
        try:
            response = requests.get(f"{base_url}{path}")
            print(f"访问 {path}: 状态码 {response.status_code}")
        except Exception as e:
            print(f"访问 {path} 失败: {e}")
    print()

# 测试3: 并发请求
def concurrent_request():
    try:
        response = requests.get(f"{base_url}/")
        return response.status_code
    except Exception as e:
        return str(e)

def test_concurrent_requests():
    print("=== 测试并发请求 ===")
    threads = []
    results = []
    
    def collect_result(result):
        results.append(result)
    
    for i in range(50):
        thread = threading.Thread(target=lambda: collect_result(concurrent_request()))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    success_count = sum(1 for r in results if r == 200)
    error_count = sum(1 for r in results if r != 200)
    
    print(f"并发请求数: 50")
    print(f"成功请求数: {success_count}")
    print(f"错误请求数: {error_count}")
    print()

# 测试4: 测试robots.txt
def test_robots_txt():
    print("=== 测试robots.txt ===")
    try:
        response = requests.get(f"{base_url}/robots.txt")
        if response.status_code == 200:
            print("robots.txt 可访问")
            print("内容:")
            print(response.text)
        else:
            print(f"robots.txt 访问失败: 状态码 {response.status_code}")
    except Exception as e:
        print(f"robots.txt 访问失败: {e}")
    print()

if __name__ == "__main__":
    print("开始测试防护措施...")
    print()
    
    # 先启动服务器，再运行测试
    print("请确保服务器已启动在 http://localhost:5000")
    input("按回车键开始测试...")
    
    test_rate_limit()
    test_sensitive_paths()
    test_concurrent_requests()
    test_robots_txt()
    
    print("测试完成！")
