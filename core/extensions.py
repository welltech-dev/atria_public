from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# RATE LIMIT
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)

MAX_TENTATIVAS = 5
BLOQUEIO_MINUTOS = 15