from datetime import datetime
import re
import sys
import getopt



LOG_ENTRY_REGEX = '.*?\\[(.*)\\].*?(/.*?) .*?" (\d+).*'
TIMESTAMP_FORMAT = '%d/%b/%Y:%H:%M'
OUTPUT_TIMESTAMP_FORMAT ='%Y-%m-%dT%H:%M'


class Stat:
    def __init__(self, timestamp):
        self.start = None
        self.good = 0
        self.total = 0
        self.timestamp = timestamp


class LogParser:
    def __init__(self, filename, start, end, interval, success_codes):
        self.filename = filename
        self.start = datetime.strptime(start,
                                       OUTPUT_TIMESTAMP_FORMAT)
        self.end = datetime.strptime(end,
                                     OUTPUT_TIMESTAMP_FORMAT)
        self.interval = interval
        self.success_codes = success_codes
        self.stats = dict()
        self.processed = list()


    def _parse_entry(self, entry):
        groups = re.match(LOG_ENTRY_REGEX, entry).groups()

        timestamp, endpoint, status_code = groups

        timestamp = datetime.strptime(timestamp.rsplit(':', 1)[0],
                                      TIMESTAMP_FORMAT)

        if timestamp < self.start or timestamp > self.end:
            return

        # Eliminate anchor and query params
        for character in ('?', '#'):
            pos = endpoint.find(character)

            if pos != -1:
                endpoint = endpoint[:pos]

        if endpoint in self.stats:
            delta = timestamp - self.stats[endpoint].timestamp
            # If current entry is more than `interval` mins away from the
            # current one, add the current one to the processed list
            if delta.total_seconds() / 60 >= self.interval:
                self.processed.append((endpoint, self.stats[endpoint]))
                self.stats[endpoint] = Stat(timestamp)
        else:
            self.stats[endpoint] = Stat(timestamp)

        if status_code in self.success_codes:
            self.stats[endpoint].good += 1

        self.stats[endpoint].total += 1


    def parse(self):
        for line in open(self.filename, 'r'):
            entry = line.strip()

            if not entry:
                break

            self._parse_entry(entry)
        # Add remaining entries to the processed list
        self.processed += [(endpoint, stat)
                           for endpoint, stat in self.stats.items()]
        # Sort entries by timestamp and by endpoint
        self.processed.sort(key=lambda data: (data[1].timestamp, data[0]))


    def print_stats(self):
        for endpoint, stat in self.processed:
            print('%s %d %s %.2f' % (stat.timestamp.strftime(OUTPUT_TIMESTAMP_FORMAT),
                                     self.interval,
                                     endpoint,
                                     round(100.0 * stat.good / stat.total, 2)))
