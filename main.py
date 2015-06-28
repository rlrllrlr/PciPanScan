#!/usr/bin/env python

# PciPanScan - Searches and replaces sensistive data such as credit card and social security numbers.

# Copyright 2015 Christopher Sfalanga

#  This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse, re

#cli parsing stuff
cli_parse = argparse.ArgumentParser(description="removes taboo info from given files");
cli_parse.add_argument("filename", help="path to input file");
cli_parse.add_argument("-o", dest="output_file", help="path to output file");
cli_parse.add_argument("-c", dest="repl_char", help="character to redact taboo strings");
cli_parse.add_argument("-v", dest="verbose", help="verbose ouput of censored file",
                       action="store_true");
cli_parse.add_argument("-hi", dest="highlight", action="store_true",
                       help="highlight newly-censored strings(implies -v)");
cli_parse.add_argument("-no", dest="no_output_file", action="store_true",
                       help="don't write output to any file");
parsed = cli_parse.parse_args();

#assign cli parsing to (relatively) local variables
input_file = parsed.filename;
output_file = parsed.output_file if parsed.output_file else input_file;
repl_char = parsed.repl_char if parsed.repl_char else 'X';
highlight = parsed.highlight;
verbose = True if highlight else parsed.verbose;
no_output_file = parsed.no_output_file;

#read the input file
try:
  with open(input_file, "r") as foo:
    content = foo.read();
except IOError as e:
  print("Error reading input file: "+e.strerror);
  quit();

#s&r the social and ccnum
pattern="[0-9]{3}-[0-9]{2}-[0-9]{4}";
ssrepl = lambda _: "xxx-xx-xxxx".replace('x', repl_char);
new_content = re.sub(pattern, ssrepl, content);

pattern="([345]{1}[0-9]{3}|6011){1}[ -]?[0-9]{4}[ -]?[0-9]{2}[-]?[0-9]{2}[ -]?[0-9]{1,4}";
ccrepl = lambda _: "xxxx-xxxx-xxxx-xxxx".replace('x', repl_char);
new_content = re.sub(pattern, ccrepl, new_content);

#write to output file
if not no_output_file:
  try:
    with open(output_file, "w") as foo:
      foo.write(new_content);
  except IOError as e:
    print("Error writing to output file: "+e.strerror);

#verbose, maybe
if verbose:
  if highlight:
    cchilit_repl = lambda mobj: "\033[1;31m"+mobj.group(0)+"\033[0m";
    new_content = re.sub("xxxx-xxxx-xxxx-xxxx".replace('x', repl_char),
                         cchilit_repl, new_content);
    sshilit_repl = lambda mobj: "\033[1;94m"+mobj.group(0)+"\033[0m";
    new_content = re.sub("xxx-xx-xxxx".replace('x', repl_char),
                         sshilit_repl, new_content);
  print(new_content);
