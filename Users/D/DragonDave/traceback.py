import sys, traceback

def catcher():
    print "Exception in user code:"
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60

def run_user_code():
    try:
        run_user_code()
    except:
        catcher()

run_user_code()