import os

from pi_dawn import app
from pi_dawn import hw

if os.environ.get('DEBUG', '0') == '1':
    wired = hw.Pygame(width=10, height=32)
else:
    wired = hw.WS2801(width=10, height=32, gamma_r=app.config['GAMMA_R'], gamma_b=app.config['GAMMA_B'],
                    gamma_g=app.config['GAMMA_G'])
