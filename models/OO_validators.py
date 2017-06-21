# -*- coding: utf-8 -*-

def advanced_editor(field, value):
    return TEXTAREA(_id=str(field).replace('.', '_'),
                    _name=field.name, _class='text ckeditor', value=value, _cols=80, _rows=10)


def to_decimal(value):
    value = value.replace('R$', '')
    without_dot = value.replace('.', '')
    decimal = without_dot.replace(',', '.')
    return decimal


class IS_CPF_OR_CNPJ(object):
    def __init__(self, format=True, error_message='Digite apenas os números!'):
        self.format = format
        self.error_message = error_message

    def __call__(self, value):
        try:
            #return (value, 'cpf incorreto'+str(value))
            #return (value, 'cpf incorreto'+str(cl))
            c = []
            for d in value:
                if d.isdigit():
                    c.append(d)
            cl = str(''.join(c))
            #return (value, 'cpf incorreto'+str(cl))
            if len(cl) == 11:
                cpf = cl
                cnpj = None
            elif len(cl) == 14:
                cpf = None
                cnpj = cl
            else:
                return (value, 'Número de dígitos incorreto para CPF ou CNPJ')

            #return(cpf,'aquiok'+str(len(cpf)==11))
            if cpf:

                def valida(value):

                    def calcdv(numb):
                        result = int()
                        seq = reversed(((range(9, id_type[1], -1) * 2)[:len(numb)]))
                        #return (value,'to fundo1')
                        for digit, base in zip(numb, seq):
                            result += int(digit) * int(base)

                        dv = result % 11
                        #return (value,'to fundo1'+str(dv))
                        return (dv - 10) and dv or 0

                    id_type = ['CPF', -1]

                    numb, xdv = value[:-2], value[-2:]

                    dv1 = calcdv(numb)
                    #return (value,'entrei'+str(dv1))
                    dv2 = calcdv(numb + str(dv1))
                    return (('%d%d' % (dv1, dv2) == xdv and True or False), id_type[0])


                try:
                    cpf = str(value)
                    #return(cpf,'aquiok'+str(len(cpf)==11))
                    if len(cpf) >= 11:

                        #return (value, 'cpf acima de 11')
                        c = []
                        for d in cpf:
                            if d.isdigit():
                                c.append(d)
                        cl = str(''.join(c))
                        #return (value, 'cpf incorreto'+str(cl))
                        if len(cl) == 11:
                            if valida(cl)[0] == True:
                                return (value, None)
                            else:
                                return (value, 'cpf inválido')
                        elif len(cl) < 11:
                            return (value, 'cpf incompleto')
                        else:
                            return (value, 'cpf tem mais de 11 dígitos')
                        if cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
                            return (value, 'cpf deve estar no formato 000.000.000-00' + cpf[11])
                    else:
                        return (value, 'cpf deve estar no formato 000.000.000-00')
                        #return(cpf,'aquiok'+str(len(cpf)==11))
                except:
                    return (value, 'algum erro' + str(value))
            elif cnpj:

                """ Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam """
                inteiros = map(int, cnpj)
                novoCnpj = inteiros[:12]

                prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
                while len(novoCnpj) < 14:
                    r = sum([x * y for (x, y) in zip(novoCnpj, prod)]) % 11
                    if r > 1:
                        f = 11 - r
                    else:
                        f = 0
                    novoCnpj.append(f)
                    prod.insert(0, 6)
                    #return(str(novoCnpj),'aquiok')
                """ Se o número gerado coincidir com o número original, é válido """
                if novoCnpj == inteiros:
                    #cnpj = ''.join(novoCnpj)

                    return (str(cnpj), None)

                else:
                    return (value, 'CNPJ não é válido')



        except:
            return (value, 'algum erro' + str(value))

    def formatter(self, value):
        if len(value) == 11:
            formatado = value[0:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:11]
        elif len(value) == 14:
            formatado = value[0:2] + '.' + value[2:5] + '.' + value[5:8] + '/' + value[8:12] + '-' + value[12:14]
        else:
            formatado = value
        return formatado


class IS_CNPJ(object):
    def __init__(self, format=True, error_message='Digite apenas os números!'):
        self.format = format
        self.error_message = error_message

    def __call__(self, value):
        try:
            #return (value, 'cpf incorreto'+str(value))
            #return (value, 'cpf incorreto'+str(cl))
            c = []
            for d in value:
                if d.isdigit():
                    c.append(d)
            cl = str(''.join(c))
            #return (value, 'cpf incorreto'+str(cl))
            if len(cl) == 14:
                cnpj = cl
            else:
                return (value, 'Número de dígitos incorreto para CNPJ')

            if cnpj:

                """ Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam """
                inteiros = map(int, cnpj)
                novoCnpj = inteiros[:12]

                prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
                while len(novoCnpj) < 14:
                    r = sum([x * y for (x, y) in zip(novoCnpj, prod)]) % 11
                    if r > 1:
                        f = 11 - r
                    else:
                        f = 0
                    novoCnpj.append(f)
                    prod.insert(0, 6)
                    #return(str(novoCnpj),'aquiok')
                """ Se o número gerado coincidir com o número original, é válido """
                if novoCnpj == inteiros:
                    #cnpj = ''.join(novoCnpj)

                    return (str(cnpj), None)

                else:
                    return (value, 'CNPJ não é válido')



        except:
            return (value, 'algum erro' + str(value))

    # def formatter(self, value):
    #     formatado = value[0:2] + '.' + value[2:5] + '.' + value[5:8] + '/ ' + value[8:12] + '-' + value[12:14]
    #     return formatado


class IS_CEP(object):
    def __init__(self, format=True, error_message='Digite apenas os números!'):
        self.format = format
        self.error_message = error_message

    def __call__(self, value):
        try:
            #return (value, 'cpf incorreto'+str(value))
            #return (value, 'cpf incorreto'+str(cl))
            c = []
            for d in value:
                if d.isdigit():
                    c.append(d)
            cl = str(''.join(c))
            #return (value, 'cpf incorreto'+str(cl))
            if len(cl) == 8:
                cep = cl
                return (str(cep), None)
            else:
                return (value, 'Número de dígitos incorreto para CEP')



        except:
            return (value, 'algum erro' + str(value))

    def formatter(self, value):
        formatado = value[0:2] + '.' + value[2:5] + '-' + value[5:8]
        return formatado


class IS_TELEFONE(object):
    def __init__(self, format=True, error_message='Digite apenas os números!'):
        self.format = format
        self.error_message = error_message

    def __call__(self, value):
        try:
            telefone = str(value)
            #return(cpf,'aquiok'+str(len(cpf)==11))
            if len(telefone) >= 11:
                #return (value, 'cpf acima de 11')
                c = []
                for d in telefone:
                    if d.isdigit():
                        c.append(d)
                cl = str(''.join(c))
                #return (value, 'cpf incorreto'+str(cl))
                if len(cl) == 11:
                    return (str(cl), None)
                elif len(cl) < 11:
                    return (value, 'telefone incompleto')
                else:
                    return (value, 'o telefone tem mais de 11 dígitos')
            else:
                return (value, 'O telefone deve estar no formato 00-0000-0000')
                #return(cpf,'aquiok'+str(len(cpf)==11))
        except:
            return (value, 'algum erro' + str(value))

    def formatter(self, value):
        value = str(value)
        formatado = '(' +  value[0:2] + ')' + ' ' + value[2:7] + '-' + value[7:11]
        return formatado


def to_telefone(value):
    if value and len(value) == 10:
        formatado = '(' + value[0:2] + ')' + value[2:6] + '-' + value[6:10]
    else:
        formatado = value
    return formatado


class IS_CPF(object):
    def __init__(self, format=True, error_message='Digite apenas os números!'):
        self.format = format
        self.error_message = error_message

    def __call__(self, value):

        def valida(value):

            def calcdv(numb):
                result = int()
                seq = reversed(((range(9, id_type[1], -1) * 2)[:len(numb)]))
                #return (value,'to fundo1')
                for digit, base in zip(numb, seq):
                    result += int(digit) * int(base)

                dv = result % 11
                #return (value,'to fundo1'+str(dv))
                return (dv - 10) and dv or 0

            id_type = ['CPF', -1]

            numb, xdv = value[:-2], value[-2:]

            dv1 = calcdv(numb)
            #return (value,'entrei'+str(dv1))
            dv2 = calcdv(numb + str(dv1))
            return (('%d%d' % (dv1, dv2) == xdv and True or False), id_type[0])


        try:
            cpf = str(value)
            #return(cpf,'aquiok'+str(len(cpf)==11))
            if len(cpf) >= 11:

                #return (value, 'cpf acima de 11')
                c = []
                for d in cpf:
                    if d.isdigit():
                        c.append(d)
                cl = str(''.join(c))
                #return (value, 'cpf incorreto'+str(cl))
                if len(cl) == 11:
                    if valida(cl)[0] == True:
                        return (cl, None)
                    else:
                        return (cl, 'cpf inválido')
                elif len(cl) < 11:
                    return (cl, 'cpf incompleto')
                else:
                    return (cl, 'cpf tem mais de 11 dígitos')
            else:
                return (value, 'cpf deve estar no formato 000.000.000-00')
                #return(cpf,'aquiok'+str(len(cpf)==11))


        except:
            return (value, 'algum erro' + str(value))

    def formatter(self, value):
        #if value ==11:
        formatado = value[0:3] + '.' + value[3:6] + '.' + value[6:9] + '-' + value[9:11]
        #else:
        #    formatado=value
        #formatado = value
        return formatado

class IS_MONEY(object):

    """
    Checks if field's value is a valid decimal money

    Examples::

        INPUT(_type='text', _name='name', requires=IS_MONEY())

        >>> IS_MONEY(0, 999.99, dot=',', symbol='R$')('R$ 123,45')
        (Decimal('123.45'), None)
        >>> IS_MONEY()('$ 123.45')
        (Decimal('123.45'), None)

    """

    def __init__(self, minimum=None
                     , maximum=None
                     , error_message=None
                     , dot='.'
                     , symbol='$'):

         self.minimum = minimum
         self.maximum = maximum
         self.error_message=error_message
         self.dot = dot
         self.symbol = symbol

    def __call__(self, money):

        value = str(money).replace(self.symbol, '').strip()
        return IS_DECIMAL(minimum=self.minimum
                         ,maximum=self.maximum
                         ,error_message=self.error_message
                         ,dot=self.dot)(value)

class IS_TAG(object):
    def __init__(self, format=True, error_message='Digite a tag'):
        self.format = format
        self.error_message = error_message

    def __call__(self, value):
        tag = str(value)
        if len(tag) < 1:
            return (tag, 'Algo de errado com esse campo')

        tag = tag.replace('-', '')
        tag = tag.replace('.', '')
        tag = tag.replace(',', '')
        tag = tag.replace(';', '')
        tag = tag.replace(':', '')
        tag = tag.replace('>', '')
        tag = tag.replace('<', '')
        tag = tag.replace('/', '')
        tag = tag.replace(' ', '')
        tag = tag.upper()
        try:
            return (tag, None)
        except:
            return (tag, str(tag) + 'Não é uma tag valida' )


class E_DINHEIRO(object):
    def __init__(self, format=True, error_message='Digite o valor!'):
        self.format = format
        self.error_message = error_message

    def __call__(self, value):

        d = str(value)
        if len(d) < 1:
            return (d, 'É obrigatório o preenchimento deste campo')
        d = d.replace('R$', '')
        d = d.replace('.', '')
        d = d.replace(',', '.')
        #return (value, valor[-3:-2])
        try:
            return (d, None)
        except:
            return (d, str(d) + 'o valor digitado não é um número válido')

    def formatter(self, value):
        if value < 0:
            value = 0
        import locale

	try:
		# Works on Linux Serve
		locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
		value = locale.currency(value, grouping=True)
		return value
	except:
		# Works on Windows Server
		locale.setlocale(locale.LC_ALL, 'ptb')
		value = locale.currency(value, grouping=True)
		return value

def to_money(value):
    if value < 0:
        value = 0
    import locale

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    value = locale.currency(value, grouping=True)
    return value


def money(value):
    d = str(value)
    d = d.split('.')
    try:
        centavos = d[1][0:2]
    except:
        centavos = '00'
    if len(centavos) == 1:
        centavos = centavos + '0'

    inteiros = d[0]
    l = len(inteiros)
    i = 0
    if l > 3:
        r = l % 3
        reais = inteiros[0:r]
        while (i + 1) < (l - r):
            s = r + i
            if len(reais) > 0:
                reais = reais + '.' + inteiros[s:s + 3]
            else:
                reais = inteiros[s:s + 3]
            i = i + 3
    elif l > 0:
        reais = inteiros
    else:
        reais = 0
    return 'R$ %s,%s' % (reais, centavos)


def valor(value):
    d = str(value)
    d = d.split('.')
    try:
        centavos = d[1][0:2]
    except:
        centavos = '00'
    if len(centavos) == 1:
        centavos = centavos + '0'

    inteiros = d[0]
    l = len(inteiros)
    i = 0
    if l > 3:
        r = l % 3
        reais = inteiros[0:r]
        while (i + 1) < (l - r):
            s = r + i
            if len(reais) > 0:
                reais = reais + '.' + inteiros[s:s + 3]
            else:
                reais = inteiros[s:s + 3]
            i = i + 3
    elif l > 0:
        reais = inteiros
    else:
        reais = 0
    return '%s,%s' % (reais, centavos)


class VALOR_PAGO(object):
    def __init__(self, format=True, error_message=''):
        #self.format = format
        self.error_message = error_message

    def __call__(self, value):
        return (0, None)

    def formatter(self, value):
        #return value
        soma = db.pagamento_realizado.valor_total.sum()
        pago = db(db.pagamento_realizado.convenio_id == self.convenio.id
        ).select(soma).first()[soma]
        if not pago:
            pago = 0
        return to_money(pago)


#db.convenio.virtualfields.append(ConveniosVirtualFields())


def lt(s):
    try:
        s = unicode(s, 'utf-8').encode('latin-1')
    except:
        s = str(s)
    return s


def tl(s):
    try:
        data = s
        udata = data.decode("utf-8")
        return udata.encode("latin-1", "ignore")
    except:
        return ''


def make_time(value):
    if value:
        return value[6:10] + '-' + value[3:5] + '-' + value[0:2]
    else:
        return None


data = IS_NULL_OR(IS_DATE(format=T('%d-%m-%Y')))


def make_data(field):
    if type(field) is datetime.date:
        return field.strftime("%d/%m/%Y")
    else:
        return ''


def make_year(field):
    if type(field) is datetime.date:
        return field.strftime("%Y")
    else:
        return ''
