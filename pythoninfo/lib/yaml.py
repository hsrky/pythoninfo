############################################################################
#
# Dump dict to yaml string
#
############################################################################
class yaml(object):
    
    @staticmethod
    def append_to_storage(tabIndex, data, storage, postfix=':'):
        tab = tabIndex * 2 * ' '
        if type(data) is dict:
            for d in data:
                data_value = data[d]
                data_type = type(data_value)
                if data_type is not dict:
                    data_value = str(data_value)
                    data_value = data_value.replace('<br/>', '').replace('\n', ';')
                    value = '- {} = {}'.format(d, data_value)
                    yaml.append_to_storage(tabIndex, value, storage, '')
                else:
                    yaml.append_to_storage(tabIndex, d, storage)
                    yaml.append_to_storage(tabIndex + 1, data_value, storage)
            return

        storage.append('{}{}{}'.format(tab, data, postfix))
        
    @staticmethod
    def dumps(dict_obj):
        storage = []
        for obj in dict_obj:
            yaml.append_to_storage(0, obj, storage)
            yaml.append_to_storage(1, dict_obj[obj], storage)
            
        return '\n'.join(storage)
