class MJValidationError(object):

    def __init__(self, index, cid, etype, field,message):
        self.index = index
        self.id = cid
        self.etype = etype
        self.field = field
        self.message = message

    def __repr__(self):
        return f" index:{self.index}  id:{self.id}  type:{self.etype}  field:{self.field}  message:{self.message}"
    
    # def __getattribute__(self, name):
    #     object.__getattribute__(self, name)

    # @property
    # def index(self):
    #     return self.__index

    # @index.setter
    # def index(self, val):
    #     self.__index = val
        

# class MJValidationErrors(list):
    
#     def __getitem__(self, key):
#         return list.__getitem__(self, key-1)
