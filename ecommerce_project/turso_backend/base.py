from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper
import libsql_client

class TursoCursor:
    def __init__(self, client):
        self.client = client
        self.arraysize = 1
        self.description = None
        self.rowcount = -1
        self.rows = []
        self.row_idx = 0
        self.lastrowid = None

    def execute(self, sql, params=None):
        if params is None:
            params = []
        
        # Django uses %s, libsql uses ? or :name
        # We need to convert %s to ?
        # This is a naive replacement, might break if %s is in string
        # But for now it's better than nothing
        sql = sql.replace('%s', '?')
        
        try:
            rs = self.client.execute(sql, params)
            self.rows = rs.rows
            self.row_idx = 0
            self.rowcount = len(self.rows)
            self.lastrowid = rs.last_insert_rowid
            
            if rs.columns:
                self.description = []
                for col in rs.columns:
                    # name, type_code, display_size, internal_size, precision, scale, null_ok
                    self.description.append((col, None, None, None, None, None, None))
            else:
                self.description = None
                
        except Exception as e:
            # Better error reporting
            import sys
            print(f"Turso Database Error:", file=sys.stderr)
            print(f"  SQL: {sql}", file=sys.stderr)
            print(f"  Params: {params}", file=sys.stderr)
            print(f"  Error: {str(e)}", file=sys.stderr)
            
            # Try to extract more detail if it's a libsql error
            if hasattr(e, '__dict__'):
                print(f"  Error details: {e.__dict__}", file=sys.stderr)
            
            raise e
            
        return self

    def executemany(self, sql, param_list):
        for params in param_list:
            self.execute(sql, params)
        return self

    def fetchone(self):
        if self.row_idx < len(self.rows):
            row = self.rows[self.row_idx]
            self.row_idx += 1
            return row
        return None

    def fetchmany(self, size=None):
        if size is None:
            size = self.arraysize
        res = []
        for _ in range(size):
            row = self.fetchone()
            if row is None:
                break
            res.append(row)
        return res

    def fetchall(self):
        res = self.rows[self.row_idx:]
        self.row_idx = len(self.rows)
        return res

    def close(self):
        pass

class TursoConnection:
    def __init__(self, url, token):
        # Convert libsql:// to https:// to force HTTP protocol instead of WebSocket
        # This avoids 505 WebSocket handshake errors
        if url.startswith('libsql://'):
            url = url.replace('libsql://', 'https://')
        
        # Use sync client which handles the loop
        self.client = libsql_client.create_client_sync(url, auth_token=token)
        self.client.__enter__()
        self.autocommit = True 

    def cursor(self):
        return TursoCursor(self.client)

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        self.client.__exit__(None, None, None)

from django.db.backends.sqlite3.operations import DatabaseOperations as SQLiteDatabaseOperations

class DatabaseOperations(SQLiteDatabaseOperations):
    def last_executed_query(self, cursor, sql, params):
        return sql

class DatabaseFeatures(SQLiteDatabaseWrapper.features_class):
    uses_savepoints = False
    supports_transactions = False
    autocommit_when_autocommit_is_off = True

class DatabaseWrapper(SQLiteDatabaseWrapper):
    features_class = DatabaseFeatures
    ops_class = DatabaseOperations

    def get_new_connection(self, conn_params):
        url = conn_params['database']
        token = self.settings_dict['OPTIONS'].get('auth_token')
        return TursoConnection(url, token)

    def create_cursor(self, name=None):
        return self.connection.cursor()

    def _set_autocommit(self, autocommit):
        pass

    def validate_no_broken_transaction(self):
        pass
