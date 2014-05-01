import re

def get_pars(text):
    pars = re.findall(r'\[[0-9]+\]\n*(.*)', text)
    pars = [p.strip() for p in pars]
    return pars

def get_claims(text):
    claims = re.findall(r'.*claim.*', text, re.IGNORECASE)
    return claims

def get_claim_body(text):
    match = re.search(r'^claim[s*]$', text, re.IGNORECASE | re.MULTILINE)
    try:
        claim = match.string[match.span()[0]:] 
        claim = claim.replace('*', '')
        return claim
    except(AttributeError):
        return 'none'


if __name__ == '__main__':

    import sys
    text = sys.stdin.read()

    for p in get_pars(text):
        print 'PARAGRAPH'
        print p


    for p in get_claims(text):
        print 'CLAIMS'
        print p

    print '---------'
    print get_claim_body(text)

