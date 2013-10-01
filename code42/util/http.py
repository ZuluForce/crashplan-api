
from code42.util.container import Bunch

# Could probably improve the verbosity of this definition but the way
# the 'Bunch' object works I have to provide some value per key and that
# is what will be printed
verbs = Bunch(GET='GET', PUT='PUT', POST='POST', DELETE='DELETE')

def print_redirect_history(resp):
    print "== Redirect History =="
    print "Final url: <{0.status_code}> {0.url}".format(resp)
    
    history = resp.history
    hist_count = 1
    while history is not None and len(history) > 0:
        history = history[0]
        print  "Final-{0}: <{1.status_code}> {1.url}".format(hist_count, history)

        history = history.history
        hist_count += 1

    print "== End Redirect History =="
