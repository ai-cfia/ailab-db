# Name of this file: search.py
# Location: at the root of the project
# How to execute: python3 -m search.py query

import subprocess
import sys
import louis.db.api as api
import louis.db as db
from microbench import MicroBench, MBReturnValue, MBFunctionCall
import pandas as pd

class Bench(MicroBench, MBFunctionCall, MBReturnValue):
    pass
output_file = "benchmarking/search_results.json"
commit_version = subprocess.check_output(["git", "rev-parse", "HEAD"])\
    .strip().decode('utf-8')

basic_bench = Bench(outfile=output_file, commit_version=commit_version, \
                    function_version="0.0.1")

@basic_bench 
def search(cursor, query):
    """Execute the SQL search function"""
    return api.search_from_text_query(cursor, query)

if __name__ == '__main__':
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        results = search(cursor, ' '.join(sys.argv[1:]))
    print(results)
    
    with open(output_file, 'r') as result_file:
        print(pd.read_json(result_file, lines=True))
    


