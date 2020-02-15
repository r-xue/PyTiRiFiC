def can_evaluate(string):
    try:
        eval(string)
        return True
    except SyntaxError:
        return False
    
if  __name__=="__main__":
    
    can_evaluate('aa')