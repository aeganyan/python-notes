# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Copyright (c) 2015 Artur Eganyan
#
# This work is provided "AS IS", WITHOUT ANY WARRANTY, express or implied.
#-------------------------------------------------------------------------------

# Abstract Base Classes (ABC) - виртуальные родительские классы (или, иначе 
# говоря, интерфейсы). В ABC определяется набор методов (интерфейс). И далее 
# любые классы, у которых есть все эти методы, можно зарегистрировать как 
# потомков ABC. Для них ABC будет считаться родителем, но реально не будет им 
# являться. Т.е. isinstance(экземпляр, ABC) и issubclass(класс, ABC) будут 
# возвращать True, но ABC не будет находится в иерархии наследования. ABC - 
# это любой класс, метаклассом которого является ABCMeta.

import abc

class SomeInterface(object):
    __metaclass__ = abc.ABCMeta # Теперь класс SomeInterface станет ABC
    
    def f(self):
        u""" Метод f() должен делать такое-то действие """
    
    def g(self):
        u""" Метод g() должен делать другое действие """

class A(object):
    def f(self):
        print "A.f()"

    def g(self):
        print "A.g()"

SomeInterface.register(A)  # Теперь SomeInterface считается виртуальным
                           # родителем A. Другими словами, A считается
                           # реализующим интерфейс SomeInterface.

a = A()
print isinstance(a, SomeInterface) # True
print issubclass(A, SomeInterface) # True

# При этом нет никаких гарантий, что класс A действительно реализует методы 
# интерфейса. В python многое основано на принципе "gentlemen's agreement" - 
# разработчик, вызывающий ABC.register(класс), должен сам позаботиться, чтобы 
# его класс реализовывал данный интерфейс.

class B(object):
    def f(self):
        print "B.f()"
    # А вот g() тут нет

SomeInterface.register(B)

b = B()
print isinstance(b, SomeInterface) # True
print issubclass(B, SomeInterface) # True

# Однако, если от ABC действительно наследовать класс, и пометить методы ABC 
# декоратором @abstractmethod, то при создании такого класса будет проверено, 
# все ли абстрактные методы переопределены. Если не все, то при создании 
# экземпляра класса сгенерируется исключение TypeError.

class SomeInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod    
    def f(self):
        print "SomeInterface.f()"

    @abc.abstractmethod
    def g(self):
        print "SomeInterface.g()"

class A(SomeInterface):
    def f(self):
        print "A.f()"
# Здесь будет создан класс A через ABCMeta.__new__(). В __new__ будут проверены 
# методы A и его родителей, и определено, что g() остался абстрактным.

#A()              # TypeError: Can't instantiate abstract class A with
                  # abstract methods g
#SomeInterface()  # Аналогичная ошибка для SomeInterface - у него все
                  # методы абстрактные

# Конечно, при реальном наследовании от ABC, он уже не будет "абстрактным
# родительским классом", и дочерние классы не понадобится регистрировать
# через ABC.register().

print issubclass(A, SomeInterface) # True, т.к. это просто родительский класс

# Абстрактные методы ABC можно вызывать из дочерних классов через super()
# или напрямую. Т.е. их "абстрактность" влияет только на создание экземпляров 
# класса. Также, помимо абстрактных методов могут быть абстрактные свойства, 
# созданные декоратором @abstractproperty.

class B(SomeInterface):
    def f(self):
        super(B, self).f()    # Абстрактный метод вызывается через super

    def g(self):
        SomeInterface.g(self) # Абстрактный метод вызывается напрямую

b = B()
b.f()   # SomeInterface.f()
b.g()   # SomeInterface.g()

# Абстрактные методы можно создавать только в описании класса. Если добавить 
# абстрактный метод позже, он не будет учтен, потому что список абстрактных 
# методов составляется при создании класса.

SomeInterface.h = abc.abstractmethod(lambda: 123)

class C(B):
    pass

c = C()  # Никакой ошибки, т.к. все абстрактные методы класса
         # SomeInterface были обнаружены в момент его создания.
         # Хотя h фактически является абстрактным.

# Функции isinstance(экземпляр, класс) и issubclass(подкласс, класс) вызывают 
# методы класс.__instancecheck__(экземпляр) и класс.__subclasscheck__(подкласс). 
# Для ABCMeta эти методы проверяют классы, зарегистрированные через 
# ABCMeta.register(). При необходимости можно переопределить эти методы, но 
# удобнее переопределить ABCMeta.__subclasshook__(подкласс). Он вызывается из 
# __subclasscheck__() и должен возвращать или True, или False, или 
# NotImplemented (в последнем случае проверка будет делаться как обычно).

class SomethingWithLength(object):
    __metaclass__ = abc.ABCMeta

    # __subclasshook__ должен быть методом класса (classmethod)
    @classmethod
    def __subclasshook__(cls, subclass):
        if hasattr(subclass, "__len__"):
            return True
        return NotImplemented

print isinstance([], SomethingWithLength) # True, т.к. список имеет метод __len__

# Замечание: ABC не может наследовать от type. Не видел, чтобы об этом было 
# сказано в документации, но если ABC наследует от type, то в методе 
# ABCMeta.__subclasscheck__() произойдет ошибка при вызове ABC.__subclasses__(). 
# Потому что тогда ABC.__subclasses__() - это type.__subclasses__(), а этому 
# методу надо явно передавать класс, для которого он вернет список подклассов. 
# ABCMeta ничего не передает. А вот object.__subclasses__() не требует 
# передавать класс, поэтому если ABC наследует от object, все нормально.

class WrongABC(type):
    __metaclass__ = abc.ABCMeta

# TypeError: __subclasscheck__() takes exactly one argument (0 given)
#print isinstance(123, WrongABC)

# Та же самая ошибка:
# TypeError: descriptor '__subclasses__' of 'type' object needs an argument
#print type.__subclasses__()

# А для object этой ошибки уже нет
#print object.__subclasses__() # Выведет список все потомков object

# Замечание: По сути, ABC - это среднее между настоящими интерфейсами и 
# duck typing.
#
# Настоящие интерфейсы - это родительские классы, методы которых не 
# реализованы. От интерфейсов нужно наследовать, и затем переопределять
# методы в дочернем классе. Принадлежность класса к конкретному интерфейсу
# определяется по факту наследования - на этапе компиляции, статически.
# В python такого нет.
#
# Duck typing - это определение интерфейса класса по наличию у него
# нужных методов: "если что-то выглядит, крякает и плавает как утка,
# то наверное это утка". Например, если у класса есть методы "__len__"
# и "__getitem__", то, возможно, это последовательность. В данном
# случае интерфейс определяется на этапе выполнения, динамически.
#
# ABC - это не такой строгий вариант, как настоящие интерфейсы, но более 
# строгий, чем duck typing. Абстрактный класс содержит не только набор методов, 
# но обычно и их описание - что именно они должны делать. Кроме того, класс 
# считается реализующим этот интерфейс, если он явно зарегистрирован через 
# ABC.register(класс), в то время как duck typing рассчитывает на проверки 
# вроде if hasattr(класс, "метод"). А при прямом наследовании и использовании 
# @abstractmethod ABC ведет себя почти как обычный интерфейс.
#
# Замечание: В отличие от виртуальных классов C++ и от интерфейсов в других 
# языках, ABC могут и не быть реальными родительскими классами.
