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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
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
def baca_semua_akun(file_path='akun.txt'):
    list_akun = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            akun_buffer = {}
            for line in file:
                line = line.strip()
                if '=========================' in line:
                    if akun_buffer.get('username'):
                        list_akun.append(akun_buffer)
                    akun_buffer = {}
                elif ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key in ['username', 'sandi', 'email']:
                        akun_buffer[key] = value
            if akun_buffer.get('username'):
                list_akun.append(akun_buffer)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_path}' tidak ditemukan.")
    return list_akun
def simpan_akun_tersisa(akun_tersisa, file_path='akun.txt'):
    with open(file_path, 'w', encoding='utf-8') as f:
        for i, akun in enumerate(akun_tersisa):
            f.write(f"email: {akun.get('email', '')}\n")
            f.write(f"username: {akun.get('username', '')}\n")
            f.write(f"sandi: {akun.get('sandi', '')}\n")
            if i < len(akun_tersisa) - 1:
                f.write("=========================\n")
def get_target_stats(driver, wait, target_url):
    base_url = target_url.split('/followers')[0].split('/following')[0]
    print(f"\n🔗 Mengunjungi profil target: {base_url}")
    driver.get(base_url)
    try:
        header_xpath = "//header"
        wait.until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
        time.sleep(2) 
        followers_link = driver.find_element(By.XPATH, f"//a[contains(@href, '/followers/')]")
        following_link = driver.find_element(By.XPATH, f"//a[contains(@href, '/following/')]")
        followers_text = followers_link.text.split()[0]
        following_text = following_link.text.split()[0]
        print(f"{Fore.GREEN}📊 Statistik Ditemukan: Followers: {followers_text}, Following: {following_text}")
        return followers_text, following_text, followers_link, following_link
    except Exception:
        print(f"{Fore.RED}❌ Gagal mendapatkan statistik. Kemungkinan akun privat atau URL salah.")
        return None, None, None, None
def run_follow_process(driver, wait, list_to_click, max_follows):
    list_to_click.click()
    print(" K️otak daftar dibuka...")
    SCROLLABLE_AREA_CLASS = "x1mg3h75" 
    scrollable_div_xpath = f"//div[@role='dialog']//div[contains(@class, '{SCROLLABLE_AREA_CLASS}')]"
    print(f"🔍 Mencari area scroll dengan class: '{SCROLLABLE_AREA_CLASS}'...")
    wait.until(EC.presence_of_element_located((By.XPATH, scrollable_div_xpath)))
    print("✅ Area scroll ditemukan!")
    time.sleep(2)
    followed_count = 0
    scroll_attempts = 0
    while followed_count < max_follows:
        try:
            first_button_xpath = f"({scrollable_div_xpath}//button[.//div[text()='Follow'] or .//div[text()='Ikuti']])[1]"
            button_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, first_button_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_to_click)
            time.sleep(random.uniform(0.5, 1.5))
            driver.execute_script("arguments[0].click();", button_to_click)
            followed_count += 1
            scroll_attempts = 0
            print(f"{Fore.GREEN}✔ ({followed_count}/{max_follows}) Follow berhasil!{Style.RESET_ALL}")
            delay = random.uniform(3, 5)
            print(f"   -> Jeda {delay:.1f} detik...")
            time.sleep(delay)
        except TimeoutException:
            print("... Tidak ada tombol 'Follow' ditemukan, mencoba scroll...")
            try:
                scrollable_div = driver.find_element(By.XPATH, scrollable_div_xpath)
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            except NoSuchElementException:
                print("Area scroll tidak ditemukan lagi, mengakhiri.")
                break
            time.sleep(random.uniform(2, 4))
            scroll_attempts += 1
            if scroll_attempts > 3:
                print("Tidak menemukan tombol baru setelah beberapa kali scroll. Proses selesai untuk akun ini.")
                break
        except Exception as e:
            if "Try Again Later" in driver.page_source:
                print(f"{Fore.RED}❌ Terdeteksi Action Block 'Try Again Later' dari Instagram. Menghentikan akun ini.")
                break
            print(f"❌ Terjadi error di dalam loop: {e}")
            time.sleep(2)  
    print(f"\n🎉 Selesai untuk akun ini! Total di-follow: {followed_count}")
def login_instagram_headless(username, password):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_argument("--headless=new")
        options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 20)
        driver.get("https://www.instagram.com/accounts/login/")
        wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg' and @aria-label='Home']")))
        print(f"{Fore.GREEN}✅ Login Berhasil!{Style.RESET_ALL}")
        try:
            not_now_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now' or text()='Nanti Saja']")))
            not_now_button.click()
            print("ℹ️ Pop-up notifikasi ditutup.")
        except TimeoutException:
            print("ℹ️ Tidak ada pop-up notifikasi.")
        return driver, wait
    except Exception as e:
        print(f"{Fore.RED}❌ Login Gagal atau Error Kritis: {e}{Style.RESET_ALL}")
        if driver:
            driver.quit()
        return None, None
def menu_auto_follow():
    target_url = ""
    while not target_url.startswith("https://www.instagram.com/"):
        target_url = input(f"{Style.BRIGHT}{Fore.YELLOW}>> Masukkan URL profil target: {Style.RESET_ALL}")
        if not target_url.startswith("https://www.instagram.com/"):
            print(f"{Fore.RED}❌ URL tidak valid. Harap masukkan URL Instagram yang benar.")
    try:
        max_follows = int(input(f"{Style.BRIGHT}{Fore.YELLOW}>> Jumlah akun yang ingin di-follow? (misal: 15): {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}⚠️ Input tidak valid, menggunakan default 15.")
        max_follows = 15
    semua_akun = baca_semua_akun()
    if not semua_akun:
        print(f"{Fore.YELLOW}Tidak ada akun di 'akun.txt' untuk diproses.")
        return
    list_choice = None
    for i, akun in enumerate(semua_akun):
        print(f"\n{Style.BRIGHT}{Fore.CYAN}--- MEMPROSES AKUN KE-{i+1}: {akun['username']} ---{Style.RESET_ALL}")
        driver_instance, wait_instance = login_instagram_headless(akun['username'], akun['sandi'])
        if driver_instance and wait_instance:
            try:
                if list_choice is None:
                    followers_count, following_count, followers_link_el, following_link_el = get_target_stats(driver_instance, wait_instance, target_url)
                    if not followers_count:
                        print("Gagal mendapatkan statistik dengan akun pertama, membatalkan.")
                        break
                    user_input = ''
                    while user_input not in ['1', '2']:
                        print("\n" + "="*50)
                        print("PILIH SUMBER UNTUK DI-FOLLOW (Pilihan ini akan digunakan untuk semua akun)")
                        print(f"1. Dari daftar Followers ({followers_count})")
                        print(f"2. Dari daftar Following ({following_count})")
                        print("=" * 50)
                        user_input = input(">> Masukkan pilihan (1/2): ")
                    list_choice = user_input
                _, _, followers_link, following_link = get_target_stats(driver_instance, wait_instance, target_url)
                if not followers_link:
                    print("Gagal menemukan link followers/following, melewati akun ini.")
                    driver_instance.quit()
                    continue
                list_to_click = followers_link if list_choice == '1' else following_link
                run_follow_process(driver_instance, wait_instance, list_to_click, max_follows)
            except Exception as e:
                print(f"{Fore.RED}❌ Terjadi error tak terduga saat proses follow: {e}{Style.RESET_ALL}")
            finally:
                print(f"{Fore.BLUE}Menutup sesi untuk akun {akun['username']}...{Style.RESET_ALL}")
                driver_instance.quit()
        else:
            print(f"{Fore.YELLOW}Melewati akun {akun['username']} karena gagal login.{Style.RESET_ALL}")
        if i < len(semua_akun) - 1:
            jeda_antar_akun = random.randint(10, 30)
            print(f"\n--- Jeda {jeda_antar_akun} detik sebelum lanjut ke akun berikutnya ---")
            time.sleep(jeda_antar_akun)
def menu_login_akun():
    semua_akun = baca_semua_akun()
    if not semua_akun:
        print(f"{Fore.YELLOW}Tidak ada akun di 'akun.txt' untuk diproses.")
        return
    for i, akun in enumerate(semua_akun):
        print(f"\n{Style.BRIGHT}{Fore.CYAN}--- MEMPROSES AKUN: {akun['username']} ---{Style.RESET_ALL}")
        driver_instance = None
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_argument("--headless=new")
            driver_instance = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(driver_instance, 20)
            driver_instance.get("https://www.instagram.com/accounts/login/")
            wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(akun['username'])
            wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(akun['sandi'])
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg' and @aria-label='Home']")))
            print(f"{Fore.GREEN}✅ STATUS: Login Berhasil!")
        except Exception:
            print(f"{Fore.RED}🔥 STATUS: Login Gagal atau Error Kritis.")
        finally:
            if driver_instance:
                driver_instance.quit()
        if i < len(semua_akun) - 1:
            print(f"\n--- Jeda 10 detik sebelum lanjut ke akun berikutnya ---")
            time.sleep(10)
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
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_argument("--disable-notifications")
            options.add_argument("--log-level=3")
            options.add_argument("--headless=new")
            user_agent_terpilih = random.choice(USER_AGENTS)
            options.add_argument(f'user-agent={user_agent_terpilih}')
            print(f"{Fore.BLUE}INFO: User-Agent -> {user_agent_terpilih[:50]}...{Style.RESET_ALL}")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(driver, 60)
            print(f"{Fore.BLUE}➡️ Menjalankan pendaftaran & verifikasi...{Style.RESET_ALL}")
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            instagram_tab = driver.current_window_handle
            driver.switch_to.new_window('tab')
            driver.get("https://tempmail.ac.id/")
            while True:
                email_div_xpath = "//div[contains(text(), '@') and not(contains(text(), 'Copyright')) and string-length(text()) > 5]"
                email_element = wait.until(EC.presence_of_element_located((By.XPATH, email_div_xpath)))
                temp_email = email_element.text.strip()
                email_domain = temp_email.split('@')[1].strip().lower()
                if email_domain in BLACKLISTED_DOMAINS:
                    print(f"{Fore.YELLOW}🚫 Domain terlarang: {email_domain}. Meminta email baru...{Style.RESET_ALL}")
                    delete_button_xpath = "//div[normalize-space()='Delete'] | //button[contains(., 'Delete')]"
                    wait.until(EC.element_to_be_clickable((By.XPATH, delete_button_xpath))).click()
                    time.sleep(5)
                    driver.refresh()
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
            wait.until(EC.presence_of_element_located((By.XPATH, "//select[@title='Month:']"))).send_keys("August")
            wait.until(EC.presence_of_element_located((By.XPATH, "//select[@title='Day:']"))).send_keys("15")
            wait.until(EC.presence_of_element_located((By.XPATH, "//select[@title='Year:']"))).send_keys("1995")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))).click()
            driver.switch_to.window(driver.window_handles[1])
            subject_div_xpath = "//div[contains(@class, 'cursor-pointer')]//div[contains(., 'is your Instagram code') or contains(., 'adalah kode Instagram Anda')]"
            subject_element = wait.until(EC.presence_of_element_located((By.XPATH, subject_div_xpath)))
            otp_match = re.search(r'\b\d{6}\b', subject_element.text)
            if not otp_match: raise Exception("Gagal mengekstrak OTP.")
            otp_code = otp_match.group(0)
            print(f"{Fore.GREEN}🔑 Kode OTP: {otp_code}{Style.RESET_ALL}")
            driver.switch_to.window(instagram_tab)
            wait.until(EC.element_to_be_clickable((By.NAME, "email_confirmation_code"))).send_keys(otp_code)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Next']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg' and @aria-label='Home']")))
            print(f"{Style.BRIGHT}{Fore.GREEN}✅ Pendaftaran Instagram Berhasil!{Style.RESET_ALL}")
            with open("akun.txt", "a", encoding="utf-8") as f:
                f.write(f"email: {temp_email}\nusername: {username}\nsandi: {password}\n=========================\n")
            print(f"{Fore.GREEN}✅ Akun disimpan di akun.txt{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Style.BRIGHT}{Fore.RED}❌ Gagal membuat akun ke-{i+1}: {e}{Style.RESET_ALL}")
        finally:
            if driver:
                print(f"{Fore.YELLOW}🎉 Proses untuk akun ini selesai. Menutup browser...{Style.RESET_ALL}")
                driver.quit()
if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        tampilkan_banner("Instagram BOT", warna=Fore.MAGENTA)
        print(f"{Fore.GREEN}[1] Buat Akun Instagram")
        print(f"{Fore.CYAN}[2] Cek Login Akun dari file")
        print(f"{Fore.YELLOW}[3] Auto Follow dari Target")
        print(f"{Fore.RED}[4] Keluar")
        print(Style.BRIGHT + Fore.MAGENTA + "="*40)
        pilihan = input(f"{Style.BRIGHT}Pilih menu: {Style.RESET_ALL}")
        if pilihan == '1':
            menu_buat_akun()
        elif pilihan == '2':
            menu_login_akun()
        elif pilihan == '3':
            menu_auto_follow()
        elif pilihan == '4':
            print(f"{Fore.YELLOW}Terima kasih! Keluar dari program.")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid.")
        input(f"\n{Fore.YELLOW}Tekan Enter untuk kembali ke menu...")
