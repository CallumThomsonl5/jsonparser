from scanner import Tokens
import json


def parse_object(tokens):
    ret = {}

    if isinstance(tokens[0], Tokens.CloseCurlyBracket):
        tokens.pop(0)
        return {}

    while len(tokens) > 0:
        token = tokens.pop(0)

        assert isinstance(token, Tokens.String)
        key = token.value

        assert isinstance(tokens.pop(0), Tokens.Colon)
        token = tokens.pop(0)

        if isinstance(token, Tokens.OpenCurlyBracket):
            value = parse_object(tokens)
        elif isinstance(token, Tokens.OpenSquareBracket):
            value = parse_list(tokens)
        elif isinstance(token, Tokens.String) or isinstance(token, Tokens.Number) or isinstance(token, Tokens.Bool):
            value = token.value
        else:
            print(f"error at token {token} on line {token.line}")
            raise Exception("not valid value type")

        ret[key] = value

        # deal with comma, no trailing comma
        if not isinstance(tokens[0], Tokens.CloseCurlyBracket):
            assert isinstance(tokens.pop(0), Tokens.Comma)
        else:
            tokens.pop(0)
            break        

    return ret

def parse_list(tokens):
    ret = []

    # empty list
    if isinstance(tokens[0], Tokens.CloseSquareBracket):
        tokens.pop(0)
        return []

    while len(tokens) > 0:
        token = tokens.pop(0)
        if isinstance(token, Tokens.OpenCurlyBracket):
            value = parse_object(tokens)
        elif isinstance(token, Tokens.OpenSquareBracket):
            value = parse_list(tokens)
        elif isinstance(token, Tokens.String) or isinstance(token, Tokens.Number) or isinstance(token, Tokens.Bool):
            value = token.value
            return ret
        else:
            print(f"error at token {token} on line {token.line}")
            raise Exception("not valid value type")
        
        ret.append(value)
    
        if not isinstance(tokens[0], Tokens.CloseSquareBracket):
            assert isinstance(tokens.pop(0), Tokens.Comma)
        else:
            tokens.pop(0)
            break    

    return ret

def tokens_to_python(tokens):
    token = tokens.pop(0)
    if isinstance(token, Tokens.OpenCurlyBracket):
        ret = parse_object(tokens)
    elif isinstance(token, Tokens.OpenSquareBracket):
        ret = parse_list(tokens)
    else:
        raise Exception("json doesnt start with object or list")
            
    return ret