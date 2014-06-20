import traceback

class DbUtils(object):
    #FIXME change to plugin style and read query from custom config files
    db = None
    db_conn = None
    
    def __init__(self, db):
        self.db = db
    
    def __del__(self):
        # dtor
        if self.db_conn:
            self.db_conn.close()
        
    def connect(self):
        db = self.db
        protocol = db['protocol']
        if protocol.find('mysql') == -1:
            print('Do not support database other than mysql at the moment')
            return False
        
        dblib = None
        try:
            import MySQLdb as dblib
        except:
            pass
        
        if not dblib:
            print('No MySQL library installed for python')
            return False
        
        try:
            self.db_conn = dblib.connect(host=db['host'], port=int(db['port']), 
                                        user=db['username'], passwd=db['password'], 
                                         db=db['dbname'])
        except:
            print('Failed to open connection to db {} using user {}'.format(db['host'], db['username']))
            #print traceback.print_exc()
            return False
        
        return True
    
    def query(self, sql):
        if not self.db_conn:
            print('Can\'t query until connection is established.')
            return False
        
        try:
            cur = self.db_conn.cursor()
        except:
            print('Failed to create connection cursor.')
            #print traceback.print_exc()
            return False
        try:
            cur.execute(sql)
        except:
            cur.close()
            print('Failed to execute SQL command.')
            #print traceback.print_exc()
            return False
        
        cur.close()
        
        return True