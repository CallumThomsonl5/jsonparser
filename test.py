from scanner import scan_tokens
from parse import tokens_to_python
import json



def main():
    with open("testfiles/complex.json") as f:
        data = f.read()

    tokens = scan_tokens(data)
    parsed = tokens_to_python(tokens)
    
    assert parsed == json.loads(data)

if __name__ == "__main__":
    main()