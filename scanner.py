# TOKENS
class Tokens:
    class OpenSquareBracket:
        def __init__(self, line) -> None:
            self.line = line
        def __repr__(self):
            return "OpenSquare"

    class CloseSquareBracket:
        def __init__(self, line) -> None:
            self.line = line
        def __repr__(self):
            return "CloseSquare"

    class OpenCurlyBracket:
        def __init__(self, line) -> None:
            self.line = line
        def __repr__(self):
            return "OpenCurly"

    class CloseCurlyBracket:
        def __init__(self, line) -> None:
            self.line = line
        def __repr__(self):
            return "CloseCurly"

    class Colon:
        def __init__(self, line) -> None:
            self.line = line
        def __repr__(self):
            return "Colon"

    class Comma:
        def __init__(self, line) -> None:
            self.line = line
        def __repr__(self):
            return "Comma"

    class String:
        def __init__(self, value, line) -> None:
            self.value = value
            self.line = line
        def __repr__(self):
            return f"str:{self.value[:10]}"

    class Number:
        def __init__(self, value, line) -> None:
            self.value = value
            self.line = line
        def __repr__(self):
            return f"num:{self.value}"

    class Bool:
        def __init__(self, value, line) -> None:
            self.value = value
            self.line = line
        def __repr__(self):
            return f"bool:{self.value}"

def string(stream, pos, line):
    i = pos
    if stream[i] != "\"": raise Exception("not string")
    i +=1
    value = ""

    while i < len(stream):
        if stream[i] == "\n": raise Exception("end of string unexpected")
        if stream[i] == "\"": break

        value += stream[i]

        i+=1

    return value

def number(stream, pos, line):
    n = ""
    i = pos
    isFloating = False

    while i < len(stream):
        if (ord(stream[i]) >= 49 and ord(stream[i]) <= 57):
            n += stream[i]
        elif stream[i] == ".":
            n += "."
            isFloating = True
        else:
            break

        i+=1

    if isFloating:
        return float(n)
    else:
        return int(n)
    
def boolean(stream, pos, line):
    if stream[pos: pos+4] == "true":
        return True
    elif stream[pos: pos+5] == "false":
        return False
    else:
        raise Exception(f"bool scan error at line {line}")
        
def scan_tokens(stream):
    # take in json as string, return array of tokens
    tokens = []
    i = 0
    line = 1

    while i < len(stream):
        if stream[i] == "[": tokens.append(Tokens.OpenSquareBracket(line))
        elif stream[i] == "]": tokens.append(Tokens.CloseSquareBracket(line))
        elif stream[i] == "{": tokens.append(Tokens.OpenCurlyBracket(line))
        elif stream[i] == "}": tokens.append(Tokens.CloseCurlyBracket(line))
        elif stream[i] == ":": tokens.append(Tokens.Colon(line))
        elif stream[i] == ",": tokens.append(Tokens.Comma(line))
        elif stream[i] == "\"":
            value = string(stream, i, line)
            tokens.append(Tokens.String(value, line))
            i += len(value) + 1
        elif ord(stream[i]) >= 49 and ord(stream[i]) <= 57:
            value = number(stream, i, line)
            tokens.append(Tokens.Number(value, line))
            i += len(str(value)) - 1
        elif stream[i:i+4] == "true" or stream[i:i+5] == "false":
            value = boolean(stream, i, line)
            tokens.append(Tokens.Bool(value, line))
            i += (3 if value else 4)
        elif stream[i] == "\n": line += 1
        elif stream[i] != " " and stream[i] != "\t":
            raise Exception(f"invalid token {stream[i]} on line {line}")

        i+=1

    return tokens