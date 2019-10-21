import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


SERVER_ADDR = '0.0.0.0'
SERVER_PORT = 8756


CASUAL_DATASET = ROOT_DIR+'/dataset/casual_data.txt'
BUSINESS_DATASET = ROOT_DIR+'/dataset/business_data.xlsx'
LSH_STORAGE_NAME = 'gtel_chatbot'

MODEL_DIR = 'model'
QA_DICT = 'model/QA_dict.pkl'
QUESTIONS = 'model/questions.pkl'
QUESTIONS_FULL = 'model/questions_full.pkl'
LSH_BIN = 'model/lsh.pkl'

LOG_DIR = 'log'
LOG_FILE = 'chatbot.log'

DISTANCE_THRESHOLD = 0.45