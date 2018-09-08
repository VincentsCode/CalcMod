import calclib


# noinspection PyBroadException
def main():
    try:
        while True:
            try:
                expr = input('').strip()
                if expr:
                    expr = calclib.tokenize(expr)
                    expr = calclib.implicit_multiplication(expr)
                    expr = calclib.to_rpn(expr)
                    res = calclib.eval_rpn(expr)
                    print('%g' % res)
            except Exception:
                pass
    except Exception:
        pass


if __name__ == '__main__':
    main()
