import random
from datetime import datetime, timedelta


ips = [
    '1.2.3.4',
    '8.8.8.8',
    '10.10.10.10',
    '192.168.100.23',
    '172.16.35.10',
    '172.24.60.30',
]

methods = [
    'GET',
]

code_prefixes = [
    '20',
    '20',
    '20',
    '20',
    '20',
    '30',
    '40',
    '50',
]

users = [
    'grandfather',
    'receptive',
    'defiant',
    'outrageous',
    'rain',
    'pump',
    'ready',
    'wealth',
    'play',
    'direful',
    'lamentable',
    'crowded',
    'ubiquitous',
    'command',
    'tangy',
    'brave',
    'blind',
    'voracious',
    'pen',
    'geese',
]

queries = [
    'tasty',
    'owe',
    'dry',
    'permissible',
    'trip',
    'friendly',
    'show',
    'fine',
    'drink',
    'sudden',
    'fluffy',
    'burst',
    'clip',
    'locket',
    'suggest',
    'reason',
    'thoughtful',
    'giraffe',
    'quack',
    'volatile',
]

query_value = [
    'steer',
    'mindless',
    'panicky',
    'milk',
    'husky',
    'truthful',
    'recondite',
    'teeny',
    'shaggy',
    'fact',
    'furniture',
    'bounce',
    'window',
    'divide',
    'trip',
    'reduce',
    'alert',
    'undesirable',
    'mind',
    'van',
]

endpoint_prefix = [
    'bomb',
    'rest',
    'inject',
    'bizarre',
    'cagey',
    'spiteful',
    'hair',
    'quiet',
    'glue',
    'march',
    'ball',
    'annoyed',
    'son',
    'mark',
    'signal',
    'committee',
    'voiceless',
    'purpose',
    'note',
    'slim',
]

system = [
    'ubuntu',
    'fedora',
    'kubuntu',
    'ubuntu-gnome',
    'rhel',
    'windows',
    'kali',
    'linux-mint',
    'uso-v7',
    'rl-v5',
]

anchors = [
    'close',
    'post',
    'grateful',
    'dramatic',
    'minor',
    'immense',
    'wish',
    'route',
    'ignorant',
    'anxious',
    'bashful',
    'awesome',
    'modern',
    'dapper',
    'welcome',
    'stroke',
    'water',
    'colour',
    'abaft',
    'monkey',
]


# 10.10.10.10 - - [22/Feb/2017:18:45:02 +0000] "GET /so.html?user=gheorghe HTTP/1.1" 403 533 "-" "python-requests/2.12.4"
ENTRY_FORMAT = '{ip} - - [{timestamp} +0000] "{method} {endpoint} HTTP/1.1" {code} {size} "-" "python-requests/2.12.4"'


def generate_endpoint(prefix_length):
    suffix = random.choice(system) + '.html'

    if prefix_length:
        prefix = '/' + '/'.join(random.choice(endpoint_prefix)
                                for i in range(prefix_length))

        return prefix + '/' + suffix

    return '/' + suffix


def generate_query():
    return '?' + random.choice(queries) + '=' + random.choice(query_value)


def generate_anchor():
    return '#' + random.choice(anchors)


def generate_log(output_file, n_entries, n_endpoints, prefix_length, timestamp_step):
    out = open(output_file, 'w')

    start_time = datetime.now() + timedelta(days=random.randint(-500, 0),
                                            minutes=random.randint(0, 60),
                                            hours=random.randint(0, 24))

    endpoints = [generate_endpoint(prefix_length) for i in range(n_endpoints)]

    for entry_number in range(n_entries):
        ip = random.choice(ips)
        timestamp = start_time.strftime('%d/%b/%Y:%H:%M:%S')
        method = random.choice(methods)
        endpoint = random.choice(endpoints)
        size = random.randint(500, 2000)

        if random.randint(0, 4) == 0:
            endpoint += generate_query()

        if random.randint(0, 5) == 0:
            endpoint += generate_anchor()

        code = random.choice(code_prefixes) + str(random.randint(0, 5))

        entry = ENTRY_FORMAT.format(ip=ip,
                                    timestamp=timestamp,
                                    method=method,
                                    endpoint=endpoint,
                                    code=code,
                                    size=size)

        print(entry, file=out)

        start_time += timedelta(seconds=random.randint(0, timestamp_step))

    out.close()


if __name__ == '__main__':
    params = [
        ('tests/test0.log', 10, 3, 0, 10),
        ('tests/test1.log', 1000, 3, 0, 3),
        ('tests/test2.log', 1000, 3, 0, 30),
        ('tests/test3.log', 1000, 3, 0, 300),
        ('tests/test4.log', 10000, 10, 3, 3),
        ('tests/test5.log', 10000, 10, 3, 30),
        ('tests/test6.log', 10000, 10, 3, 300),
        ('tests/test7.log', 70000, 30, 5, 3),
        ('tests/test8.log', 70000, 30, 5, 30),
        ('tests/test9.log', 70000, 30, 5, 300),
        ('tests/test10.log', 400000, 30, 5, 10),
    ]

    for i, param in enumerate(params):
        generate_log(*param)
