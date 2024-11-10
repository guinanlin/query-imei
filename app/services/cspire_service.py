from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
import logging
import httpx
from typing import Tuple, Dict
from app.core.config import settings
import asyncio

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确保在当前目录加载.env文件
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class CSpireService:
    BASE_URL = "https://www.cspire.com"
    PROXY_URL = "socks5://192.168.8.19:9054"
    
    # 类属性，用于存储 token
    _token = None
    
    @staticmethod
    async def get_token(isProxy: str = "Y") -> Dict:
        logger.info(f"isProxy设置为: {isProxy}")
        
        proxies = {
            "all://": CSpireService.PROXY_URL
        } if isProxy.upper() == "Y" else None
        
        logger.info(f"使用代理: {proxies if proxies else '不使用代理'}")
        logger.info(f"请求 URL: {CSpireService.BASE_URL}/rest-api/token/v1/login-status")
        
        async with httpx.AsyncClient(proxies=proxies) as client:
            headers = {
                "Content-Type": "application/json",
                "Client": "web",
                "Referer": f"{CSpireService.BASE_URL}/rest-api/token/v1/login-status",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            try:
                response = await client.get(
                    f"{CSpireService.BASE_URL}/rest-api/token/v1/login-status",
                    headers=headers
                )
                response.raise_for_status()  # 检查响应是否正常
                
                logger.info(f"成功获取响应: {response.status_code}")
                logger.debug(f"响应内容: {response.text}")  # 输出响应内容
                
                # 存储获取到的 token
                CSpireService._token = response.json().get("token")
                return {"token": CSpireService._token}
            except httpx.RequestError as e:
                logger.error(f"代理请求失败: {e}")
                return {"error": str(e)}
            except httpx.HTTPStatusError as e:
                logger.error(f"请求失败，状态码: {e.response.status_code}, 内容: {e.response.text}")
                return {"error": f"请求失败，状态码: {e.response.status_code}"}

    @staticmethod
    async def get_device_unlock_status(imei: str, token: str, isProxy: str = "Y") -> Dict:
        logger.info(f"使用Token: {token}")
        transport = httpx.AsyncHTTPTransport(proxy=CSpireService.PROXY_URL) if isProxy.upper() == "Y" else None
        cookies = "VOTER_REG=rvt1370f39331; FB_LIKE=fblt1370f1fd13; _cls_v=82933bb6-d3b8-4807-b8bd-cff01eb47b92; _fbp=fb.1.1731054680762.533804366621084912; _gcl_au=1.1.1752720171.1731054682; _tt_enable_cookie=1; _ttp=YmOytaH-MJXaRTx6XrCQvdJd2pt; _cfuvid=uCQS9XA12AvBe8NdHr3.zhJT4UmkZ8rdrwww51BSFso-1731215709008-0.0.1.1-604800000; at_check=true; AMCVS_85279F01585CF4FA0A495CC3%40AdobeOrg=1; _cls_s=d78faffd-7b88-4e6f-a1ab-af942c0b3e71:1; s_cc=true; _ga=GA1.1.539719668.1731215714; rto=c0; ApplicationGatewayAffinityCORS=3e53813bfb724589ce09f21334caabe1; ApplicationGatewayAffinity=3e53813bfb724589ce09f21334caabe1; AMCV_85279F01585CF4FA0A495CC3%40AdobeOrg=179643557%7CMCIDTS%7C20038%7CMCMID%7C04273013018952943824581981715608919266%7CMCAAMLH-1731831991%7C11%7CMCAAMB-1731831991%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1731234391s%7CNONE%7CvVersion%7C5.5.0; s_sq=%5B%5BB%5D%5D; BIGipServer~Web~prod_web_http_17700_pool=578621450.9285.0000; JSESSIONID=O9IVg4nmlLN_gVY80ZNBSbVSKo-9_oOGTh_Cc06jkPEnbLGSJUNW!1475395455; adcloud={%22_les_v%22:%22c%2Cy%2Ccspire.com%2C1731234773%22}; QSI_HistorySession=https%3A%2F%2Fwww.cspire.com%2Fwireless%2Fapps%2Fdevice-unlock~1731215715973%7Chttps%3A%2F%2Fwww.cspire.com%2F~1731217884538%7Chttps%3A%2F%2Fwww.cspire.com%2Fwireless%2Fapps%2Fdevice-unlock~1731220667018%7Chttps%3A%2F%2Fwww.cspire.com%2F~1731227206185%7Chttps%3A%2F%2Fwww.cspire.com%2Fwireless%2Fapps%2Fdevice-unlock~1731229054743%7Chttps%3A%2F%2Fwww.cspire.com%2F~1731231362759%7Chttps%3A%2F%2Fwww.cspire.com%2Fwireless%2Fapps%2Fdevice-unlock~1731232973376; __cf_bm=oc5aQCM7hwuL2Xy7n_sAyd7FEtdwgxdFfpfKCg_Ldlw-1731233989-1.0.1.1-ihEvGlSKm8aWzNOWkW4K2H3Pdqb3JrO0Zgxt1Nwud1FEPuVkmlCdgGtxB192rJXTR3o_Owe82vpWRWjZomIlmA; mbox=PC#b7e220afc4964ed8bcaf68c94ef1c189.32_0#1794478792|session#fffe8d22792f4b639c5261485e3bc095#1731235852; cf_clearance=rcSoX.MEfdIo1..P4Q0Ev74JWVCEWK5_zmQdavPL1lE-1731233992-1.2.1.1-CzwqdkA9aMIoss2ZIuJmN1NQJOcyIeNCK2VwLjSqugxvYII1sF_8FbYBJhVlCOv09vVRVOeVbAbE4MaLiOvUYPPv5W4gNo8JGsYwkjyyT_B6ZXajoMEvGtYlbc_briXQuXnlecMR1HzzxIoOrD4nhC4_rCegGRwKk9jVCtEXD2NA0fVuR8pwbbE31xkq.kVscpEcBGj8oVx3HKIOFzhCfnQbLjjB1WGTBLqJc9htCc9_Dlyff.v1aod5bo5oKPCd1CiaCv9_iLGzeRJ7tnddOMxRS1naBmgO9D51QwnM1bHSKz4Ulk0B3Yy134ChhOmIqOzgvas_qPeeJ01oPsUfOSamkUPVziG1a92IvDFmQ2_ud730UIJrBrpu1bRa.7Ax4XbgSH8fUQd_0g5.ckjkcg; _ga_GQ7XNYBB62=GS1.1.1731232923.6.0.1731234000.49.0.0; serverTime=1731234188240; expiryTime=1731235988240; warningTime=1731235388240; TS018d3304=0135c98afc5dae0f77ee8b418b8c8d769be8dd857f9a15bbd9c2a0f338d5b63b844b3464039e1814f16df49916041808a81b7ead833c967e5ea7893a226f6b874a7c945dc69378580a9f7fa9447400b23211743bdf9d4465af9cc3cb4a1033992144e53d4ef01173de2524fce9331c1fb3f1f39c69b971e6cfffb1c927651144cb003b2426028ec48286a1724291af7007e264142c5f0e0a246acd1ffd0411577c3f84b4f7beebbe8a57f820a0b66796751a251e028e275a2306136681ba46bc808b2f2ea5"
        
        client_params = {"transport": transport} if transport else {}
        async with httpx.AsyncClient(**client_params) as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Client":"web",
                "Referer": f"{CSpireService.BASE_URL}/rest-services/web-wirelessaccount-services/v1/device-unlock",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Cookie": cookies
            }
            response = await client.get(
                f"{CSpireService.BASE_URL}/rest-services/web-wirelessaccount-services/v1/device-unlock",
                params={"imei": imei},
                headers=headers
            )
            return response.json()

    @staticmethod
    async def get_imei_lockstatus(imei: str, isProxy: str = "Y") -> Tuple[int, Dict]:
        try:
            # 步骤1：获取token
            token_response = await CSpireService.get_token(isProxy)
            token = token_response["token"]
            
            # 打印获取到的 token
            logger.info(f"获取到的 token: {token}")
            
            # 等待2秒钟
            await asyncio.sleep(2)
            
            # 步骤2：获取设备解锁状态
            unlock_status = await CSpireService.get_device_unlock_status(imei, token, isProxy)
            return 0, unlock_status
        except Exception as e:
            logging.error(f"获取IMEI锁定状态失败: {str(e)}")
            return 1, {"error": str(e)}

    @staticmethod
    def check_imei(imei: str) -> tuple[int, str]:
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--enable-unsafe-swiftshader')
        
        # 添加SOCKS5代理配置
        proxy_host = os.getenv("PROXY_HOST", "127.0.0.1")
        proxy_port = os.getenv("PROXY_PORT", "1080")
        
        # 配置SOCKS5代理
        chrome_options.add_argument(f'--proxy-server=socks5://{proxy_host}:{proxy_port}')
        logger.info(f"使用SOCKS5代理: socks5://{proxy_host}:{proxy_port}")
        
        # 启用无图模式
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        # 设置页面加载策略为 'eager'
        chrome_options.page_load_strategy = 'eager'
        
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        try:
            target_url = os.getenv("TARGET_URL")
            if not target_url:
                raise ValueError("TARGET_URL 环境变量未设置")
            
            logger.info(f"开始检查IMEI: {imei}")
            logger.info(f"访问网址: {target_url}")
            
            # 访问初始页面
            driver.get(target_url)
            logger.info("页面加载完成")
            
            # 保存页面内容到 HTML 文件
            page_source = driver.page_source  # 获取页面源代码
            html_file_path = os.path.join(os.path.dirname(__file__), f"initial_page_{imei}.html")  # 定义文件路径
            with open(html_file_path, "w", encoding="utf-8") as f:
                f.write(page_source)  # 写入文件
            logger.info(f"初始页面已保存到: {html_file_path}")
            
            # 尝试查找并点击 "Check Status" 按钮
            logger.info("尝试查找 Check Status 按钮")
            check_status_button = None
            while check_status_button is None:
                try:
                    check_status_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'status-btn') and contains(text(), 'Check The Status')]"))
                    )
                    check_status_button.click()
                    logger.info("Check Status 按钮点击成功")
                except Exception as e:
                    logger.warning(f"未找到 Check Status 按钮: {str(e)}，继续等待...")
                    # 继续等待，直到找到按钮
            
            # 等待输入框出现并输入IMEI
            logger.info("等待输入框出现")
            input_field = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )
            
            # 输入框出现时的调试信息
            logger.info("输入框已出现，准备输入IMEI")
            input_field.clear()
            input_field.send_keys(imei)
            logger.info("IMEI输入完成")
            
            # 保存当前页面的 HTML 容
            page_source = driver.page_source
            html_file_path = os.path.join(os.path.dirname(__file__), f"imei_input_page_{imei}.html")
            with open(html_file_path, "w", encoding="utf-8") as f:
                f.write(page_source)
            logger.info(f"IMEI输入完成时的页面已保存到: {html_file_path}")
            
            # 等待提交按钮变为可点击
            logger.info("等待提交按钮为可点击")
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Continue')]"))
            )
            
            # 点击提交按钮
            submit_button.click()
            logger.info("提交按钮点击成功")
            
            # 等待结果出现 - 用多个可能的选择器
            logger.info("等待结果出现")
            result_selectors = [
                "#result",
                ".result",
                "//*[contains(@class, 'result')]",
                "//*[contains(@id, 'result')]"
            ]
            
            result_text = None
            for selector in result_selectors:
                try:
                    if selector.startswith("/"):
                        result_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        result_element = wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    result_text = result_element.text
                    logger.debug(f"找到结果元素: {selector}, 内容: {result_text}")
                    break
                except Exception as e:
                    logger.warning(f"未能找到结果元素: {selector}, 错误: {str(e)}")
                    continue
                    
            if result_text:
                logger.info(f"获取到结果: {result_text}")
                return 0, result_text.strip()
            else:
                raise Exception("未能获取结果")
            
        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
            return 1, f"检查失败: {str(e)}"
        
        finally:
            driver.quit()
            logger.info("浏览器已关闭")

    @staticmethod
    async def test_proxy():
        logger.info(f"使用代理: {CSpireService.PROXY_URL}")
        async with httpx.AsyncClient(proxies={"all://": CSpireService.PROXY_URL}) as client:
            try:
                response = await client.get("http://httpbin.org/ip")
                logger.info(f"响应内容: {response.json()}")
                return response.json()
            except Exception as e:
                logger.error(f"请求失败: {str(e)}")