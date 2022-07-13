from core.core import *
from source.app import *
from config.config import *

blockchain = BlockChain()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)