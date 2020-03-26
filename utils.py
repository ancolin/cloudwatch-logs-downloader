# coding: utf-8
import boto3
import os
import json
import datetime
import csv


class Utils:
    flg_debug = False

    key_events = 'events'
    key_next_forward_token = 'nextForwardToken'

    key_timestamp = 'timestamp'
    key_message = 'message'
    key_ingestion_time = 'ingestionTime'

    def setFlgDebug(self, flg=False):
        self.flg_debug = True

    def log(self, m):
        if self.flg_debug is True:
            print(str(m))

    def getEvents(self, log_group_name, log_stream_name, region_name):
        list_events = []
        for events in self.request(
                log_group_name=log_group_name,
                log_stream_name=log_stream_name,
                region_name=region_name
        ):
            for e in events:
                list_events.append(e)

        return {self.key_events: list_events}

    def request(self, log_group_name, log_stream_name, region_name):
        client = boto3.client('logs', region_name=region_name)

        # ログは 1 リクエストに付き 1 MB までなのでループして取得する

        # 1 度目のリクエスト
        response = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            startFromHead=True
        )
        yield response[self.key_events]

        # 2 度目以降のリクエスト
        while True:
            next_token = response[self.key_next_forward_token]
            response = client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                nextToken=next_token
            )

            # 同じトークンを受け取ったら終わり
            if response[self.key_next_forward_token] == next_token:
                break

            yield response[self.key_events]

    def outputJson(self, base_dir, filename, content):
        if os.path.isdir(base_dir) is False:
            os.makedirs(base_dir)
        with open(base_dir + '/' + filename, 'w') as f:
            f.write(json.dumps(content))

    def outputCsv(self, base_dir, filename, content):
        list_logs = [[
            self.key_timestamp,
            self.key_message,
            self.key_ingestion_time
        ]]

        for d in content[self.key_events]:
            list_logs.append([
                datetime.datetime.fromtimestamp(int(d[self.key_timestamp]) / 1000),
                d[self.key_message],
                datetime.datetime.fromtimestamp(int(d[self.key_ingestion_time]) / 1000)
            ])

        if os.path.isdir(base_dir) is False:
            os.makedirs(base_dir)
        with open(base_dir + '/' + filename, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(list_logs)

    def outputText(self, base_dir, filename, content):
        string_logs = ''

        for d in content[self.key_events]:
            string_logs += d[self.key_message]

        if os.path.isdir(base_dir) is False:
            os.makedirs(base_dir)
        with open(base_dir + '/' + filename, 'w') as f:
            f.write(string_logs)
