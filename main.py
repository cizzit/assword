import webapp2
import os
import jinja2
import random
import re
import string

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


DEBUG=True
CUSSWORDFILE='cusswords.txt'

def leetify(text):
    rules = (
        (('are', 'Are'), 'r'),
        (('ate', 'Ate'), '8'),
        (('that', 'That'), 'tht'),
        (('you', 'You'), 'j00'),
        (('o'), ('o', 'O', '0')),
        (('i'), ('i', 'I', 'l', '1')),
        (('e'), ('3', 'e', 'E')),
        (('s'), ('5', 's', 'S', '$')),
        (('a'), ('4', 'a', 'A', '@')),
        (('t'), ('7', 't', 'T', '+')),
        (('b'), ('b', 'B', '8')),
        (('c'), ('c', 'C', '(')),
        (('d'), ('d', 'D', '|)')),
        (('f'), ('f', 'F')),
        (('g'), ('g', 'G', '6', '9')),
        (('h'), ('h', 'H', '|-|', '#')),
        (('j'), ('j', 'J')),
        (('k'), ('k', 'K')),
        (('l'), ('l', 'L', '1', '!')),
        (('m'), ('m', 'M', '44')),
        (('n'), ('n', 'N')),
        (('p'), ('p', 'P')),
        (('q'), ('q', 'Q')),
        (('r'), ('r', 'R')),
        (('u'), ('u', 'U')),
        (('v'), ('v', 'V', '\\/')),
        (('w'), ('w', 'W', '\\/\\/')),
        (('x'), ('x', 'X')),
        (('y'), ('y', 'Y')),
        (('z'), ('z', 'Z', '2'))
    )
    for befores, after in rules:
        for before in befores:
            text = text.replace(before, random.choice(after))
    return text

class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)

# generates a list of cuss words from the text file
# requires: none
# returns: list
def createWordList():
    global CUSSWORDFILE
    lines=[line.strip() for line in open(CUSSWORDFILE)]
    return lines

class MainPage(MainHandler):
    def get(self):
        length = self.request.get('l') or 10 #10 is default length
        length = int(length)
        test=[]
        #get a list of cusswords
        cuss = createWordList()
        icuss = random.choice(cuss) #individual, random, cuss word
        newcuss = leetify(icuss)
        i=0
        #if this function doesn't change the cussword (possible) then run it again until it does.
        while newcuss == icuss:
            i+=1
            newcuss = leetify(icuss)
            #if this while loop is being annoying and continuing, break out at 50.
            if i==50:
                break

        #newcuss is now different from icuss
        # add random characters to start and end of word
        
        lcuss = len(newcuss)
        lengthcuss = length - lcuss
        lcdt = lengthcuss / 2
        if lcdt <1:
            lcdt = 1
        
        precuss = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(0,lcdt)))
        postcuss = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range((length-(len(precuss)+len(newcuss)))))

        self.render("base.html", precuss = precuss, cussword = newcuss, postcuss = postcuss)

app = webapp2.WSGIApplication([('/', MainPage),
                               ],
                              debug=DEBUG)
