#!/usr/bin/env python3

import sys, os, asyncio, traceback
# from concurrent.futures import ThreadPoolExecutor as Executor   # or ProcessPoolExecutor as Executor
import langdetect 


name = 'SUMMA-LanguageDetection'      # required by rabbitmq module
# executor = None

# required
def init(max_workers=1):
    # global executor
    # executor = Executor(max_workers=max_workers)
    # init_module()                           # initialize in calling thread
    # executor.submit(init_module).result()   # initialize in worker thread and wait to complete
    pass


def setup_argparser(parser):
    env = os.environ


# required, but may not be called
def shutdown():
    # global executor
    # executor.shutdown()
    pass

# async def run(text, feed_lang, loop=None):
#     if not loop:
#         loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(executor, run_detection, text, feed_lang)

# required by rabbitmq module
async def process_message(task_data, loop=None, send_reply=None, **kwargs):
    return run_detection(task_data.get('text'), task_data.get('feedLang'))
    # result = await run(task_data.get('text'), task_data.get('feedLang'), loop)
    # if type(result) is str:
    #     return result
    # return ''.join(result)


# --- private ---

def init_module():
    pass
    # print('Setting up language detection models')

def run_detection(text, feed_lang):
    lang = langdetect.detect(text)
    if lang != feed_lang:
        print('Language mismatch: detected-language=%s, feed-language=%s' % (lang, feed_lang))
        print('Input text:', text)
    return lang


if __name__ == "__main__":

    import argparse, json

    parser = argparse.ArgumentParser(description='Language Detection Task', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', action='store_true', help='enable debug mode') 
    # parser.add_argument('--parallel', '-n', dest='PARALLEL', metavar='PORT', type=int, default=os.environ.get('PARALLEL',1),
    #         help='messages to process in parallel (or set env variable PARALLEL)')
    parser.add_argument('filename', type=str, default='test.json', nargs='?', help='text file or JSON file with task data')

    setup_argparser(parser)

    args = parser.parse_args()

    init(args)

    print('Reading', args.filename)
    with open(args.filename, 'r') as f:
        if args.filename.endswith('.json'):
            task_data = json.load(f).get('taskData')
        else:
            task_data = dict(text=f.read())
    metadata = {}

    async def print_partial(partial_result):
        print('Partial result:')
        print(partial_result)

    try:
        loop = asyncio.get_event_loop()
        # loop.set_debug(True)
        result = loop.run_until_complete(process_message(task_data, loop=loop, send_reply=print_partial, metadata=metadata))
        print('Result:')
        print(result)
    except KeyboardInterrupt:
        print('INTERRUPTED')
    except:
        print('EXCEPTION')
        traceback.print_exc()
        # raise
    finally:
        shutdown()
