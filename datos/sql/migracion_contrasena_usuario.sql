USE trello_db;

SET @columna_existe = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'usuario'
      AND COLUMN_NAME = 'password_hash'
);
SET @sql = IF(
    @columna_existe = 0,
    'ALTER TABLE usuario ADD COLUMN password_hash VARCHAR(255) NULL',
    'SELECT 1'
);
PREPARE migracion FROM @sql;
EXECUTE migracion;
DEALLOCATE PREPARE migracion;

SET @columna_existe = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'usuario'
      AND COLUMN_NAME = 'es_admin'
);
SET @sql = IF(
    @columna_existe = 0,
    'ALTER TABLE usuario ADD COLUMN es_admin TINYINT(1) NOT NULL DEFAULT 0',
    'SELECT 1'
);
PREPARE migracion FROM @sql;
EXECUTE migracion;
DEALLOCATE PREPARE migracion;
