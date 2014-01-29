# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 00:50:30 2013

@author: Preston
"""

import shlex

KEYWORD_TO_VARIABLE = {'say': 'phrase', 'play': 'card',
                       'player': 'player', 'notify': 'reason',
                       'punish': 'penalty'}


WHITE_LIST = set()
DEFAULT_VALUES = {'phrase': None, 'card': None, 'args': None,
                  'timeout': 0}
                    # {Variable name: value}
                    # I.E: {'failure_function': 'SERVER.punish'}

def get_base_code(script_line):
    """Finds the command in the line of script and returns the
    corresponding unformatted code"""
    base_mapping = {
            'Remove': '\n'.join((
                'if "{variable}" in WHITE_LIST:',
                '    del({variable})',
                'else:',
                '    {variable} = None',)),

            'Set': '\n'.join(('{variable} = {value}',)),

            'Replace': '\n'.join((
                '{variable1}, {variable2} = {variable2}, {variable1}',
                )),

            'Wait': '\n'.join((
                'rule = {rule}',
                'if {phrase}:',
                '    rule.say_queue.put(({phrase}, {player}))',
                'if {card}:',
                '    rule.play_queue.put(({card}, {player}))',
                'rule.say_queue.not_empty.wait({timeout}/2.0)',
                'rule.play_queue.not_empty.wait({timeout}/2.0)',
                'for queue in (rule.play_queue, rule.say_queue):',
                '    if queue.empty:',
                '        {failure_function}({player}, {penalty},',
                '                           reason = {reason})',
                '        while not queue.empty():',
                '            queue.get_nowait()',
                'Phrase, Card = {phrase}, {card}',)),

            'Call': '\n'.join((
            'for rule in {rulehandler}.rules:',
            '    if rule == {name}:',
            '        exec(rule.script)',))
                   }
    for word in get_script_values(script_line):
        if base_mapping.get(word):
            return base_mapping.get(word)

def format_code(line, **variable_values):
    """Takes an unformatted line of code and formats it with the given
    variable: value pairs. I.E: to set variable in the delete code to
    player,format_code(get_base_code('Remove'), variable =
    player_instance)."""
    return line.format(**variable_values)

def get_base_variables(base_line):
    """Returns a set of the variables for the base line from
    get_base_code. I.E: Returns set(['variable', 'value']) for
    {variable} = {{{value}: 5}} Note that double braces (which
    represents normal { and } respectively) are ignored"""
    variables = set()
    chunks = base_line.replace('{{', '').replace('}}', '')
    next_part = lambda chunk: chunk[-1].partition('}')
    for _ in xrange(chunks.count('{')):
        var, _, chunks = next_part(chunks.partition('{'))
        variables.add(var)
    return variables

def add_variable(variable):
    """Attempts to add the variable, value pair to the whitelist. If
    that variable is already used in the local name space, returns
    False. If the dictionary is successfully updated, then return True
    """
    if variable in globals().iterkeys() and variable not in WHITE_LIST:
        return False
    else:
        WHITE_LIST.add(variable)
        return True

def get_script_values(script_line):
    """Returns a list of the values present in order on the script line.
    I.E: Returns [Set, dog, 'cat'] for "Set dog to 'cat'".
    The delimiters that are removed are 'to', 'with', 'in' and 'and'"""
    delimiters = (' to ', ' with ', ' in ', ' and ', ' for ')
    values = ''.join(script_line)
    #Hexadecimal for space: \x20
    for delimiter in delimiters:
        values = values.replace(delimiter, ' ')
    return shlex.split(values, posix = False)
    #Otherwise, strings with spaces in them get cut off

def get_keyword_values(values):
    """Parses a list of values, like the one returned from
    get_script_values and returns a dictionary representing matching
    explicit keyword arguments. The KEYWORD_TO_VARIABLE dictionary is
    used to associate the script word to the variable. As an example:

    SCRIPT:     wait ... for player to say 'Hello World!'
    VALUE LIST: [..., player, say, 'Hello World!']
    say is a special script word for the 'phrase' variable, so this
    would return {'phrase': 'Hello World!'}"""
    keyword_args = {}
    for value in values:
        if KEYWORD_TO_VARIABLE.get(value):
            keyword_args.update({KEYWORD_TO_VARIABLE.get(value):
                         values.pop(values.index(value) + 1)})
    return keyword_args

def compile_code(code):
    """Returns a compiled version of the code"""
    return compile(code, __name__, 'exec')

def codify(rule):
    """Converts the high-level script from the rule into Python code.
    Returns a compiled version of the code to be ran by eval"""
    code = ''
    script = rule.script
    for line_num, line in enumerate(script.split('\n')):
        if line.endswith(':'):
            code += line + '\n'
            continue
        line_num += 1
        values = get_script_values(line)[1:]
        base = get_base_code(line)
        if not base:
            raise SyntaxError, (
            "Couldn't find a command on line {}".format(line_num))
        variables = get_base_variables(base)
        for value in values:
            if not add_variable(value):
                raise SyntaxError, ' '.join((
                "On line {},".format(line_num),
                "{} cannot be used, choose a different variable".format(
                value)))
        args = DEFAULT_VALUES.copy()
        args.update(dict(zip(variables, values)))
        args.update(get_keyword_values(values))
        args.update({'say_queue': 'rule.say_queue',
                     'play_queue': 'rule.play_queue'})
        assert len(variables) <= len(args),(" ".join((
            "On line {},".format(line_num),
            "received {} parametres, but need {}\n".format(
            len(args), len(variables)),
            "Given: {}\n".format(args.keys()),
            "Still Need:  {}\n".format(list(set(variables).difference(
                                       set(args.keys())))))))
        indent = 0
        for letter in line:
            if letter.isspace():
                indent += 1
            else:
                break
        base = base.replace('\n', '\n' + ' ' * indent)
        code += ' ' * indent + (
            format_code(base, **args) + '\n')
    return compile_code(code)

if __name__ == '__main__':
    import Rule
    dog, cat = None, None
    # Note the Variable names, not the variables themselves
    WHITE_LIST.add('dog')
    WHITE_LIST.add('cat')
    TEST = codify(Rule.Rule('No Name', None, '\n'.join((
                 "if True:",
                 "    Set dog to 'bark!'",
                 "    if not dog:",
                 "        Remove dog",
                 "    elif dog == 'bark!':",
                 "        Set cat to 'Meow!'",
                 "    Replace cat and dog",
                 ))))
    exec(TEST)
    print "dog = {}, cat = {}".format(dog, cat)
    print 'Basic test complete, starting parser-thing'
    print
    print
    def interpreter():
        "Runs the script interpreter, returns a compiled code object"
        print 'Working Commands: '
        print '\n'.join(('Remove', 'Set', 'Replace', ))
        script = []
        while 1:
            line = raw_input('>')
            if line:
                script.append(line)
            else:
                break
        if script:
            return codify(Rule.Rule('CLI script', None,
                          '\n'.join(script)))
        else:
            return '""'
    eval(interpreter())
    print "Compiled and executed!"
