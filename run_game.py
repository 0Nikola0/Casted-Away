import sys
from src.settings import REQUIREMENTS

if sys.version_info < (3, 8):
    sys.exit(
        "This game requires Python 3.8 or later."
    )

try:
    from src.game import Game
    Game().run()

except ImportError:
    import traceback
    traceback.print_exc()
    with open(REQUIREMENTS, "r") as f:
        req = f.read()
    sys.exit(
        f"""
Please ensure you have the following packages installed:

{req}
You can run 'pip install -r requirements.txt' to install these.
        """)
