import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parser.parser import parse_file, save_to_edf
from .word import save_analytics_to_word
def get_marked_edf(unmarked_filename, hash):
    hardcoded_file = "server/static/hardcoded.edf" # Добавить обработку нейронки
    data, swd, is_, ds = parse_file(hardcoded_file)

    marked_filename = f"static/{hash}_marked.edf"
    analytics = save_to_edf(data, "server/"+marked_filename)
    save_analytics_to_word(analytics, f"server/static/{hash}.docx")

    return marked_filename, data
    


def get_ai_data(filepath):
    parsed, _, _, _ = parse_file(filepath)
    data, swd, is_, ds = parse_file("")
    return data