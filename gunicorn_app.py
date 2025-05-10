import os
from src.app import create_app

# Cria a aplicação com configuração de produção
app = create_app('production')