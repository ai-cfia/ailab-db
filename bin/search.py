import subprocess
import sys
import json
import logging
import ailab.db.api as api
import ailab.db as db
from microbench import MicroBench, MBReturnValue, MBFunctionCall
import pandas as pd


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Bench(MicroBench, MBFunctionCall, MBReturnValue):
    pass


OUTFILE = "benchmarking/search_results.json"
commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
basic_bench = Bench(
    output_file=OUTFILE, commit_version=commit, function_version="0.0.1"
)

@basic_bench
def init_bench(query):
    """Initialize the benchmark by calling the function search"""
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        return api.search_from_text_query(cursor, query)


if __name__ == "__main__":
    """Execute the sql search function with the query passed as an argument. 
    How to execute: python3 -m search.py query"""
    query = " ".join(sys.argv[1:])  
    logging.debug(f"Query is: {query}")
    results = init_bench(query)
    query_file_name = query.replace (" ", "-") + ".json"
    with open('tests/output/' + query_file_name, 'w+') as result_file:
        json.dump(results, result_file)
