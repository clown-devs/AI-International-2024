import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parser.parser import parse_file

def get_marked_edf(unmarked_filename):
    data, swd, is_, ds = parse_file(unmarked_filename)
    return "static/hardcoded.edf", data
    


def get_ai_data(filepath):
    parsed, _, _, _ = parse_file(filepath)
    data, swd, is_, ds = parse_file("")
    return data