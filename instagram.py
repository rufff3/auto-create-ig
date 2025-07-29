import time
import json
import random
import string
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.2592.81",
]

def tampilkan_banner(teks, warna=Fore.CYAN, font="slant"):
    banner_text = pyfiglet.figlet_format(teks, font=font, width=100)
    print(Style.BRIGHT + warna + banner_text)

def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_project_folders():
    if not os.path.exists('cookies'): os.makedirs('cookies')
    if not os.path.exists('data'): os.makedirs('data')

def menu_buat_akun():
    create_project_folders()
    BLACKLISTED_DOMAINS = ["innovasolar.me", "oliq.tech", "gijo.me", "edushort.me"]
    
    try:
        jumlah_akun = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}Berapa banyak akun yang ingin Anda buat? {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}Input tidak valid. Harap masukkan angka.")
        return

    for i in range(jumlah_akun):
        print(f"\n{Style.BRIGHT}{Fore.CYAN}--- MEMBUAT AKUN KE-{i+1} DARI {jumlah_akun} ---{Style.RESET_ALL}")
        driver = None
        try:
            proxy = ""
            
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-notifications")
            options.add_argument("--log-level=3")
            options.add_argument("--headless=new")
        
            user_agent_terpilih = random.choice(USER_AGENTS)
            options.add_argument(f'user-agent={user_agent_terpilih}')
            print(f"{Fore.BLUE}INFO: User-Agent -> {user_agent_terpilih[:50]}...")

            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
            
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(driver, 60)

            print(f"{Fore.BLUE}➡️ Menjalankan pendaftaran & verifikasi...{Style.RESET_ALL}")
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            instagram_tab = driver.current_window_handle
            driver.switch_to.new_window('tab')
            driver.get("https://tempmail.ac.id/")
            tempmail_tab = driver.current_window_handle
            while True:
                email_div_xpath = "//div[contains(text(), '@') and not(contains(text(), 'Copyright')) and string-length(text()) > 5]"
                email_element = wait.until(EC.presence_of_element_located((By.XPATH, email_div_xpath)))
                temp_email = email_element.text.strip()
                email_domain = temp_email.split('@')[1].strip().lower()
                if email_domain in BLACKLISTED_DOMAINS:
                    print(f"{Fore.YELLOW}🚫 Domain terlarang: {email_domain}. Meminta email baru...{Style.RESET_ALL}")
                    delete_button_xpath = "//div[normalize-space()='Delete'] | //button[contains(., 'Delete')]"
                    delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath)))
                    delete_button.click(); time.sleep(5); driver.refresh()
                else:
                    print(f"{Fore.GREEN}✅ Email valid didapatkan: {temp_email}{Style.RESET_ALL}")
                    break
            driver.switch_to.window(instagram_tab)
            full_name = " ".join(generate_random_string(6) for _ in range(2)).title()
            username = generate_random_string(10)
            password = generate_random_string(12) + "A1!"
            wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone"))).send_keys(temp_email)
            driver.find_element(By.NAME, "fullName").send_keys(full_name)
            time.sleep(1)
            driver.find_element(By.NAME, "username").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
            time.sleep(5)
            try:
                limit_error_xpath = "//span[contains(., 'something went wrong creating your account') or contains(., 'has been flagged as an open proxy')]"
                driver.find_element(By.XPATH, limit_error_xpath)
                raise Exception("IP Kena Limit/Proxy!")
            except NoSuchElementException:
                pass
            wait.until(EC.presence_of_element_located((By.XPATH, "//select[@title='Month:']"))).send_keys("August")
            wait.until(EC.presence_of_element_located((By.XPATH, "//select[@title='Day:']"))).send_keys("15")
            wait.until(EC.presence_of_element_located((By.XPATH, "//select[@title='Year:']"))).send_keys("1995")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))).click()
            driver.switch_to.window(tempmail_tab)
            subject_div_xpath = "//div[contains(@class, 'cursor-pointer')]//div[contains(., 'is your Instagram code') or contains(., 'adalah kode Instagram Anda')]"
            subject_element = wait.until(EC.presence_of_element_located((By.XPATH, subject_div_xpath)))
            subject_text = subject_element.text
            otp_match = re.search(r'\b\d{6}\b', subject_text)
            if not otp_match: raise Exception("Gagal mengekstrak OTP.")
            otp_code = otp_match.group(0)
            print(f"{Fore.GREEN}🔑 Kode OTP: {otp_code}{Style.RESET_ALL}")
            driver.switch_to.window(instagram_tab)
            confirmation_input = wait.until(EC.element_to_be_clickable((By.NAME, "email_confirmation_code")))
            confirmation_input.send_keys(otp_code)
            next_button_xpath = "//div[@role='button' and text()='Next']"
            wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath))).click()
            time.sleep(5)
            try:
                proxy_error_xpath = "//span[contains(text(), 'has been flagged as an open proxy')]"
                driver.find_element(By.XPATH, proxy_error_xpath)
                raise Exception("Gagal (Proxy terdeteksi setelah OTP).")
            except NoSuchElementException:
                pass
            beranda_termuat_xpath = "//*[local-name()='svg' and @aria-label='Home']"
            wait.until(EC.presence_of_element_located((By.XPATH, beranda_termuat_xpath)))
            print(f"{Style.BRIGHT}{Fore.GREEN}✅ Pendaftaran Instagram Berhasil!{Style.RESET_ALL}")

            print(f"{Fore.BLUE}📝 Menyimpan detail akun...{Style.RESET_ALL}")
            try:
                with open("akun.txt", "a", encoding="utf-8") as f:
                    f.write(f"email: {temp_email}\n"); f.write(f"username: {username}\n"); f.write(f"sandi: {password}\n"); f.write("="*25 + "\n")
                print(f"{Fore.GREEN}✅ Akun disimpan di akun.txt{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}⚠️ Gagal menyimpan akun: {e}{Style.RESET_ALL}")

            print(f"{Fore.BLUE}🍪 Menyimpan cookies Instagram...{Style.RESET_ALL}")
            instagram_cookies = driver.get_cookies()
            cookie_file_path = os.path.join('cookies', f'{username}_instagram.json')
            with open(cookie_file_path, 'w') as f: json.dump(instagram_cookies, f)
            print(f"{Fore.GREEN}✅ Cookies untuk '{username}' berhasil disimpan.{Style.RESET_ALL}")

        except Exception as e:
            print(f"\n{Style.BRIGHT}{Fore.RED}❌ Gagal membuat akun ke-{i+1}: {e}{Style.RESET_ALL}")
        
        finally:
            if driver:
                print(f"{Fore.YELLOW}🎉 Proses untuk akun ini selesai. Menutup browser...{Style.RESET_ALL}")
                driver.quit()

if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        tampilkan_banner("Auto Create", warna=Fore.MAGENTA)
        tampilkan_banner("Instagram", warna=Fore.BLUE, font="small")

        print(f"{Fore.GREEN}[1] Buat Akun Instagram")
        print(f"{Fore.YELLOW}[2] Keluar")
        print(Style.BRIGHT + Fore.MAGENTA + "="*40)
        
        pilihan = input(f"{Style.BRIGHT}Pilih menu: {Style.RESET_ALL}")
        
        if pilihan == '1':
            menu_buat_akun()
        elif pilihan == '2':
            print(f"{Fore.YELLOW}Terima kasih! Keluar dari program.")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid.")
        
        input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali ke menu...")