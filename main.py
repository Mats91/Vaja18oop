#!/usr/bin/env python
import os
import random

import jinja2
import logging
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):

    country_capital_dict = {"Slovenia": "Ljubljana", "Croatia": "Zagreb", "Austria": "Vienna"}

    def get(self):
        random_num = random.randint(0, 2)  # vrne intiger med 0 in 2
        selected_country = self.country_capital_dict.keys()[random_num]  # bo zbral vedno slovenijo ce je 0
        return self.render_template("hello.html", params={'state': selected_country})

    def post(self):

        guess = self.request.get('guess')

        correct = self.check_guess(guess, self.request.get('state'), self.country_capital_dict)

        if correct:
            self.write('Pravilno')
        else:
            self.write('Narobe')

    def check_guess(self, user_guess, country, cc_dict):

        capital = cc_dict[country]

        if user_guess.lower() == capital.lower():  # da prime majhne crke
            print "Correct"
            return True
        else:
            print "False"
            return False

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
