import pymysql

class Api(object) :
    def __init__(self, logger):
        try :
            self.logger = logger
            self.conn = pymysql.connect(
                user='root',
                password='1234',
                host='localhost',
                port=3306,
                database='recycle_monitoring',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            self.logger.error(f'API Load Error : {e}')
        
    def select_all(self, query):
        try :
            self.cur.execute(query)
            result = self.cur.fetchall()
            self.logger.info('DB Select Success')
            return result
        except Exception as e:
            self.logger.error(f'DB Select Error : {e} \n {query}')
            return
        
    def select(self, query):
        try :
            self.cur.execute(query)
            result = self.cur.fetchone()
            self.logger.info('DB Select Success')
            return result
        except Exception as e:
            self.logger.error(f'DB Select Error : {e} \n {query}')
            return
        
    def update(self, query):
        try :
            self.cur.execute(query)
            self.conn.commit()
            self.logger.info('DB Update Success')
            return
        except Exception as e:
            self.logger.error(f'DB Update Error : {e} \n {query}')
            return 
        
    def insert(self, query):
        try :
            self.cur.execute(query)
            self.conn.commit()
            self.logger.info('DB Insert Success')
            return
        except Exception as e:
            self.logger.error(f'DB Insert Error : {e} \n {query}')
            return
        
    def delete(self, query):
        try :
            self.cur.execute(query)
            self.conn.commit()
            self.logger.info('DB Delete Success')
            return
        except Exception as e:
            self.logger.error(f'DB Delete Error : {e} \n {query}')
            return