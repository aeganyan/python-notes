# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Copyright (c) 2015 Artur Eganyan
#
# This work is provided "AS IS", WITHOUT ANY WARRANTY, express or implied.
#-------------------------------------------------------------------------------

# Свойство - это атрибут с функциями чтения/записи/удаления:
#
# class SomeClass(object):
#   <свойство> = property(<функция чтения>, <записи>, <удаления>, <документация>)
#
# Функции чтения/записи/удаления принимают первым параметром ссылку на 
# экземпляр, к свойству которого обратились ("экземпляр.свойство"). Если 
# к свойству обратились через класс ("класс.свойство"), то эти функции не 
# будут вызываться. Однако, свойство должно быть создано в классе, а не в 
# экземпляре, потому что иначе оно, как и любой дескриптор, не будет 
# реагировать на обращения (см. пример).
#
# Замечание: На самом деле, свойство - это просто дескриптор, который можно 
# удобно создать функией property().

class A(object):

    def __init__(self):
        self.__x = 0

    def x_get(self):
        return self.__x

    def x_set(self, value):
        if value >= 0:
            self.__x = value

    def x_del(self):
        del self.__x

    x = property(x_get, x_set, x_del, u"Документация к свойству x")

a = A()
print a.x   # 0, вызовет a.x_get()
a.x = 10    # Вызовет a.x_set(10)
a.x = -10   # Вызовет a.x_set(-10)
print a.x   # 10
help(A)     # Выведет описание класса A, в том числе - документацию к x

# Если свойство создать как атрибут экземпляра, оно не будет работать
a.x2 = property(A.x_get)
print a.x2  # Вернет само свойство <property object at адрес>, а не результат x_get()

# Если свойство создать как атрибут класса, то все нормально
A.x3 = property(A.x_get) # A.x3 - то же самое, что A.x, но только для чтение
print a.x3  # 10
#a.x3 = 123 # AttributeError: can't set attribute
#del a.x3   # AttributeError: can't delete attribute

del a.x     # Вызовет a.x_del()
#print a.x  # AttributeError: 'A' object has no attribute '_A__x'


# Замечание: Свойство создать проще, чем вручную описывать аналогичный 
# дескриптор:
#
# class MyProperty(object):
#     def __get__(self, instance, owner):
#         <функция чтения>
#
#     def __set__(self, instance, value):
#         <функция записи>
#
#     def __delete__(self, instance):
#         <функция удаления>
# 
# class MyClass(object):
#    x = MyProperty()
