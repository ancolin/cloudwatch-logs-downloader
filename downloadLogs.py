# coding: utf-8
import sys
from utils import Utils

u = Utils()
u.setFlgDebug(True)

try:
    argv = sys.argv

    if len(argv) < 4:
        print('this script needs 3 arguments.')
        print('#1 log group name. (ex. /aws/lambda/fooFunction)')
        print('#2 log stream name. (ex. 2020/03/25[$LATEST]foobar)')
        print('#3 region name. (ex. ap-northeast-1)')
        print('#4 output format. default json. (format: json, csv, txt)')
    else:
        # ログの情報を取得する
        log_group_name = argv[1]
        log_stream_name = argv[2]
        region_name = argv[3]

        # 出力フォーマットを取得する
        output_format = 'json'
        if len(argv) > 4:
            output_format = argv[4]

        if output_format != 'json' and output_format != 'csv' and output_format != 'txt':
            print('invalid output format. you can use json, csv or txt. if not specified, use json.')
            quit(1)

        # ログを取得する
        events = u.getEvents(log_group_name, log_stream_name, region_name)

        # ログを JSON 形式でファイルに出力する
        base_dir = 'logs'
        filename = log_group_name.split('/')[-1] + '-' + log_stream_name.split(']')[-1].split('/')[-1] + '.' + output_format
        if output_format == 'csv':
            u.outputCsv(base_dir, filename, events)
        elif output_format == 'json':
            u.outputJson(base_dir, filename, events)
        elif output_format == 'txt':
            u.outputText(base_dir, filename, events)

        print('output logs: ' + base_dir + '/' + filename)

except Exception as e:
    u.log(e)
