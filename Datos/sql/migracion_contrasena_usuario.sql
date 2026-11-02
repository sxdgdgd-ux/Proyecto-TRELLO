USE trello_db;

ALTER TABLE usuario
    ADD COLUMN password_hash VARCHAR(255) NULL;
