import argparse
import random
import datetime
import os
import time
from faker import Faker

fake = Faker()

# Domyślna ścieżka do foldera, gdzie zostaną zapisane access_log
DEFAULT_LOG_FOLDER = '.'

# Lista możliwych ścieżek ataku
attack_paths = [
    '/admin',
    '/login',
    '/wp-admin',
    '/phpmyadmin',
    '/shellshock',
    '/csrf',
    '/xxe',
    '/sqli',
    '/rce',
    '/path-traversal'
]

# Lista możliwych kodów odpowiedzi HTTP
status_codes = ['200', '404', '500']

def generate_attack_log():
    current_time = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S')
    remote_host = fake.ipv4()
    request_path = random.choice(attack_paths)
    http_status = random.choice(status_codes)
    user_agent = fake.user_agent()
    
    log_entry = f'{remote_host} - - [{current_time}] "GET {request_path} HTTP/1.1" {http_status} "-" "{user_agent}"'
    return log_entry

def generate_normal_log():
    current_time = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S')
    remote_host = fake.ipv4()
    request_path = random.choice(['/page1', '/page2', '/page3', '/home', '/about'])
    http_status = random.choice(status_codes)
    user_agent = fake.user_agent()
    
    log_entry = f'{remote_host} - - [{current_time}] "GET {request_path} HTTP/1.1" {http_status} "-" "{user_agent}"'
    return log_entry

def save_logs(filename, num_logs, interval):
    while num_logs > 0:
        log_entry = generate_attack_log() if random.random() < 0.5 else generate_normal_log()
        with open(os.path.join(log_folder, filename), 'a') as file:
            file.write(log_entry + '\n')
        num_logs -= 1
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description='Generate Apache access logs with attack patterns.')
    parser.add_argument('--num-logs', type=int, default=100, help='Number of logs to generate')
    parser.add_argument('--interval', type=int, default=5, help='Interval in seconds between log generation')
    parser.add_argument('--output-file', type=str, default='access_log', help='Output file name')
    parser.add_argument('--log-folder', type=str, default=DEFAULT_LOG_FOLDER, help='Folder where logs will be saved')
    args = parser.parse_args()

    global log_folder
    log_folder = args.log_folder

    print(f'Generating {args.num_logs} logs with {args.interval} seconds interval to {os.path.join(log_folder, args.output_file)}')
    save_logs(args.output_file, args.num_logs, args.interval)
    print('Logs generated successfully.')

if __name__ == '__main__':
    main()
