# -*- coding: utf-8 -*-
# flavio@casacurta.com
import re
patern = re.compile('([^\d]+)')
UNMASK = lambda num: re.sub(patern, '', num or '')


'''
db.define_table('mytable'
               , Field('CCPF', 'decimal(11,0)')
               , Field('CCNPJ', 'decimal(14,0)')
               , Field('SALARIO', 'decimal(7,2)')
               , Field('CBARRA1', 'decimal(12,0)'))

mytable = db['mytable']

mytable.id.writable = False
mytable.CCPF.label = 'CPF'
mytable.CCPF.writable = True
mytable.CCPF.requires = [IS_NOT_EMPTY(), IS_CPF()]
mytable.CCPF.represent = lambda value, row: MASK_CPF()(value)
mytable.CCNPJ.label = 'CNPJ'
mytable.CCNPJ.writable = True
mytable.CCNPJ.requires = [IS_NOT_EMPTY(), IS_CNPJ()]
mytable.CCNPJ.represent = lambda value, row: MASK_CNPJ()(value)
mytable.SALARIO.label = 'Salário'
mytable.SALARIO.writable = True
mytable.SALARIO.requires = [IS_NOT_EMPTY(), IS_DECIMAL(0,99999.99, dot=',')]
mytable.SALARIO.represent = lambda value, row: MASK_DECIMAL(dot=',')(value, 2)
mytable.CBARRA1.label = 'Código de Barra'
mytable.CBARRA1.writable = True
mytable.CBARRA1.requires = [IS_NOT_EMPTY(), IS_MODULO_10(mask='-')]
mytable.CBARRA1.represent = lambda value, row: MASK_DV(mask='-')(value)

'''

class MASK_DECIMAL(object):
    """
    Edit the a value mask

    If "Decimal point is comma" was defined, comma separator is dot

    example::

        db.mytable.mycolumn.represent = lambda value, row: MASK_DECIMAL()(value, 0)

        >>> MASK_DECIMAL()('.12', 2)
        '0.12'
        >>> MASK_DECIMAL(dot=',')(',12', 2)
        '0,12'
        >>> MASK_DECIMAL()('12345.67', 3)
        '12,345.670'
        >>> MASK_DECIMAL(dot=',')('1234,567', 3)
        '1.234,567'
    """

    def __init__(self, dot='.'):
         self.dot = dot
         self.comma = ',' if dot == '.' else '.'


    def __call__(self, value, dec=0):
        value = str(value)
        sign = ''
        if float(value.replace(',','.')) < 0:
            sign = '-'
            value = value[1:]
        if dec:
            pdot = value.find(self.dot) + 1
            z = dec - (len(value) - (pdot)) if pdot else dec
            value = value + ('0' * z)
        value = value.replace(".", "").replace(",", "")
        if len(value) == dec:
            value = '0' + value
        q_int = len(value)-dec
        r = q_int % 3
        mask = eval("'{}{}{}{}'.format('{}' * r if r else ''\
                                     ,self.comma if q_int > 3 and r else ''\
                                     ,(('{}{}{}' + self.comma) * (q_int/3))[:-1]\
                                     ,self.dot + '{}' * dec if dec else '')").format(*value)

        return sign + mask


class MASK_MONEY(object):
    """
    Edit the a value money mask
db.define_table('mytable'
               , Field('CCPF', 'decimal(11,0)')
               , Field('CCNPJ', 'decimal(14,0)')
               , Field('SALARIO', 'decimal(7,2)')
               , Field('CBARRA1', 'decimal(12,0)'))

mytable = db['mytable']

mytable.id.writable = False
mytable.CCPF.label = 'CPF'
mytable.CCPF.writable = True
mytable.CCPF.requires = [IS_NOT_EMPTY(), IS_CPF()]
mytable.CCPF.represent = lambda value, row: MASK_CPF()(value)
mytable.CCNPJ.label = 'CNPJ'
mytable.CCNPJ.writable = True
mytable.CCNPJ.requires = [IS_NOT_EMPTY(), IS_CNPJ()]
mytable.CCNPJ.represent = lambda value, row: MASK_CNPJ()(value)
mytable.SALARIO.label = 'Salário'
mytable.SALARIO.writable = True
mytable.SALARIO.requires = [IS_NOT_EMPTY(), IS_DECIMAL(0,99999.99, dot=',')]
mytable.SALARIO.represent = lambda value, row: MASK_DECIMAL(dot=',')(value, 2)
mytable.CBARRA1.label = 'Código de Barra'
mytable.CBARRA1.writable = True
mytable.CBARRA1.requires = [IS_NOT_EMPTY(), IS_MODULO_10(mask='-')]
mytable.CBARRA1.represent = lambda value, row: MASK_DV(mask='-')(value)

SDS
    example::

        db.mytable.mycolumn.represent = lambda value, row: MASK_MONEY(symbol='R$')(value, 0)

        >>> MASK_MONEY()('.12', 2)
        'R$ 0,12'
        >>> MASK_MONEY(dot='.', symbol='$')(',12', 2)
        '$ 0.12'
        >>> MASK_MONEY()('12345.67', 3)
        'R$ 12.345,670'
        >>> MASK_MONEY(dot='.', symbol='R$')('1234,567', 3)
        'R$ 1.234,567'
        >>> MASK_MONEY(LC_ALL='usa')('1234567', 2)
        '$ 1,234,567.00'
    """

    def __init__(self, LC_ALL='', dot='', symbol=''):
        import locale

        locale.setlocale(locale.LC_ALL, LC_ALL)
        if not dot:
            self.dot = locale.localeconv()['decimal_point']
        else:
            self.dot = dot
        if not symbol:
            self.symbol = locale.localeconv()['currency_symbol']
        else:
            self.symbol = symbol

    def __call__(self, value, dec=0):
        rep =  ',' if self.dot == '.' else '.'
        value = str(value).replace(rep, self.dot).replace(self.symbol, '')
        return '{} {}'.format(self.symbol, MASK_DECIMAL(dot=self.dot)(value, dec))


class MASK_CPF(object):
    """
    Edit the a CPF code mask

    example::

        db.mytable.mycolumn.represent = lambda value, row: MASK_CPF()(value)

        >>> MASK_CPF()('12345678909')
        '123.456.789-09'
        >>> MASK_CPF()('123456797')
        '001.234.567-97'

    """
    def __init__(self):
        pass

    def __call__(self, cpf):
        if not isinstance(cpf,(list, str)):
           cpf=str(cpf)
        if isinstance(cpf, str):
           cpf = UNMASK(cpf)
           cpf = '0' * (11 - len(cpf)) + cpf
        return '{}{}{}.{}{}{}.{}{}{}-{}{}'.format(*cpf)


class MASK_CNPJ(object):
    """
    Edit the a CNPJ code mask

    example::

        db.mytable.mycolumn.represent = lambda value, row: MASK_CNPJ()(value)

        >>> MASK_CNPJ()('12345678000195')
        '12.345.678/0001-95'
        >>> MASK_CNPJ()('123456000149')
        '00.123.456/0001-49'
    """
    def __init__(self):
        pass

    def __call__(self, cnpj):
        if not isinstance(cnpj,(list, str)):
           cnpj=str(cnpj)
        if isinstance(cnpj, str):
           cnpj = UNMASK(cnpj)
           cnpj = '0' * (14 - len(cnpj)) + cnpj
        return '{}{}.{}{}{}.{}{}{}/{}{}{}{}-{}{}'.format(*cnpj)


class MASK_DV(object):
    """
    Edit the a digit checker

    example::

        db.mytable.mycolumn.represent = lambda value, row: MASK_DV('/')(value)

        >>> MASK_DV('-')('12345678000195')
        '1234567800019-5'
    """
    def __init__(self, mask=''):
        self.mask = mask

    def __call__(self, value):
        if not isinstance(value,(list, str)):
           value=str(value)
        if isinstance(value, str):
           value = UNMASK(value)
        return '{}{}{}'.format(value[:-1], self.mask, value[-1])
