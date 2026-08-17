
# Imports
import stouputils as stp
from stewbeet import Context, JsonFile


# Functions
def beet_default(ctx: Context) -> None:
    """ Patch JSON files with a custom encoder that indents them for readability. """

    # Patch all JSON files
    patched: list[str] = []
    for path, obj in (*ctx.data.all(), *ctx.assets.all()):
        if isinstance(obj, JsonFile):
            patched.append(f"- {("'"+path):>42}' of type {obj.__class__.__name__}")

            # Change the encoder by a max level of 2 indentation
            obj.encoder = lambda x: stp.json_dump(x, ensure_ascii=True)
            obj._content = stp.json_dump(obj.data, ensure_ascii=True) # type: ignore

    # Output
    if patched:
        stp.debugc(f"Patched {len(patched)} JSON files:\n" + "\n".join(patched))

