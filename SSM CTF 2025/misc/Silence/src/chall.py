import string

allowed = '*0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[] _"'
flag = 'SSMCTF{wH0_ne3D5_std3Rr_wh3n_y0u_g0t_stdT1m3}'
assert all([part.isalnum() for part in flag.lstrip('SSMCTF{').rstrip('}').split('_')])

while True:
    try:
        import sys
        sys.stdout = sys.__stdout__
        code = input('> ')
        sys.stdout = "a" # do you really need stdout?
        del sys
        
        if any([i not in allowed for i in code]):
            continue
        if any([i in code for i in ["import", "exec", "eval", "__"]]):
            continue
        if any([i not in string.printable for i in code]):
            continue
        eval(code)
    except Exception as e: # good luck outputting anything to stderr!
        pass