Python notes
------------

Это заметки по python версии 2.7.9 (и немного про отличия от версии 3). 
В них написано не про стандартную библиотеку, а про основные механизмы языка. 
Сначала составлял для себя, но потом подумал, что если писать подробнее, то 
это может пригодиться не только мне. Поэтому здесь могут встречаться довольно 
очевидные фразы. 

Конечно, в этих заметках могут быть любые ошибки и неточности. Все файлы 
предоставляются "КАК ЕСТЬ" ("AS IS"), БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ.


Источники
---------

Читал в основном официальную документацию - The Python Tutorial и The Python 
Language Reference. Также помогли следующие статьи (спасибо их авторам):

- The Inside Story on New-Style Classes:
  http://python-history.blogspot.ru/2010/06/inside-story-on-new-style-classes.html

- The Python 2.3 Method Resolution Order:
  https://www.python.org/download/releases/2.3/mro

- Python’s super() considered super!:
  https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
 
- Things to Know About Python Super [2 of 3]:
  http://www.artima.com/weblogs/viewpost.jsp?thread=236278
  (про вызов super() с одним параметром - зачем это нужно и почему это плохо)

- The Python "with" Statement by Example:
  http://preshing.com/20110920/the-python-with-statement-by-example/

- PEP 3119 - Introducing Abstract Base Classes:
  https://www.python.org/dev/peps/pep-3119/

 
Возможный порядок чтения
------------------------

1. data, if_for_while
2. functions
3. variables
4. classes
5. exceptions
6. iterator, with
7. descriptor
8. property, slots, decorator
9. mro, super
10. metaclass, abc
11. modules/use_modules, modules/use_packages
12. encoding


Разное
------

Кодировка файлов utf-8 (без BOM). Строки, содержащие русские буквы, записаны 
в коде как u"строка", т.е. как юникод-строки. Подробнее об этом есть в 
заметках "data" и "encoding".

В тексте часто используются три связанных слова: экземпляр, класс и объект. 
Вообще, "экземпляр" и "объект" являются синонимами, но в заметках "объект" 
обычно означает "экземпляр или класс", т.к. в python любые данные, в том числе 
классы - это объекты.

Также используется слово "блок" ("блок кода"). Строго говоря, блоком в python 
называют только определенные части кода - про это есть в "variables". Однако 
в заметках под этим словом иногда понимаются инструкции вроде try, except, 
with и т.п. (хотя формально это не блоки).

Фразы "python 2.x/3.x" в заметках означают "какие-то из версий 2.x/3.x".

Артур
