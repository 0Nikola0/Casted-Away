import sys
from pathlib import Path

if sys.version_info < (3, 8):
    sys.exit(
        "This game requires Python 3.8 or later."
    )

dist = Path(__file__).parent.resolve()

try:
    from src.game import Game
except ImportError:
    import traceback
    traceback.print_exc()
    with open(f'{dist}/requirements.txt', "r") as req:
        text = req.read()
    sys.exit(
        f"""
Please ensure you have the following packages installed:

{text}
You can run 'pip install -r requirements.txt' to install these 
(currently this will require a compiler to be configured).
        """)
